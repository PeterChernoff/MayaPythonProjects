'''
Created on May 30, 2014
for Tin Girl Book and game project

@author: Eyal Assaf
'''
import maya.cmds as mc
# import tgpUtils as ut
from functools import partial
from tgpBaseUI import BaseUI as UI

'''
import tgpBlendColors as bc
reload(bc)
bc.tgpBlendColors()

'''


class pcCreateRigSpine(UI):
    def __init__(self):

        self.window = "bcWindow"
        self.title = "pcRigSpine"
        self.winSize = (500, 320)

        self.createUI()


    def createCustom(self, *args):
        '''
        #
        #
        #
        #
        #
        '''
        # selection type
        mc.rowColumnLayout(nc=2, cw=[(1, 500), (2, 500)], cs=[1, 5], rs=[1, 3])

        mc.text(l="Select The Root: ")
        '''mc.radioButtonGrp("selType_rbg", la2=["Hierarchy", "Selected"], nrb=2, sl=1, cw2=[80, 80],
                          onc=partial(self.tgpShowBtnOp, "1", "selType_rbg", "selGeo_cb"))
                          '''
        mc.text(l="")
        mc.checkBox("selGeo_cb", l="Affect Geometry", en=True, v=True)

        mc.setParent("..")
        mc.separator(st="in", h=20, w=500)

        # sources
        mc.rowColumnLayout(nc=2, cw=[(1, 100), (2, 370)], cs=[1, 5], rs=[1, 3])
        mc.text(bgc=(0.85, 0.65, 0.25), l="Joints: ")
        mc.textFieldButtonGrp("jointLoad_tfbg", cw=(1, 322), bl="  Load  ")

        mc.setParent("..")

        mc.separator(st="in", h=20, w=500)

        # Attributes


        # load buttons
        #
        # TO DELETE: May need to edit so the buttons load things properly
        mc.textFieldButtonGrp("jointLoad_tfbg", e=True, bc=self.loadSrc1Btn)

        #
        #

        #

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

    def createCTRLs(self, s, size=3, prnt = False, ornt = False, pnt=False, orientVal=(1, 0, 0), colour=5, sections=None):
        selname = str(s)


        ctrlName = selname.replace("JNT_", "CTRL_")
        if sections:
            ctrl = mc.circle(nr=orientVal, r=size, n=ctrlName, degree=1, sections=8)[0]
        else:
            ctrl = mc.circle(nr=orientVal, r=size, n=ctrlName)[0]

        mc.setAttr('{0}.overrideEnabled'.format(ctrlName), 1)
        mc.setAttr("{0}.overrideColor".format(ctrlName), colour)
        groupPC = mc.group(ctrl, n="AUTO_" + ctrl)
        offset = mc.group(groupPC, n="OFFSET_" + ctrl)

        mc.parentConstraint(s, offset, mo=0)
        mc.delete(mc.parentConstraint(s, offset))
        if prnt:
            mc.parentConstraint(ctrl, s, mo=0)
        if ornt:
            mc.orientConstraint(ctrl, s, mo=0)
        if pnt:
            mc.pointConstraint(ctrl, s, mo=0)

        offsetCtrl = [offset, ctrl]
        return offsetCtrl

    def lockHideCtrls(self, s, translate=False, rotate=False, scale=False):
        if translate:

            mc.setAttr("{0}.tx".format(s),k=False, l=True)
            mc.setAttr("{0}.ty".format(s), k=False, l=True)
            mc.setAttr("{0}.tz".format(s), k=False, l=True)
        if rotate:

            mc.setAttr("{0}.rx".format(s),k=False, l=True)
            mc.setAttr("{0}.ry".format(s), k=False, l=True)
            mc.setAttr("{0}.rz".format(s), k=False, l=True)
        if scale:

            mc.setAttr("{0}.sx".format(s),k=False, l=True)
            mc.setAttr("{0}.sy".format(s), k=False, l=True)
            mc.setAttr("{0}.sz".format(s), k=False, l=True)

    def tgpMakeBC(self, *args):

        checkGeo = mc.checkBox("selGeo_cb", q=True, v=True)

        self.jntNames = mc.textFieldButtonGrp("jointLoad_tfbg", q=True, text=True)
        #self.geoNames = mc.textFieldButtonGrp("GeoLoad_tfbg", q=True, text=True)

        # make sure the selections are not empty
        checkList = [self.jntNames]

        if ((checkList[0] == "")):
            mc.warning("You are missing a selection!")
            return
        else:
            # create the IK base controls
            jntEnd = self.jointArray[-1]

            noUnicode = str(jntEnd)
            print(noUnicode)
            jntEndSize = mc.getAttr('{0}.radius'.format(noUnicode))
            ikHip = mc.duplicate (jntEnd, n="JNT_IK_hip")
            print(ikHip)
            mc.parent(ikHip, w=True)
            noUnicode = str(ikHip[0])
            print(noUnicode)
            mc.setAttr('{0}.radius'.format(noUnicode), jntEndSize*3)
            ikMidSpine = mc.duplicate (ikHip, n="JNT_IK_midSpine")
            ikChest = mc.duplicate(ikHip, n="JNT_IK_chest")
            spineIKs = [ikHip[0], ikMidSpine[0], ikChest[0]]

            # gets values for later use
            jntSize = len(self.jointArray)
            midValue = int(jntSize/2)

            # moves the named IK joints into position using constraints, then deletes the constraints
            todelete1 = mc.pointConstraint(self.jointArray[0], ikHip, mo=False)
            todelete2 = mc.pointConstraint(self.jointArray[midValue], ikMidSpine, mo=False)

            mc.delete(todelete1, todelete2)

            try:
                mc.parent("GEO_hip", ikHip)
            except:
                mc.warning("Hip geometry either does not exist or is not properly named")

            # create the IK spline

            ikSpines = mc.ikHandle(n = "IK_spine", sj=self.jointArray[0], ee=jntEnd, sol="ikSplineSolver",numSpans=2)

            ikSpine = ikSpines[0]
            effSpine = ikSpines[1]
            crvSpine = ikSpines[2]

            effSpine = mc.rename(effSpine, "EFF_spine")
            crvSpine = mc.rename(crvSpine, "CRV_spine")

            # bind the curve to the JNT IKs
            '''
            Bind To: Selected Joints
            Bind Method: Closest Distance
            Skinning Method: Classic Linear
            Normalize Weights: Interactive
            '''
            mc.select(crvSpine, ikMidSpine, ikChest, ikHip)

            #mc.skinCluster (ikHip, ikMidSpine, ikChest, crvSpine, sm=0, nw = 1)

            scls = mc.skinCluster(ikMidSpine, ikChest, ikHip, crvSpine, name='spine_skinCluster', toSelectedBones=True,
                                  bindMethod=0, skinMethod=0, normalizeWeights=1)[0]

            # create controls for IK Spines
            spineIKCtrls = []
            for sik in spineIKs:
                spineIKCtrls.append(self.createCTRLs(sik, 19, prnt=True, colour=18))

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

            mc.connectAttr(ikHip[0] + ".worldMatrix[0]", ikSpine + ".dWorldUpMatrix")
            mc.connectAttr(ikChest[0] + ".worldMatrix[0]", ikSpine + ".dWorldUpMatrixEnd")



            print("-------")

            mc.setAttr('{0}.dTwistValueType'.format(ikSpine), 1)

            # adding stretch
            curveInfo = mc.arclen(crvSpine, ch = True)

            curveInfo = mc.rename(curveInfo, "spineInfo")
            curveLen = mc.getAttr("{0}.arcLength".format(curveInfo))
            mc.shadingNode("multiplyDivide", n="spine_md",au=True)
            mc.setAttr("spine_md.i2x".format(curveInfo), curveLen)
            mc.setAttr("spine_md.operation".format(curveInfo), 2)


            mc.connectAttr("{0}.arcLength".format(curveInfo), "spine_md.i1x")

            # get the scales to the spines


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


            for i in range(jntSize-1):
                mc.connectAttr("spine_md.ox", "{0}.scaleX".format(self.jointArray[i]))
                mc.connectAttr("spineSquashDiv_md.ox", "{0}.scaleY".format(self.jointArray[i]))
                mc.connectAttr("spineSquashDiv_md.ox", "{0}.scaleZ".format(self.jointArray[i]))


            #print(mc.getAttr("{0}.translate".format(self.jointArray[0])))

            # create FK joints, then orient them to world
            fkJnts = []
            for i in range(0, jntSize,2):
                if i == jntSize-1:
                    lastTerm = "end"
                else:
                    lastTerm = "{0}".format(i/2 + 1)

                pos = mc.xform(self.jointArray[i], query=True, translation=True, worldSpace=True )
                print(pos)
                fkJnts.append(mc.joint(name="JNT_FK_spine_{0}".format(lastTerm),p=pos, rad=jntEndSize*2))
                mc.joint("JNT_FK_spine_{0}".format(lastTerm), e=True, zso=True, oj="none")


            # create CTRLs, then parent them appropriately
            offsetCtrlFKJnts=[]  #keeps track of the offsets so we can parent them appropriately
            for i in range(len(fkJnts[:-1])):
                print(fkJnts[i])
                # Putting into a list so the CTRL sees it properly
                offsetCtrl = self.createCTRLs(fkJnts[i], 23, ornt=True, orientVal=(0,1,0), colour=17, sections=8)

                print(offsetCtrl)
                offsetCtrlFKJnts.append(offsetCtrl)
            # put the
            # mc.parent is driven, driver
            mc.parent(offsetCtrlFKJnts[1][0], offsetCtrlFKJnts[0][1])
            mc.parent(offsetCtrlFKJnts[2][0], offsetCtrlFKJnts[1][1])

            mc.parent(spineIKCtrls[1][0], offsetCtrlFKJnts[1][1])
            mc.parent(spineIKCtrls[2][0], offsetCtrlFKJnts[2][1])

            # create hip controls


            fkHip = mc.duplicate (ikHip, n="JNT_FK_hip")
            print(fkHip)
            print("------")
            # delete the children
            fkHipChilds= mc.listRelatives(fkHip[0], ad=True, f=True)
            mc.delete(fkHipChilds)
            fkHip=fkHip[0]


            fkHipEnd = mc.duplicate (fkHip, n="JNT_FK_hipEnd")
            mc.move(-20, fkHipEnd, y=True, r=True)

            mc.parent(fkHipEnd, fkHip)

            fkHipOffsetCtrl = self.createCTRLs(fkHip, 27, prnt=True, colour=17, sections=8)


            mc.parent(fkHipOffsetCtrl[0], spineIKCtrls[0][0])
            mc.parent(fkHip, ikHip) # TO DELETE: May need to edit this as I made a mistake when taking notes. fkHip needs to go under ikHip

            # Create center of gravity

            cogCTRL = mc.circle(nr=(1,0,0), r=35, n="CTRL_COG", degree=1, sections=6)[0]

            mc.setAttr('{0}.overrideEnabled'.format(cogCTRL), 1)
            mc.setAttr("{0}.overrideColor".format(cogCTRL), 13)

            cogCTRLGrp = mc.group(cogCTRL, n="AUTO_" + str(cogCTRL))
            cogCTRLOffset = mc.group(cogCTRLGrp, n="OFFSET_" + str(cogCTRL))

            mc.parent(cogCTRLOffset, spineIKCtrls[0][1],  relative=True)
            mc.parent(cogCTRLOffset, w=True)

            mc.pointConstraint(offsetCtrlFKJnts[0][1], fkJnts[0])
            # parent OFFSET_CTRL_spine_1 and OFFSET_CTRL_IK_hip under CTRL_COG
            mc.parent(offsetCtrlFKJnts[0][0], spineIKCtrls[0][0], cogCTRL)

            # group NT_IK_spine_1, JNT_IK_hip, JNT_IK_midSpine, JNT_IK_chest, JNT_FK_spine_1, (and JNT_FK_hip)
            # TO DELETE MAY NEED TO COME BACK TO AS GROUPING OBJECTS CREATES THE GROUP AT THE CENTER NOT THE ORIGIN

            #spineGrp = mc.group(self.jointArray[0], spineIKs, fkJnts[0], fkHip, n="Grp_JNT_spine")
            spineGrp = mc.group(n="GRP_JNT_spine", em=True, w=True)
            mc.parent(self.jointArray[0], spineIKs, fkJnts[0], spineGrp)

            ikGrpDNT = mc.group(n="GRP_doNotTouch_spine", em=True, w=True)
            mc.parent(crvSpine,ikSpine, ikGrpDNT)
            #ikGrpDNT = mc.group(crvSpine,ikSpine, n="GRP_doNotTouch_spine")

            rigSpine = mc.group(n="GRP_rig_spine", em=True, w=True)
            mc.parent(spineGrp, ikGrpDNT, rigSpine)

            #rigSpine = mc.group(spineGrp, ikGrpDNT, n="Grp_rig_spine")

            mc.setAttr("{0}.inheritsTransform".format(crvSpine), False)

            # lock attributes
            print(fkHip)
            self.lockHideCtrls(fkHipOffsetCtrl[1], translate=True, scale=True)
            for i in range(len(offsetCtrlFKJnts)):
                self.lockHideCtrls(offsetCtrlFKJnts[i][1], translate=True, scale=True)

            for i in range(len(spineIKs)):
                self.lockHideCtrls(spineIKCtrls[i][1], scale=True)


