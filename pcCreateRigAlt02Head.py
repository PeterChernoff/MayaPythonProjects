'''
Created on May 30, 2014
for Tin Girl Book and game project

@author: Eyal Assaf
'''
import maya.cmds as mc
# import tgpUtils as ut
from functools import partial
from tgpBaseUI import BaseUI as UI

import pcCreateRigAlt00AUtilities
from pcCreateRigAlt00AUtilities import pcCreateRigUtilities as CRU

reload(pcCreateRigAlt00AUtilities)


class pcCreateRigAlt02Head(UI):
    def __init__(self):

        self.window = "bcWindow"
        self.title = "pcRigHead"
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

        mc.text(l="Select The BND Neck Root: ")
        mc.text(l="")
        mc.setParent("..")
        mc.separator(st="in", h=17, w=500)
        mc.checkBox("selSpineEnd_cb", l="Connect To Spine", en=True, v=True)

        mc.separator(st="in", h=17, w=500)

        # sources
        mc.rowColumnLayout(nc=2, cw=[(1, 140), (2, 360)], cs=[1, 5], rs=[1, 3])
        mc.text(bgc=(0.85, 0.65, 0.25), l="Neck Start Joint: ")
        mc.textFieldButtonGrp("jointLoad_tfbg", cw=(1, 300), bl="  Load  ")

        mc.text(bgc=(0.85, 0.65, 0.25), l="IK Shoulder Joint: ")
        mc.textFieldButtonGrp("jntIKShoulderLoad_tf", cw=(1, 300), bl="  Load  ", tx="JNT_IK_shoulder")

        mc.text(bgc=(0.85, 0.65, 0.25), l="Torso DNT Group: ")
        mc.textFieldButtonGrp("grpTorsoDNT_tfbg", cw=(1, 300), bl="  Load  ", tx="GRP_DO_NOT_TOUCH")

        mc.text(bgc=(0.85, 0.65, 0.25), l="Root Transform Control: ")
        mc.textFieldButtonGrp("rootTrans_tfbg", cw=(1, 300), bl="  Load  ", tx="CTRL_rootTransform_emma")

        mc.separator(st="in", h=17, w=500)
        mc.setParent("..")

        mc.rowColumnLayout(nc=2, cw=[(1, 100), (2, 380)], cs=[1, 5], rs=[1, 3])
        mc.checkBox("selGeo_cb", l="Affect Geometry", en=True, v=False)

        mc.setParent("..")
        # Attributes

        # load buttons
        mc.textFieldButtonGrp("jointLoad_tfbg", e=True, bc=self.loadSrc1Btn)
        mc.textFieldButtonGrp("jntIKShoulderLoad_tf", e=True, bc=self.loadSrc2Btn)
        mc.textFieldButtonGrp("grpTorsoDNT_tfbg", e=True, bc=self.loadSrc3Btn)
        mc.textFieldButtonGrp("rootTrans_tfbg", e=True, bc=self.loadSrc4Btn)

        mc.showWindow(self.window)

    def createButtonCmd(self, *args):
        self.tgpMakeBC()

    def loadSrc1Btn(self):
        self.selSrc1 = self.tgpLoadJntsBtn("jointLoad_tfbg", "joint", "Root Neck Joint", ["JNT", "BND", "neck", "1"])
        print(self.selSrc1)

    def loadSrc2Btn(self):
        self.selSrc2 = self.tgpLoadTxBtn("jntIKShoulderLoad_tf", "joint", "IK Shoulder Joint",
                                         ["JNT", "_IK_", "shoulder"], "control")
        print(self.selSrc2)

    def loadSrc3Btn(self):
        self.selSrc3 = self.tgpLoadTxBtn("grpTorsoDNT_tfbg", "transform", "Torso DO NOT TOUCH",
                                         ["GRP", "DO", "NOT", "TOUCH"],
                                         "group")
        print(self.selSrc3)

    def loadSrc4Btn(self):
        self.selSrc4 = self.tgpLoadTxBtn("rootTrans_tfbg", "nurbsCurve", "Root Transform Control",
                                         ["CTRL", "rootTransform"])
        print(self.selSrc4)

    def tgpLoadTxBtn(self, loadBtn, objectType, objectDesc, keywords, objectNickname=None):
        if objectNickname is None:
            objectNickname = objectType

        self.selLoad = []
        self.selLoad = mc.ls(sl=True, fl=True, type="transform")

        if (len(self.selLoad) != 1):
            mc.warning("Select only the {0}".format(objectDesc))
            return
        else:
            if CRU.checkObjectType(self.selLoad[0]) != objectType:
                mc.warning("{0} should be a {1}".format(objectDesc, objectNickname))
                return
            selName = self.selLoad[0]

            if not all(word.lower() in selName.lower() for word in keywords):
                mc.warning("That is the wrong {0}. Select the {1}".format(objectNickname, objectDesc))
                return
            mc.textFieldButtonGrp(loadBtn, e=True, tx=selName)
            return selName

    def tgpLoadJntsBtn(self, loadBtn, objectType, objectDesc, keywords, objectNickname=None):
        if objectNickname is None:
            objectNickname = objectType
        # hierarchy
        self.selLoad = []
        self.selLoad = mc.ls(sl=True, fl=True, type=objectType)
        if (len(self.selLoad) != 1):
            mc.warning("Select only the {0}".format(objectDesc))
            return
        else:

            selName = self.selLoad[0]

            if not all(word.lower() in selName.lower() for word in keywords):
                mc.warning("That is the wrong {0}. Select the {1}".format(objectNickname, objectDesc))
                return
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

            self.jointArrayNeck = [x for x in self.jointArray if "neck" in x]
            # removes if the last joint is End
            # checks if the last three letters are "End"
            self.jointEndArray = [x for x in self.jointArray if "End" in x[-3:]]
            self.jointArray = [x for x in self.jointArray if "End" not in x[-3:]]

        return self.jointArray

    def createIKSpline(self, jntStart, jntEnd, name, *args):

        ikSpline = mc.ikHandle(n="HDL_{0}".format(name), sj=jntStart, ee=jntEnd, sol="ikSplineSolver", numSpans=1)

        hdlSpline = ikSpline[0]
        effSpline = ikSpline[1]
        crvSpline = ikSpline[2]

        effSpline = mc.rename(effSpline, "EFF_{0}".format(name))
        crvSpline = mc.rename(crvSpline, "CRV_{0}".format(name))

        return hdlSpline, effSpline, crvSpline

    def createNeckIK(self, jntArray, jntEnd, jntEndSize, crvToUse, *args):

        ikNeckBase = mc.duplicate(jntEnd, n="JNT_IK_neckBase", renameChildren=True)
        mc.parent(ikNeckBase, w=True)
        noUnicode = str(ikNeckBase[0])
        mc.setAttr('{0}.radius'.format(noUnicode), jntEndSize * 3)
        ikNeckEnd = mc.duplicate(ikNeckBase, n="JNT_IK_neckEnd")
        print(ikNeckEnd)
        CRU.changeRotateOrder(ikNeckEnd, "ZXY")
        neckIKs = [ikNeckBase[0], ikNeckEnd[0]]

        # moves the named IK joints into position using constraints, then deletes the constraints
        todelete1 = mc.parentConstraint(jntArray[0], ikNeckBase[0], mo=False)

        mc.delete(todelete1)

        '''
        Bind To: Selected Joints
        Bind Method: Closest Distance
        Skinning Method: Classic Linear
        Normalize Weights: Interactive
        Max Influences  2

        '''
        mc.select(crvToUse, ikNeckBase, ikNeckEnd)

        # mc.skinCluster (ikHip, ikShoulder, crvSpine, sm=0, nw = 1)

        scls = mc.skinCluster(ikNeckBase, ikNeckEnd, crvToUse, name='neck_skinCluster', toSelectedBones=True,
                              bindMethod=0, skinMethod=0, normalizeWeights=1, maximumInfluences=2)[0]

        return ikNeckBase[0], ikNeckEnd[0], neckIKs

    def addIkTwist(self, hdlSpline, ikBase, ikEnd, *args):

        '''
        Set World Up Type to Object Rotation Up (Start/End)
        Set Forward axis to Positive X
        Set Up axis to Negative Y
        Set Up Vector to 0, -1, 0
        Set Up Vector 2 to 0, -1, 0 (Best works if all joints are facing the same direction, and may need to be adjusted)
        Note: this would likely be 0, -1, -1 if using the default version with the end joint set to world space
        Set World Up Object to JNT_IK_neckBase
        Set World Up Object 2 to JNT_IK_neckEnd
        Set Twist Value Type to Start/End.

        '''
        mc.setAttr('{0}.dTwistControlEnable'.format(hdlSpline), True)

        mc.setAttr('{0}.dForwardAxis'.format(hdlSpline), 0)

        mc.setAttr('{0}.dWorldUpType'.format(hdlSpline), 4)
        mc.setAttr('{0}.dWorldUpAxis'.format(hdlSpline), 1)

        mc.setAttr('{0}.dWorldUpVectorX'.format(hdlSpline), 0)
        mc.setAttr('{0}.dWorldUpVectorY'.format(hdlSpline), -1)
        mc.setAttr('{0}.dWorldUpVectorZ'.format(hdlSpline), 0)

        mc.setAttr('{0}.dWorldUpVectorEndX'.format(hdlSpline), 0)
        mc.setAttr('{0}.dWorldUpVectorEndY'.format(hdlSpline), -1)
        mc.setAttr('{0}.dWorldUpVectorEndZ'.format(hdlSpline), 0)

        mc.connectAttr(ikBase + ".worldMatrix[0]", hdlSpline + ".dWorldUpMatrix")
        mc.connectAttr(ikEnd + ".worldMatrix[0]", hdlSpline + ".dWorldUpMatrixEnd")

        mc.setAttr('{0}.dTwistValueType'.format(hdlSpline), 1)
        mc.select(hdlSpline)

    def createHeadCtrls(self, ikNeckEnd, *args):
        # Creates the head control
        ctrlHeadName = "CTRL_head"
        ctrlHeadPre, ctrlHeadPreName = CRU.setupCtrl(ikNeckEnd, 14, orientVal=(0, 1, 0), colour=17, )
        ctrlHead = mc.rename(ctrlHeadPre, ctrlHeadName)
        todelete = mc.pointConstraint(ikNeckEnd, ctrlHead)
        mc.delete(todelete)

        mc.makeIdentity(ctrlHead, apply=True, t=True, r=True, s=True)
        mc.select(ctrlHead + ".cv[:]")
        mc.move(20, y=True, r=True, os=True, wd=True)
        CRU.changeRotateOrder([ctrlHead], "ZXY")
        CRU.layerEdit([ctrlHead], ikLayer=True, noRecurse=True)
        mc.parentConstraint(ctrlHead, ikNeckEnd, mo=True)

        return ctrlHead

    def createFKJntAndCtrls(self, jntArray, jntEnd, jntEndSize, *args):

        mc.select(cl=True)
        # create FK joints, then orient them to world
        fkJnts = []
        ctrlFKJntsTU = []
        addFKJnt = False
        grpFKConsts = []
        ctrlFKJntsEnds = []

        jntSize = len(jntArray)

        for i in range(0, jntSize):
            if i == jntSize - 1:
                lastTerm = "End"
            elif i == 0:
                lastTerm = "Base"
                addFKJnt = True
            else:
                # we only care if it's the first or last
                continue

            fkName = "JNT_FK_neck{0}".format(lastTerm)

            pos = mc.xform(jntArray[i], query=True, translation=True, worldSpace=True)
            fkJnts.append(mc.joint(name=fkName, p=pos, rad=jntEndSize * 2))

            if addFKJnt:
                ctrlFKJntsTU.append(fkName)

            else:
                # creates the names for GRP_FKConsts
                ctrlFKJntsEnds.append(fkName)
                grpFKConsts.append("GRP_FKConst{0}".format(lastTerm))

            mc.setAttr('{0}.overrideEnabled'.format(fkName), 1)
            mc.setAttr("{0}.overrideColor".format(fkName), 28)

            addFKJnt = False
        # change the rotate order
        CRU.changeRotateOrder([fkJnts[0]], "YZX")
        for i in range(len(fkJnts) - 1):
            mc.joint(fkJnts[i], e=True, zso=True, oj="yxz", secondaryAxisOrient="xup")

        # create the FK control and move it into a nice position
        ctrlFK = CRU.createCTRLsFKDirect(fkJnts[0], 10, orientVal=(0, 1, 0), colour=28)
        ctrlShape = mc.listRelatives(ctrlFK, s=True, )[0]
        fkJnts[0] = ctrlFK

        fkLength = mc.getAttr("{0}.ty".format(fkJnts[-1]))
        cvsToMove = mc.select(ctrlShape + ".cv[:]")
        mc.move(fkLength * .35, cvsToMove, y=True, r=True, wd=True, os=True)

        CRU.layerEdit(fkJnts, fkLayer=True, noRecurse=True)

        return ctrlFK, fkJnts

    def createGroupHead(self, ctrlHead, ikNeckEnd, fkJnts, *args):

        grpHead = "GRP_head"
        mc.group(em=True, w=True, n=grpHead)
        todelete = mc.pointConstraint(ikNeckEnd, grpHead)
        mc.delete(todelete)
        mc.makeIdentity(grpHead, a=True)
        mc.parent(ctrlHead, grpHead)

        todelete = mc.parentConstraint(fkJnts[-1], grpHead, mo=True)
        # chapter 9 has this deleted so we'll do that here
        mc.delete(todelete)

        return grpHead

    def addStretch(self, jntArray, crvSpline, jntSize, name, ctrlRootTrans, *args):
        curveInfo = mc.arclen(crvSpline, ch=True)
        splineInfo = "{0}Info".format(name)

        curveInfo = mc.rename(curveInfo, splineInfo)
        curveLen = mc.getAttr("{0}.arcLength".format(curveInfo))
        splineStretchNameDiv = "{0}_stretchPercent_DIV".format(name)
        mc.shadingNode("multiplyDivide", n=splineStretchNameDiv, au=True)

        mc.setAttr("{0}.i2x".format(splineStretchNameDiv), curveLen)
        mc.setAttr("{0}.operation".format(splineStretchNameDiv), 2)

        mc.connectAttr("{0}.arcLength".format(curveInfo), "{0}.i1x".format(splineStretchNameDiv))

        # get the scales to the spline

        # to allow for the squash/stretch
        # get square root of output

        splineStretchNamePow = "{0}_sqrtStretch_POW".format(name)

        mc.shadingNode("multiplyDivide", n=splineStretchNamePow, au=True)
        mc.setAttr("{0}.operation".format(splineStretchNamePow), 3)
        mc.setAttr("{0}.i2x".format(splineStretchNamePow), 0.5)
        mc.connectAttr("{0}.ox".format(splineStretchNameDiv), "{0}.i1x".format(splineStretchNamePow))

        # divide by the square root
        splineStretchNameInv = "{0}_stretchInvert_DIV".format(name)
        mc.shadingNode("multiplyDivide", n=splineStretchNameInv, au=True)
        mc.setAttr("{0}.operation".format(splineStretchNameInv), 2)
        mc.setAttr("{0}.i1x".format(splineStretchNameInv), 1)
        mc.connectAttr("{0}.ox".format(splineStretchNamePow), "{0}.i2x".format(splineStretchNameInv))

        for i in range(jntSize - 1):
            # connects the spline's joints to the joint scale to allow for squash and stretch
            mc.connectAttr("{0}.ox".format(splineStretchNameDiv), "{0}.scaleX".format(jntArray[i]))
            mc.connectAttr("{0}.ox".format(splineStretchNameInv), "{0}.scaleY".format(jntArray[i]))
            mc.connectAttr("{0}.ox".format(splineStretchNameInv), "{0}.scaleZ".format(jntArray[i]))

        globalScaleNormalizeDiv = "globalScale_{0}Normalize_DIV".format(name)
        mc.shadingNode("multiplyDivide", n=globalScaleNormalizeDiv, au=True)
        mc.setAttr("{0}.operation".format(globalScaleNormalizeDiv), 2)

        mc.connectAttr("{0}.arcLength".format(splineInfo), "{0}.i1x".format(globalScaleNormalizeDiv))
        mc.connectAttr("{0}.sy".format(ctrlRootTrans), "{0}.i2x".format(globalScaleNormalizeDiv))
        # we want to overwrite the old version
        mc.connectAttr("{0}.ox".format(globalScaleNormalizeDiv), "{0}.i1x".format(splineStretchNameDiv), f=True)

        return splineInfo, splineStretchNameDiv

    def parentRootTransform(self, ctrlRootTrans, crvNeck, hdlNeck, ikNeckBase, ikNeckEnd, grpHead, fkJntStart,
                            jntArrayStart, *args):
        grpHeadNeckName = "GRP_headNeck"
        grpHeadNeck = mc.group(n=grpHeadNeckName, w=True, em=True)
        mc.parent(crvNeck, hdlNeck, ikNeckBase, ikNeckEnd, grpHead, fkJntStart, jntArrayStart, grpHeadNeck)
        mc.parent(grpHeadNeck, ctrlRootTrans)

        mc.setAttr("{0}.inheritsTransform".format(crvNeck), False)
        return

    def createNeckShoulderLoc(self, checkboxSpine, jntIKShoulder, ikNeckBase, fkJnts, *args):
        locConstNeckShoulder = mc.spaceLocator(p=(0, 0, 0), name="LOC_const_neckShoulder")[0]
        # move to the base of the neck
        todelete = mc.pointConstraint(ikNeckBase, locConstNeckShoulder)
        mc.delete(todelete)

        if checkboxSpine:
            mc.parent(locConstNeckShoulder, jntIKShoulder)

        # Create a group for the FKNeck joint
        grpNeckFK = "GRP_FK_neck"
        mc.group(n=grpNeckFK, w=True, em=True)
        parentFK = mc.listRelatives(fkJnts[0], p=True)[0]
        mc.parent(grpNeckFK, parentFK)
        mc.parent(fkJnts[0], grpNeckFK)

        # locConstNeckShoulder parent constrains ikNeckBase and grpNeckFK
        mc.parentConstraint(locConstNeckShoulder, ikNeckBase, mo=True)
        mc.parentConstraint(locConstNeckShoulder, grpNeckFK, mo=True)

        mc.setAttr("{0}.v".format(locConstNeckShoulder), False)

        return locConstNeckShoulder, grpNeckFK

    def createSpaceSwitching(self, ctrlHead, jntIKShoulder, ctrlRootTrans, fkJnts, grpTorsoDNT, *args):

        # creates the head follow attributes
        headLocArray = []
        headLocArray.append(mc.spaceLocator(p=(0, 0, 0), name="LOC_space_headNeck")[0])
        headLocArray.append(mc.spaceLocator(p=(0, 0, 0), name="LOC_space_headShoulder")[0])
        headLocArray.append(mc.spaceLocator(p=(0, 0, 0), name="LOC_space_headBody")[0])
        headLocArray.append(mc.spaceLocator(p=(0, 0, 0), name="LOC_space_headRoot")[0])

        # moves these to the head
        for i in range(len(headLocArray)):
            todelete = mc.pointConstraint(fkJnts[-1], headLocArray[i])
            mc.delete(todelete)

        # parent the head space to their respective parts
        mc.parent(headLocArray[0], fkJnts[-1])
        mc.parent(headLocArray[1], jntIKShoulder)
        mc.parent(headLocArray[2], grpTorsoDNT)
        mc.parent(headLocArray[3], ctrlRootTrans)

        headFollowOrntConstr = mc.orientConstraint(headLocArray, ctrlHead)[0]
        headFollowPntConstr = mc.pointConstraint(headLocArray, ctrlHead)[0]

        headFollowRot = 'rotationSpace'
        headFollowTrans = 'translationSpace'
        mc.addAttr(ctrlHead, longName=headFollowRot, at="enum", enumName="Neck:Shoulders:upperBody:Root", k=True)
        mc.addAttr(ctrlHead, longName=headFollowTrans, at="enum", enumName="Neck:Shoulders:upperBody:Root", k=True)

        # grab the last 4 attributes
        headSpaceFollowOrnt = mc.listAttr(headFollowOrntConstr)[-4:]
        headSpaceFollowPnt = mc.listAttr(headFollowPntConstr)[-4:]
        for i in range(len(headSpaceFollowOrnt)):
            # set the driven key to 1 and the undriven keys to 0
            print("i: {0}".format(i))

            CRU.setDriverDrivenValues(ctrlHead, headFollowRot, headFollowOrntConstr, headSpaceFollowOrnt[i], i, 1)
            CRU.setDriverDrivenValues(ctrlHead, headFollowTrans, headFollowPntConstr, headSpaceFollowPnt[i], i, 1)
            for i2 in range(len(headSpaceFollowOrnt)):
                if i2 != i:
                    # need to have the second to last value be i, not i2
                    CRU.setDriverDrivenValues(ctrlHead, headFollowRot, headFollowOrntConstr, headSpaceFollowOrnt[i2], i,
                                              0)
                    CRU.setDriverDrivenValues(ctrlHead, headFollowTrans, headFollowPntConstr, headSpaceFollowPnt[i2], i,
                                              0)

        for i in range(len(headLocArray)):
            mc.setAttr("{0}.v".format(headLocArray[i]), False)

    def createNeckHeadCtrls(self, jntIKShoulder, grpJntSpine, checkboxSpine, *args):
        listCtrls = ["neck", "head", "jaw1"]
        headOffsetCtrls = []
        specVal = 0
        for i in range(len(self.jointArray)):
            val = str(self.jointArray[i])
            colourTU = 17

            if any(x in val for x in listCtrls):
                # if the neck, do the following
                if listCtrls[0] in val:
                    sizeCtrl = 10
                    orntVal = (0, 1, 0)
                    headOffsetCtrls.append(
                        CRU.createCTRLs(val, prnt=False, ornt=True, size=sizeCtrl, orientVal=orntVal, colour=colourTU))

                    child = mc.listRelatives(val, c=True)[0]
                    boneLength = mc.getAttr("{0}.ty".format(child))

                    mc.select(headOffsetCtrls[specVal][1] + ".cv[:]")
                    mc.move(boneLength * .2, z=True, r=True, os=True, wd=True)
                elif listCtrls[1] in val:
                    # if the head, do the following
                    sizeCtrl = 15
                    orntVal = (0, 1, 0)

                    boneLength = mc.getAttr("{0}End.ty".format(val))
                    headOffsetCtrls.append(
                        CRU.createCTRLs(val, prnt=False, ornt=True, size=sizeCtrl, orientVal=orntVal, colour=colourTU))
                    mc.select(headOffsetCtrls[specVal][1] + ".cv[:]")
                    mc.move(boneLength * .65, y=True, r=True)

                elif listCtrls[2] in val:
                    # if the jaw, do the following
                    sizeCtrl = 3
                    orntVal = (0, 1, 0)
                    # get the length of the bone
                    getBoneChild = mc.listRelatives(val, type="joint", ad=True)
                    boneLength = mc.getAttr("{0}.ty".format(getBoneChild[0]))
                    boneLength2 = mc.getAttr("{0}.ty".format(getBoneChild[1]))
                    headOffsetCtrls.append(
                        CRU.createCTRLs(val, prnt=False, ornt=True, pnt=True, size=sizeCtrl, orientVal=orntVal,
                                        colour=colourTU))
                    # move the CVs into place
                    mc.select(headOffsetCtrls[specVal][1] + ".cv[:]")
                    mc.move(0, -boneLength2 * 2, boneLength * 1.1, r=True)

                specVal += 1

        mc.parent(headOffsetCtrls[1][0], headOffsetCtrls[0][1])
        mc.parent(headOffsetCtrls[2][0], headOffsetCtrls[1][1])
        mc.parent(headOffsetCtrls[3][0], headOffsetCtrls[2][1])

        # CTRL_neck1 point constrains JNT_neck1
        # parent OFFSET_CTRL_neck1 under CTRL_IK_chest
        if checkboxSpine:
            mc.pointConstraint(headOffsetCtrls[0][1], self.jointArray[0])
            noUnicode = str(self.jointArray[0])
            grpHead = mc.group(n="GRP_JNT_head", w=True, em=True)
            mc.parent(noUnicode, grpHead)

            mc.parent(headOffsetCtrls[0][0], jntIKShoulder)

            # was originally GRP_JNT_torso, but changed to GRP_rig_torso
            grpTorso = mc.group(n="GRP_rig_torso", w=True, em=True)
            mc.parent(grpHead, grpJntSpine, grpTorso)

        return headOffsetCtrls

    def createEyeControls(self, eyeArray, headOffsetCtrls, *args):
        # Create eye control
        eyeCtrlArray = []

        eyeOffsetArray = []

        radiusBase = mc.getAttr("{0}.ty".format(self.jointEndArray[-1]))

        for i in range(len(eyeArray)):
            # takes the eye joints, creates a corresponding locator
            eyeName = str(eyeArray[i]).replace("JNT_", "")
            eyeCtrlArray.append(mc.spaceLocator(p=(0, 0, 0), name="CTRL_" + eyeName)[0])

            mc.setAttr('{0}.overrideEnabled'.format(eyeCtrlArray[i]), 1)
            if "_l_" in eyeCtrlArray[i]:
                mc.setAttr("{0}.overrideColor".format(eyeCtrlArray[i]), 14)
            elif "_r_" in eyeCtrlArray[i]:
                mc.setAttr("{0}.overrideColor".format(eyeCtrlArray[i]), 13)

            # groups them at the creation point
            autoGrp = mc.group(eyeCtrlArray[i], name="AUTO_" + eyeName)
            eyeOffsetArray.append(mc.group(autoGrp, name="OFFSET_" + eyeName))

            # moves the eye into posiiton
            todelete = mc.parentConstraint(eyeArray[i], eyeOffsetArray[i], mo=False)
            mc.delete(todelete)

            mc.move(radiusBase * 2, eyeOffsetArray[i], z=True, r=True)

        # Create the eyes control
        eyesCtrlName = "CTRL_eyes"
        eyesCtrl = mc.circle(nr=(0, 1, 0), r=radiusBase * .75, n=eyesCtrlName, degree=1, sections=4)[0]

        mc.setAttr("{0}.ry".format(eyesCtrl), 45)
        mc.makeIdentity(eyesCtrl, a=True)  # freeze transform
        mc.setAttr("{0}.sx".format(eyesCtrl), 1.5)
        mc.makeIdentity(eyesCtrl, a=True)  # freeze transform
        mc.setAttr("{0}.rx".format(eyesCtrl), 90)
        mc.makeIdentity(eyesCtrl, a=True)  # freeze transform

        eyesAuto = mc.group(eyesCtrl, n="AUTO_" + eyesCtrlName)

        eyesOffset = mc.group(eyesAuto, n="OFFSET_" + eyesCtrlName)

        todelete = mc.pointConstraint(eyeCtrlArray, eyesOffset)
        mc.delete(todelete)

        mc.parent(eyeOffsetArray, eyesCtrl)

        aimArray = []
        for i in range(len(eyeArray)):
            aimArray.append(mc.aimConstraint(eyeCtrlArray[i], eyeArray[i], aim=[0, 0, 1]))

        # create the eye follow settings
        eyesFollowLocArray = []

        eyesFollowLocArray.append(mc.spaceLocator(p=(0, 0, 0), name="LOC_eyesHeadFollow")[0])
        eyesFollowLocArray.append(mc.spaceLocator(p=(0, 0, 0), name="LOC_eyesWorldFollow")[0])

        for i in range(len(eyesFollowLocArray)):
            todelete = mc.parentConstraint(eyesCtrl, eyesFollowLocArray[i], mo=False)
            mc.delete(todelete)
        headCtrl = ""
        for i in range(len(headOffsetCtrls)):
            if "head" in headOffsetCtrls[i][1]:
                headCtrl = headOffsetCtrls[i][1]

        mc.parent(eyesFollowLocArray[0], headCtrl)

        eyesCtrlPrntConst = mc.parentConstraint(eyesFollowLocArray[0], eyesFollowLocArray[1], eyesOffset)[0]

        mc.addAttr(eyesCtrl, longName='eyesFollow', at="enum", enumName="Head:World", k=True)

        # The last two attributes would be the relevant head and eye controls
        eyesFollow = mc.listAttr(eyesCtrlPrntConst)[-2:]

        CRU.setDriverDrivenValues(eyesCtrl, "eyesFollow", eyesCtrlPrntConst, eyesFollow[0], 0, 1)
        CRU.setDriverDrivenValues(eyesCtrl, "eyesFollow", eyesCtrlPrntConst, eyesFollow[0], 1, 0)

        CRU.setDriverDrivenValues(eyesCtrl, "eyesFollow", eyesCtrlPrntConst, eyesFollow[1], 0, 0)
        CRU.setDriverDrivenValues(eyesCtrl, "eyesFollow", eyesCtrlPrntConst, eyesFollow[1], 1, 1)

        for i in range(len(eyesFollowLocArray)):
            mc.setAttr("{0}.v".format(eyesFollowLocArray[i]), False)

        grpWorldFollow = mc.group(n="GRP_LOC_follow", w=True, em=True)

        mc.parent(eyesFollowLocArray[1], grpWorldFollow)

        return headCtrl, eyeCtrlArray, eyesCtrl, grpWorldFollow

    def neckCleanUp(self, jntArray, fkJnts, ikNeckBase, ikNeckEnd, hdlNeck, crvNeck, grpHead, grpNeckFK, ctrlHead, *args):

        # Make the objects invisible
        mc.setAttr("{0}.v".format(ikNeckBase), False)
        mc.setAttr("{0}.v".format(ikNeckEnd), False)
        mc.setAttr("{0}.v".format(hdlNeck), False)
        mc.setAttr("{0}.v".format(crvNeck), False)
        # mc.setAttr("{0}.v".format(jntArray[0]), False)

        grpHeadDNT = "GRP_DO_NOT_TOUCH_HEAD"
        mc.group(n=grpHeadDNT, w=True, em=True)
        parentFK = mc.listRelatives(jntArray[0], p=True)[0]
        mc.parent(grpHeadDNT, parentFK)
        mc.parent(jntArray[0], ikNeckBase, ikNeckEnd, hdlNeck, crvNeck, grpHeadDNT)

        # hide scale on ctrlHead
        CRU.lockHideCtrls(ctrlHead, scale=True)

        # hide translate, scale, radius on FK Control
        CRU.lockHideCtrls(fkJnts[0], scale=True, translate=True)
        CRU.lockHideCtrls(fkJnts[0], theVals=["radi"], channelBox=False, toLock=True, toHide=False)

        CRU.lockHideCtrls(grpHead, translate=True, rotate=True, scale=True, visible=True)
        CRU.lockHideCtrls(grpNeckFK, translate=True, rotate=True, scale=True, visible=True)
        CRU.lockHideCtrls(ikNeckEnd, translate=True, rotate=True, scale=True, visible=True)

        CRU.layerEdit(jntArray, bndLayer=True, noRecurse=True)

    def tgpMakeBC(self, *args):
        checkGeo = mc.checkBox("selGeo_cb", q=True, v=True)
        checkboxSpine = mc.checkBox("selSpineEnd_cb", q=True, v=True)

        # We want to be able to have space switching regardless
        jntIKShoulder = mc.textFieldButtonGrp("jntIKShoulderLoad_tf", q=True, text=True)
        grpTorsoDNT = mc.textFieldButtonGrp("grpTorsoDNT_tfbg", q=True, text=True)

        ctrlRootTrans = mc.textFieldButtonGrp("rootTrans_tfbg", q=True, text=True)

        self.jntNames = mc.textFieldButtonGrp("jointLoad_tfbg", q=True, text=True)

        # make sure the selections are not empty
        checkList = [self.jntNames]

        # eyeArray = [x for x in self.jointArray if "eye" in x]

        # gets us most of the geos
        jntArrayNoEnd = [x for x in self.jointArray if "End" not in x]
        jntArray = self.jointArrayNeck
        jntEnd = jntArray[-1]
        print(jntArray)

        jntArrayLen = len(jntArray)

        noUnicode = str(jntEnd)
        jntEndSize = mc.getAttr('{0}.radius'.format(noUnicode))

        if ((checkList[0] == "")):
            mc.warning("You are missing a selection!")
            return
        else:
            if "neck1" not in checkList[0]:
                mc.warning("Make the first selection the root neck joint")
                return

            CRU.createLocatorToDelete()
            hdlNeck, effNeck, crvNeck = self.createIKSpline(jntArray[0], jntEnd, "neck")
            ikNeckBase, ikNeckEnd, neckIKs = self.createNeckIK(jntArray, jntEnd, jntEndSize, crvNeck)

            self.addIkTwist(hdlNeck, ikNeckBase, ikNeckEnd)

            # creates the head control
            ctrlHead = self.createHeadCtrls(ikNeckEnd)

            # creates the FK and FK control
            ctrlFK, fkJnts = self.createFKJntAndCtrls(jntArray, jntEnd, jntEndSize)

            # creates the group head and
            grpHead = self.createGroupHead(ctrlHead, ikNeckEnd, fkJnts)

            neckInfo, neckStretchNameDiv = self.addStretch(jntArray, crvNeck, jntArrayLen, "neck", ctrlRootTrans, )
            fkJntsStart = fkJnts[0]
            jntArrayStart = jntArray[0]
            self.parentRootTransform(ctrlRootTrans, crvNeck, hdlNeck, ikNeckBase, ikNeckEnd, grpHead, fkJntsStart,
                                     jntArrayStart, )

            # Space Switching Shoulders
            # In case we want to attach it to the body
            locConstNeckShoulder, grpNeckFK = self.createNeckShoulderLoc(checkboxSpine, jntIKShoulder, ikNeckBase,
                                                                         fkJnts, )

            self.createSpaceSwitching(ctrlHead, jntIKShoulder, ctrlRootTrans, fkJnts, grpTorsoDNT)

            self.neckCleanUp(jntArray, fkJnts, ikNeckBase, ikNeckEnd, hdlNeck, crvNeck, grpHead, grpNeckFK, ctrlHead)
            return

            if checkGeo:
                CRU.tgpSetGeo(jntArrayNoEnd, setLayer=True)
