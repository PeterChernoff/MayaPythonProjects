'''
Created on May 30, 2014
for Tin Girl Book and game project

@author: Eyal Assaf
'''
import maya.cmds as mc
# import tgpUtils as ut
from functools import partial
from tgpBaseUI import BaseUI as UI

import pcCreateRigUtilities
from pcCreateRigUtilities import pcCreateRigUtilities as CRU

reload(pcCreateRigUtilities)


class pcCreateRigSpine(UI):
    def __init__(self):

        self.window = "bcWindow"
        self.title = "pcRigSpine"
        self.winSize = (500, 320)

        self.createUI()

    def createCustom(self, *args):
        # selection type
        mc.rowColumnLayout(nc=2, cw=[(1, 500), (2, 500)], cs=[1, 5], rs=[1, 3])

        mc.text(l="Select The Root: ")
        mc.text(l="")
        mc.checkBox("selGeo_cb", l="Affect Geometry", en=True, v=True)

        mc.setParent("..")
        mc.separator(st="in", h=20, w=500)

        # sources
        mc.rowColumnLayout(nc=2, cw=[(1, 100), (2, 370)], cs=[1, 5], rs=[1, 3])
        mc.text(bgc=(0.85, 0.65, 0.25), l="IK Spine Joints: ")
        mc.textFieldButtonGrp("jointLoad_tfbg", cw=(1, 322), bl="  Load  ")

        mc.setParent("..")

        mc.separator(st="in", h=20, w=500)

        # load buttons
        mc.textFieldButtonGrp("jointLoad_tfbg", e=True, bc=self.loadSrc1Btn)

        mc.showWindow(self.window)

    def createButtonCmd(self, *args):
        self.tgpMakeBC()

    def tgpShowBtnOp(self, type, trigger, action, *args):
        if (type == "1"):
            # radio button
            checkBtn = mc.radioButtonGrp(trigger, q=True, select=True)
            # if "attr" not in trigger:
            if (checkBtn == 1):
                mc.checkBox(action, edit=True, en=True)
            else:
                mc.checkBox(action, edit=True, v=0, en=False)

        return

    def loadSrc1Btn(self):
        '''self.src1Sel = self.tgpLoadTxBtn("jointLoad_tfbg", "selType_rbg", "selGeo_cb")'''
        self.jntSel = self.tgpLoadTxBtn("jointLoad_tfbg", "joint")
        print(self.jntSel)

    def tgpLoadTxBtn(self, loadBtn, myType):
        # hierarchy
        self.selLoad = []
        self.selLoad = mc.ls(sl=True, fl=True, type="joint")
        if (len(self.selLoad) != 1):
            mc.warning("Select only the root joint")
            return
        else:

            selName = ', '.join(self.selLoad)
            mc.textFieldButtonGrp(loadBtn, e=True, tx=selName)

            # get the children joints
            self.parent = self.selLoad[0]
            self.child = mc.listRelatives(self.selLoad, ad=True, type="joint")
            # collect the joints in an array
            self.jointArray = [self.parent]
            # reverse the order of the children joints
            self.child.reverse()

            # add to the current list
            self.jointArray.extend(self.child)
            print(self.jointArray)

        return self.jointArray

    def createSpineIK(self, jntEnd, jntEndSize, midValue, *args):

        ikHip = mc.duplicate(jntEnd, n="JNT_IK_hip", renameChildren=True)
        print(ikHip)
        mc.parent(ikHip, w=True)
        noUnicode = str(ikHip[0])
        print(noUnicode)
        mc.setAttr('{0}.radius'.format(noUnicode), jntEndSize * 3)
        ikMidSpine = mc.duplicate(ikHip, n="JNT_IK_midSpine")
        ikChest = mc.duplicate(ikHip, n="JNT_IK_chest")
        spineIKs = [ikHip[0], ikMidSpine[0], ikChest[0]]

        print(ikHip)

        # moves the named IK joints into position using constraints, then deletes the constraints
        todelete1 = mc.pointConstraint(self.jointArray[0], ikHip[0], mo=False)
        todelete2 = mc.pointConstraint(self.jointArray[midValue], ikMidSpine, mo=False)

        mc.delete(todelete1, todelete2)

        return ikHip[0], ikMidSpine, ikChest[0], spineIKs

    def createIKSpline(self, jntEnd, *args):

        ikSpines = mc.ikHandle(n="IK_spine", sj=self.jointArray[0], ee=jntEnd, sol="ikSplineSolver", numSpans=2)

        ikSpine = ikSpines[0]
        effSpine = ikSpines[1]
        crvSpine = ikSpines[2]

        effSpine = mc.rename(effSpine, "EFF_spine")
        crvSpine = mc.rename(crvSpine, "CRV_spine")

        return ikSpine, effSpine, crvSpine

    def createIKSpineCtrls(self, crvSpine, ikMidSpine, ikChest, ikHip, spineIKs, *args):
        '''
        Bind To: Selected Joints
        Bind Method: Closest Distance
        Skinning Method: Classic Linear
        Normalize Weights: Interactive
        '''
        mc.select(crvSpine, ikMidSpine, ikChest, ikHip)

        # mc.skinCluster (ikHip, ikMidSpine, ikChest, crvSpine, sm=0, nw = 1)

        scls = mc.skinCluster(ikMidSpine, ikChest, ikHip, crvSpine, name='spine_skinCluster', toSelectedBones=True,
                              bindMethod=0, skinMethod=0, normalizeWeights=1)[0]

        # create controls for IK Spines
        spineIKCtrls = []
        spineIKSizes = [[1, 26, 20], [1, 28, 20], [1, 15, 15]]

        for i in range(len(spineIKs)):
            spineIKCtrls.append(
                CRU.createCTRLs(spineIKs[i], 19, prnt=True, colour=18, boxDimensionsLWH=spineIKSizes[i]))

        # make the neck area more appealing
        '''cvsToMove = mc.select(spineIKCtrls[-1][1] + ".cv[:]")
        mc.rotate(-20, cvsToMove, y=True)
        mc.move(-2, cvsToMove, x=True, r=True, wd=True, ls=True)
        mc.move(2, cvsToMove, z=True, r=True, wd=True, ls=True)'''

        return spineIKCtrls

    def addIkTwist(self, ikSpine, ikHip, ikChest, *args):

        '''
        Set World Up Type to Object Rotation Up (Start/End)
        Set Up axis to Negative Z
        Set Up Vector and Up Vector 2 to 0, 0, -1 (Best works if all joints are facing the same direction)
        Set World Up Object to CTRL_IK_hip
        Set World Up Object 2 to CTRL_IK_chest
        Set Twist Value Type to Start/End.
        '''
        mc.setAttr('{0}.dTwistControlEnable'.format(ikSpine), True)
        mc.setAttr('{0}.dWorldUpType'.format(ikSpine), 4)
        mc.setAttr('{0}.dWorldUpAxis'.format(ikSpine), 4)

        mc.setAttr('{0}.dWorldUpVectorX'.format(ikSpine), 0)
        mc.setAttr('{0}.dWorldUpVectorY'.format(ikSpine), 0)
        mc.setAttr('{0}.dWorldUpVectorZ'.format(ikSpine), -1)

        mc.setAttr('{0}.dWorldUpVectorEndX'.format(ikSpine), 0)
        mc.setAttr('{0}.dWorldUpVectorEndY'.format(ikSpine), 0)
        mc.setAttr('{0}.dWorldUpVectorEndZ'.format(ikSpine), -1)

        mc.connectAttr(ikHip + ".worldMatrix[0]", ikSpine + ".dWorldUpMatrix")
        mc.connectAttr(ikChest + ".worldMatrix[0]", ikSpine + ".dWorldUpMatrixEnd")

        mc.setAttr('{0}.dTwistValueType'.format(ikSpine), 1)

    def addStretch(self, crvSpine, jntSize, *args):
        curveInfo = mc.arclen(crvSpine, ch=True)

        curveInfo = mc.rename(curveInfo, "spineInfo")
        curveLen = mc.getAttr("{0}.arcLength".format(curveInfo))
        mc.shadingNode("multiplyDivide", n="spine_md", au=True)

        mc.setAttr("spine_md.i2x".format(curveInfo), curveLen)
        mc.setAttr("spine_md.operation".format(curveInfo), 2)

        mc.connectAttr("{0}.arcLength".format(curveInfo), "spine_md.i1x")

        # get the scales to the spines

        # to allow for the squash/stretch
        # get square root of output
        mc.shadingNode("multiplyDivide", n="spineSquashPow_md", au=True)
        mc.setAttr("spineSquashPow_md.operation".format(curveInfo), 3)
        mc.setAttr("spineSquashPow_md.i2x".format(curveInfo), 0.5)
        mc.connectAttr("spine_md.ox", "spineSquashPow_md.i1x")

        # divide by the square root
        mc.shadingNode("multiplyDivide", n="spineSquashDiv_md", au=True)
        mc.setAttr("spineSquashDiv_md.operation".format(curveInfo), 2)
        mc.setAttr("spineSquashDiv_md.i1x".format(curveInfo), 1)
        mc.connectAttr("spineSquashPow_md.ox", "spineSquashDiv_md.i2x")

        for i in range(jntSize - 1):
            # connects the spine joints to the joint scale to allow for squash and stretch
            mc.connectAttr("spine_md.ox", "{0}.scaleX".format(self.jointArray[i]))
            mc.connectAttr("spineSquashDiv_md.ox", "{0}.scaleY".format(self.jointArray[i]))
            mc.connectAttr("spineSquashDiv_md.ox", "{0}.scaleZ".format(self.jointArray[i]))

    def createFKJntAndCtrls(self, jntSize, jntEndSize, spineIKCtrls, *args):

        # create FK joints, then orient them to world
        fkJnts = []
        for i in range(0, jntSize, 2):
            if i == jntSize - 1:
                lastTerm = "end"
            else:
                lastTerm = "{0}".format(i / 2 + 1)

            pos = mc.xform(self.jointArray[i], query=True, translation=True, worldSpace=True)
            print(pos)
            fkJnts.append(mc.joint(name="JNT_FK_spine_{0}".format(lastTerm), p=pos, rad=jntEndSize * 2))
            mc.joint("JNT_FK_spine_{0}".format(lastTerm), e=True, zso=True, oj="none")

        # create CTRLs, then parent them appropriately
        offsetCtrlFKJnts = []  # keeps track of the offsets so we can parent them appropriately
        for i in range(len(fkJnts[:-1])):
            print(fkJnts[i])
            # Putting into a list so the CTRL sees it properly
            offsetCtrl = CRU.createCTRLs(fkJnts[i], 23, ornt=True, orientVal=(0, 1, 0), colour=17)

            print(offsetCtrl)
            offsetCtrlFKJnts.append(offsetCtrl)

        cvsToMove = mc.select(offsetCtrlFKJnts[0][1] + ".cv[:]")
        mc.move(5, cvsToMove, y=True, r=True, wd=True, ls=True)

        cvsToMove = mc.select(offsetCtrlFKJnts[-1][1] + ".cv[:]")
        mc.move(-5, cvsToMove, y=True, r=True, wd=True, ls=True)

        # put the
        # mc.parent is driven, driver
        mc.parent(offsetCtrlFKJnts[1][0], offsetCtrlFKJnts[0][1])
        mc.parent(offsetCtrlFKJnts[2][0], offsetCtrlFKJnts[1][1])

        mc.parent(spineIKCtrls[1][0], offsetCtrlFKJnts[1][1])
        mc.parent(spineIKCtrls[2][0], offsetCtrlFKJnts[2][1])

        return fkJnts, offsetCtrlFKJnts

    def createHipCtrl(self, ikHip, spineIKCtrls, *args):
        # create hip controls


        fkHip = mc.duplicate(ikHip, n="JNT_FK_hip")
        print(fkHip)
        print("------")
        # delete the children
        fkHipChilds = mc.listRelatives(fkHip[0], ad=True, f=True)
        mc.delete(fkHipChilds)
        fkHip = fkHip[0]

        fkHipEnd = mc.duplicate(fkHip, n="JNT_FK_hipEnd")[0]
        mc.move(-20, fkHipEnd, y=True, r=True)
        valToMove = mc.getAttr("{0}.ty".format(fkHipEnd))

        mc.parent(fkHipEnd, fkHip)

        fkHipOffsetCtrl = CRU.createCTRLs(fkHip, 27, prnt=True, colour=17)
        cvsToMove = mc.select(fkHipOffsetCtrl[1] + ".cv[:]")
        print(valToMove)
        mc.move(-10, cvsToMove, x=True, r=True, wd=True, ls=True)

        mc.parent(fkHipOffsetCtrl[0], spineIKCtrls[0][
            1])
        print(fkHip)
        print(ikHip)
        mc.parent(fkHip, ikHip)

        return fkHip, fkHipOffsetCtrl

    def createCOGCtrl(self, spineIKCtrls, offsetCtrlFKJnts, fkJnts, spineIKs, crvSpine, ikSpine, *args):
        # Create center of gravity

        cogCtrl = mc.circle(nr=(1, 0, 0), r=45, n="CTRL_COG", degree=1, sections=3)[0]
        cvsToMove = mc.select(cogCtrl + ".cv[:]")
        mc.rotate(90, cvsToMove, x=True)
        mc.move(10, cvsToMove, x=True, r=True, wd=True, ls=True)

        mc.setAttr('{0}.overrideEnabled'.format(cogCtrl), 1)
        mc.setAttr("{0}.overrideColor".format(cogCtrl), 31)

        cogAuto = mc.group(cogCtrl, n="AUTO_" + str(cogCtrl))
        cogOffset = mc.group(cogAuto, n="OFFSET_" + str(cogCtrl))

        cogOffsetCtrl = []
        cogOffsetCtrl.append(cogOffset)
        cogOffsetCtrl.append(cogCtrl)
        cogOffsetCtrl.append(cogAuto)

        mc.parent(cogOffset, spineIKCtrls[0][1], relative=True)
        mc.parent(cogOffset, w=True)

        mc.pointConstraint(offsetCtrlFKJnts[0][1], fkJnts[0])
        # parent OFFSET_CTRL_spine_1 and OFFSET_CTRL_IK_hip under CTRL_COG
        mc.parent(offsetCtrlFKJnts[0][0], spineIKCtrls[0][0], cogCtrl)

        # group JNT_IK_spine_1, JNT_IK_hip, JNT_IK_midSpine, JNT_IK_chest, JNT_FK_spine_1, (and JNT_FK_hip)

        # spineGrp = mc.group(self.jointArray[0], spineIKs, fkJnts[0], fkHip, n="Grp_JNT_spine")
        spineGrp = mc.group(n="GRP_JNT_spine", em=True, w=True)
        mc.parent(self.jointArray[0], spineIKs, fkJnts[0], spineGrp)

        ikGrpDNT = mc.group(n="GRP_doNotTouch_spine", em=True, w=True)
        mc.parent(crvSpine, ikSpine, ikGrpDNT)

        mc.setAttr("{0}.inheritsTransform".format(crvSpine), False)

        return cogOffsetCtrl

    def spineCleanup(self, fkHipOffsetCtrl, offsetCtrlFKJnts, spineIKs, spineIKCtrls, cogOffsetCtrl, crvSpine, ikSpine,
                     *args):
        # lock attributes
        CRU.lockHideCtrls(fkHipOffsetCtrl[1], translate=True, scale=True, visible=True)
        print(offsetCtrlFKJnts)
        for i in range(len(offsetCtrlFKJnts)):
            CRU.lockHideCtrls(offsetCtrlFKJnts[i][1], translate=True, scale=True, visible=True)

        for i in range(len(spineIKs)):
            CRU.lockHideCtrls(spineIKCtrls[i][1], scale=True, visible=True)
            print(spineIKCtrls[i][1])

        CRU.lockHideCtrls(cogOffsetCtrl[1], scale=True, visible=True)

        mc.setAttr('{0}.v'.format(crvSpine), False)
        mc.setAttr('{0}.v'.format(ikSpine), False)

        CRU.lockHideCtrls(crvSpine, visible=True)
        CRU.lockHideCtrls(ikSpine, visible=True)

        '''
        #TO DELETE: come back and adjust it so it can put the FK and IKs into the layer 
        CRU.layerEdit(spineIKs, ikLayer=True)
        CRU.layerEdit(fkJnts, ikLayer=True)'''

    def tgpMakeBC(self, *args):

        checkGeo = mc.checkBox("selGeo_cb", q=True, v=True)

        self.jntNames = mc.textFieldButtonGrp("jointLoad_tfbg", q=True, text=True)
        # self.geoNames = mc.textFieldButtonGrp("GeoLoad_tfbg", q=True, text=True)

        # make sure the selections are not empty
        checkList = [self.jntNames]

        if ((checkList[0] == "")):
            mc.warning("You are missing a selection!")
            return
        else:
            # print(m.ModClass.static_method())
            CRU.createLocatorToDelete()
            # create the IK base controls
            jntEnd = self.jointArray[-1]

            noUnicode = str(jntEnd)
            print(noUnicode)
            jntEndSize = mc.getAttr('{0}.radius'.format(noUnicode))

            # gets values for later use
            jntSize = len(self.jointArray)
            midValue = int(jntSize / 2)

            # Create the IK joints
            ikHip, ikMidSpine, ikChest, spineIKs = self.createSpineIK(jntEnd, jntEndSize, midValue)

            # Adding the Spline IK
            ikSpine, effSpine, crvSpine = self.createIKSpline(jntEnd)

            # Creating the IK Spine Controls:
            # bind the curve to the JNT IKs,
            spineIKCtrls = self.createIKSpineCtrls(crvSpine, ikMidSpine, ikChest, ikHip, spineIKs)

            # Adding the IK twist
            self.addIkTwist(ikSpine, ikHip, ikChest, )

            # Adding Some Stretch
            self.addStretch(crvSpine, jntSize, )

            # FK Joints and Controls
            fkJnts, offsetCtrlFKJnts = self.createFKJntAndCtrls(jntSize, jntEndSize, spineIKCtrls)

            # Adding an extra hip control
            fkHip, fkHipOffsetCtrl = self.createHipCtrl(ikHip, spineIKCtrls)

            # Creating the COG control
            cogOffsetCtrl = self.createCOGCtrl(spineIKCtrls, offsetCtrlFKJnts, fkJnts, spineIKs, crvSpine, ikSpine, )

            # cleanup
            self.spineCleanup(fkHipOffsetCtrl, offsetCtrlFKJnts, spineIKs, spineIKCtrls, cogOffsetCtrl, crvSpine,
                              ikSpine, )

            # make the last thing we do the geometry
            if checkGeo:
                print("2222222")
                CRU.tgpSetGeo(self.jointArray, "JNT_IK_")
            try:
                CRU.tgpSetGeo([fkHip], "JNT_FK_")
                # mc.parent("GEO_hip", ikHip)
            except:
                mc.warning("Hip geometry either does not exist or is not properly named")
