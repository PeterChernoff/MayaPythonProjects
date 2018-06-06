# coding=utf-8
'''
Created on May 30, 2014
for Tin Girl Book and game project

@author: Eyal Assaf
'''
import maya.cmds as mc
# import tgpUtils as ut
from functools import partial
import tgpBaseUI
from tgpBaseUI import BaseUI as UI

reload(tgpBaseUI)

import pcCreateRig00AUtilities

import pcCreateRigAlt00AUtilities

reload(pcCreateRigAlt00AUtilities)
from pcCreateRigAlt00AUtilities import pcCreateRigUtilities as CRU


class pcCreateRigAlt05Arms(UI):
    def __init__(self):
        self.valLeft = "l_"
        self.valRight = "r_"

        self.window = "bcWindow"
        self.title = "pcRigArms"
        self.winSize = (500, 500)

        self.createUI()

    def createCustom(self, *args):
        # selection type

        mc.rowColumnLayout(nc=2, cw=[(1, 500), (2, 500)], cs=[1, 5], rs=[1, 3])

        mc.text(l="Select The Arm Root: ")
        mc.text(l="")
        mc.separator(st="in", h=17, w=500)
        mc.setParent("..")
        mc.rowColumnLayout(nc=3, cw=[(1, 125), (2, 150), (3, 150)], cs=[1, 5], rs=[1, 3],
                           cal=([1, "left"], [2, "left"], [3, "left"],))

        mc.text(l="Mirror Arm As Well?")

        mc.radioButtonGrp("selArmMirrorType_rbg", la2=["No", "Yes"], nrb=2, sl=2, cw2=[50, 300], )
        mc.text(l="")
        mc.setParent("..")

        mc.rowColumnLayout(nc=3, cw=[(1, 150), (2, 150), (3, 150)], cs=[1, 5], rs=[1, 3],
                           cal=([1, "left"], [2, "left"]))
        mc.checkBox("selSpecialStretch_cb", l="Toggle Stretch for \nShoulders and IK Arms", en=True, v=True)
        mc.checkBox("selAddIKFKSwitching_cb", l="Include IK FK\nSwitching Setup", en=True, v=True)
        mc.checkBox("selStretchSpineToggle_cb", l="Using Spine\nStretch Toggle", en=True, v=True)
        mc.setParent("..")
        mc.separator(st="in", h=17, w=500)

        mc.rowColumnLayout(nc=3, cw=[(1, 100), (2, 200), (3, 150)], cs=[1, 5], rs=[1, 3],
                           cal=([1, "left"], [2, "left"], [3, "left"],))
        mc.text(l="Initial Limb: ")
        mc.radioButtonGrp("selArmType_rbg", la2=["Left", "Right"], nrb=2, sl=1, cw2=[50, 50], )
        mc.setParent("..")
        mc.separator(st="in", h=17, w=500)

        # sources
        mc.rowColumnLayout(nc=2, cw=[(1, 100), (2, 380)], cs=[1, 5], rs=[1, 3])

        mc.text(bgc=(0.85, 0.65, 0.25), l="Arm Joint: ")
        mc.textFieldButtonGrp("jointArmsLoad_tfbg", cw=(1, 322), bl="  Load  ", tx="JNT_BND_l_upperArm")

        mc.text(bgc=(0.85, 0.65, 0.25), l="Shoulder Joint: ")
        mc.textFieldButtonGrp("jointShoulderJntLoad_tfbg", cw=(1, 322), bl="  Load  ", tx="JNT_BND_l_shoulderBase")

        mc.text(bgc=(0.85, 0.65, 0.25), l="Shoulder IK Joint: ")
        mc.textFieldButtonGrp("jntIKShoulderLoad_tf", cw=(1, 322), bl="  Load  ", tx="JNT_IK_shoulder")

        mc.text(bgc=(0.85, 0.65, 0.25), l="Torso \nDo Not Touch: ")
        mc.textFieldButtonGrp("grpTorsoDNTLoad_tf", cw=(1, 322), bl="  Load  ", tx="GRP_DO_NOT_TOUCH_torso")

        mc.setParent("..")

        mc.separator(st="in", h=17, w=500)
        mc.rowColumnLayout(nc=2, cw=[(1, 100), (2, 380)], cs=[1, 5], rs=[1, 3])

        mc.text(bgc=(0.85, 0.65, 0.25), l="Root Control: ")
        mc.textFieldButtonGrp("rootTrans_tfbg", cw=(1, 322), bl="  Load  ", tx="CTRL_rootTransform")

        mc.text(bgc=(0.85, 0.65, 0.25), l="Stretchable Head\nShoulder Group: ")
        mc.textFieldButtonGrp("grpheadShoulders_tfbg", cw=(1, 322), bl="  Load  ", tx="GRP_head_shoulders")

        mc.setParent("..")

        mc.separator(st="in", h=17, w=500)

        mc.rowColumnLayout(nc=2, cw=[(1, 120), (2, 370)], cs=[1, 5], rs=[1, 3])
        mc.checkBox("selGeo_cb", l="Affect Geometry", en=True, v=True)
        mc.setParent("..")

        # load buttons
        mc.textFieldButtonGrp("jointArmsLoad_tfbg", e=True, bc=self.loadSrc1Btn)
        mc.textFieldButtonGrp("jointShoulderJntLoad_tfbg", e=True, bc=self.loadSrc2Btn)
        mc.textFieldButtonGrp("jntIKShoulderLoad_tf", e=True, bc=self.loadSrc3Btn)
        mc.textFieldButtonGrp("grpTorsoDNTLoad_tf", e=True, bc=self.loadSrc4Btn)
        mc.textFieldButtonGrp("rootTrans_tfbg", e=True, bc=self.loadSrc5Btn)
        mc.textFieldButtonGrp("grpheadShoulders_tfbg", e=True, bc=self.loadSrc6Btn)

        self.selLoad = []
        self.jointArray = []
        mc.showWindow(self.window)

    def createButtonCmd(self, *args):
        self.tgpMakeBC()

    def loadSrc1Btn(self):
        self.selSrc1 = self.tgpLoadJntsBtn("jointArmsLoad_tfbg", "joint", "Root Upper Arm Joint",
                                           ["JNT", "BND", "upperArm"])
        print(self.selSrc1)

    def loadSrc2Btn(self):
        self.selSrc2 = CRU.tgpLoadTxBtn("jointShoulderJntLoad_tfbg", "joint", "Root Shoulder Joint",
                                         ["JNT", "BND", "shoulder"])
        print(self.selSrc2)

    def loadSrc3Btn(self):
        self.selSrc3 = CRU.tgpLoadTxBtn("jntIKShoulderLoad_tf", "joint", "IK Shoulder Joint",
                                         ["JNT", "_IK_", "shoulder"])
        print(self.selSrc3)

    def loadSrc4Btn(self):
        self.selSrc4 = CRU.tgpLoadTxBtn("grpTorsoDNTLoad_tf", "transform", "DO NOT TOUCH Torso Group",
                                         ["GRP", "DO_NOT_TOUCH", "torso"],
                                         "Group")
        print(self.selSrc4)

    def loadSrc5Btn(self):
        self.selSrc5 = CRU.tgpLoadTxBtn("rootTrans_tfbg", "nurbsCurve", "Root Control", ["CTRL", "rootTransform"],
                                         "control")
        print(self.selSrc5)

    def loadSrc6Btn(self):
        self.selSrc6 = CRU.tgpLoadTxBtn("grpheadShoulders_tfbg", "transform", "Head Shoulders Group",
                                         ["GRP", "head", "shoulders"],
                                         "group")
        print(self.selSrc6)

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
            returner = self.tgpGetJnts(selName, loadBtn, objectType, objectDesc, keywords, objectNickname)

            if returner is None:
                return None

        return self.jointArray

    def tgpGetJnts(self, selName, loadBtn, objectType, objectDesc, keywords, objectNickname=None, ):
        if objectNickname is None:
            objectNickname = objectType

        if CRU.checkObjectType(selName) != objectType:
            mc.warning("{0} should be a {1}".format(objectDesc, objectNickname))
            return

        if not all(word.lower() in selName.lower() for word in keywords):
            mc.warning("That is the wrong {0}. Select the {1}".format(objectNickname, objectDesc))
            return

        mc.textFieldButtonGrp(loadBtn, e=True, tx=selName)

        # get the children joints
        self.parent = selName
        self.child = mc.listRelatives(selName, ad=True, type="joint")
        # collect the joints in an array
        self.jointArray = [self.parent]
        # reverse the order of the children joints
        self.child.reverse()

        # add to the current list
        self.jointArray.extend(self.child)

        self.jointRoot = selName
        return self.jointArray

    def createSettings(self, jntArmArray, isLeft, name, colourTU, fkJnts, ikJnts, bndJnts, ctrlIKArm, *args):
        ctrlArmSettings = CRU.createNailNoOffset(jntArmArray[-2], isLeft, name, bodySize=15, headSize=2,
                                                 colourTU=colourTU,
                                                 pnt=True)

        grpSettings = "GRP_settings"
        if not mc.objExists(grpSettings):
            mc.group(n=grpSettings, w=True, em=True)
        mc.parent(ctrlArmSettings, grpSettings)
        CRU.layerEdit(grpSettings, newLayerName="settings_LYR", colourTU=CRU.clrSettings)

        # creates the FKIK blend control

        fkikBlendName = "fkik_blend"
        fkikBlendNiceName = "FK / IK Blend"
        # NOTE: we make the default value 0.5 for testing purposes
        mc.addAttr(ctrlArmSettings, longName=fkikBlendName, niceName=fkikBlendNiceName, at="float", k=True, min=0,
                   max=1, dv=1)
        mc.setAttr("{0}.{1}".format(ctrlArmSettings, fkikBlendName), 0)

        CRU.makeBlendBasic(fkJnts, ikJnts, bndJnts, ctrlArmSettings, fkikBlendName, rotate=True, translate=True)
        # connect the visibility of the controllers
        fkVis = "FK_visibility"
        ikVis = "IK_visibility"

        mc.addAttr(ctrlArmSettings, longName=fkVis, at="bool", k=True)
        mc.addAttr(ctrlArmSettings, longName=ikVis, at="bool", k=True)

        mc.connectAttr("{0}.{1}".format(ctrlArmSettings, fkVis), "{0}.visibility".format(fkJnts[0]))

        mc.connectAttr("{0}.{1}".format(ctrlArmSettings, ikVis), "{0}.visibility".format(ikJnts[0]))
        ####
        # we reroute this in a later part, might as well skip it here.
        # mc.connectAttr("{0}.{1}".format(ctrlArmSettings, ikVis), "{0}.visibility".format(ctrlIKArm))
        ####
        mc.setAttr("{0}.{1}".format(ctrlArmSettings, fkVis), True)
        mc.setAttr("{0}.{1}".format(ctrlArmSettings, ikVis), True)

        return ctrlArmSettings, fkikBlendName, fkVis, ikVis

    def bindArmTwists(self, twistJntsArrayOfArrays, leftRight, ikArms, *args):

        bindJntTwistStart = "JNT_{0}arm_bindStart".format(leftRight)
        bindJntTwistMid = "JNT_{0}arm_bindMid".format(leftRight)
        bindJntTwistEnd = "JNT_{0}arm_bindEnd".format(leftRight)
        cycleVis = []
        cycleVis.append(bindJntTwistStart, )
        cycleVis.append(bindJntTwistMid)
        cycleVis.append(bindJntTwistEnd)

        mc.duplicate(twistJntsArrayOfArrays[0][0], n=bindJntTwistStart, po=True)
        if mc.listRelatives(bindJntTwistStart, p=True) is not None:
            mc.parent(bindJntTwistStart, w=True)

        mc.duplicate(twistJntsArrayOfArrays[0][-1], n=bindJntTwistMid, po=True)
        if mc.listRelatives(bindJntTwistMid, p=True) is not None:
            mc.parent(bindJntTwistMid, w=True)

        mc.duplicate(twistJntsArrayOfArrays[-1][-1], n=bindJntTwistEnd, po=True)
        if mc.listRelatives(bindJntTwistEnd, p=True) is not None:
            mc.parent(bindJntTwistEnd, w=True)

        jntRad = mc.getAttr("{0}.radius".format(bindJntTwistStart))
        mc.setAttr("{0}.radius".format(bindJntTwistStart), 1.5 * jntRad)
        mc.setAttr("{0}.radius".format(bindJntTwistMid), 1.5 * jntRad)
        mc.setAttr("{0}.radius".format(bindJntTwistEnd), 1.5 * jntRad)

        ##########
        # bind the curves to the twists
        crvUpperArm = ikArms[0][2]
        crvLowerArm = ikArms[1][2]

        self.bindTwistControls(crvUpperArm, bindJntTwistStart, bindJntTwistMid)
        self.bindTwistControls(crvLowerArm, bindJntTwistMid, bindJntTwistEnd)
        ##########
        # activate the advanced Twist Control

        hdlUpperArm = ikArms[0][0]
        hdlLowerArm = ikArms[1][0]

        # the right upperArm seemd to do better with closestZ instead of negative Z
        # alternatively, using Positive Y works
        if leftRight == self.valLeft:
            # this may need tweaking depending on the model
            uArmUV = [0, -1, 0]
            uArmUV2 = [0, -1, 0]

            lArmUV = [0, 0, 1]
            lArmUV2 = [0, 0, 1]
        else:
            uArmUV = [0, 1, 0]
            uArmUV2 = [0, -1, 0]

            lArmUV = [0, 0, -1]
            lArmUV2 = [0, 0, -1]

        self.advancedTwistControls(hdlUpperArm, bindJntTwistStart, bindJntTwistMid, uArmUV, uArmUV2, 1)
        self.advancedTwistControls(hdlLowerArm, bindJntTwistMid, bindJntTwistEnd, lArmUV, lArmUV2, 4)
        ##########

        for i in range(len(cycleVis)):
            mc.setAttr("{0}.visibility".format(cycleVis[i]), False)

        return bindJntTwistStart, bindJntTwistMid, bindJntTwistEnd

    def bindTwistControls(self, crvToUse, startJnt, endJnt):
        mc.select(crvToUse, endJnt, startJnt)
        skinName = crvToUse.replace("CRV_", "")
        skinName = skinName + "_skinCluster"

        # mc.skinCluster (ikHip, ikShoulder, crvSpine, sm=0, nw = 1)

        scls = mc.skinCluster(endJnt, startJnt, crvToUse, name=skinName, toSelectedBones=True,
                              bindMethod=0, skinMethod=0, nw=1, maximumInfluences=2)[0]

    def advancedTwistControls(self, hdlArm, startJnt, endJnt, armUV, armUV2, uAxis=None):
        # this one may need a bit of tweaking manually
        if uAxis is None:
            uAxis = 4
        mc.setAttr('{0}.dTwistControlEnable'.format(hdlArm), True)

        # forward to positive x
        mc.setAttr('{0}.dForwardAxis'.format(hdlArm), 0)

        # World Up Type to Object Rotation Up (Start/End)
        mc.setAttr('{0}.dWorldUpType'.format(hdlArm), 4)

        # up to positive Y / negative z
        mc.setAttr('{0}.dWorldUpAxis'.format(hdlArm), uAxis)

        # Up Vector and Up Vector 2 to 0, 0, 1
        # they may need to be opposite values on the left/right

        mc.setAttr('{0}.dWorldUpVectorX'.format(hdlArm), armUV[0])
        mc.setAttr('{0}.dWorldUpVectorY'.format(hdlArm), armUV[1])
        mc.setAttr('{0}.dWorldUpVectorZ'.format(hdlArm), armUV[2])

        mc.setAttr('{0}.dWorldUpVectorEndX'.format(hdlArm), armUV2[0])
        mc.setAttr('{0}.dWorldUpVectorEndY'.format(hdlArm), armUV2[1])
        mc.setAttr('{0}.dWorldUpVectorEndZ'.format(hdlArm), armUV2[2])

        # connects the joints to the right place
        mc.connectAttr(startJnt + ".worldMatrix[0]", hdlArm + ".dWorldUpMatrix")
        mc.connectAttr(endJnt + ".worldMatrix[0]", hdlArm + ".dWorldUpMatrixEnd")

        mc.setAttr('{0}.dTwistValueType'.format(hdlArm), 0)

    def makeFKStretchJnt(self, fkJnts, limbName, add=True, *args):

        ctrlFKLengthKeyArray = []
        endVal = len(limbName) * -1
        for i in range(len(fkJnts)):
            fkJnt = fkJnts[i]
            if limbName in fkJnt[endVal:]:
                drivenAttr = "translateX"
                limbChild = mc.listRelatives(fkJnt, typ="joint")[0]
                legLen = mc.getAttr("{0}.{1}".format(limbChild, drivenAttr))
                length = "length"
                driverValue = 1
                if add:
                    mc.addAttr(fkJnt, longName=length, at="float", k=True, min=0, dv=1)
                CRU.setDriverDrivenValues(fkJnt, length, limbChild, drivenAttr, drivenValue=legLen,
                                          driverValue=driverValue,
                                          modifyBoth="spline")
                CRU.setDriverDrivenValues(fkJnt, length, limbChild, drivenAttr, drivenValue=0, driverValue=0,
                                          modifyBoth="spline")
                fkKey = "{0}_{1}".format(limbChild, drivenAttr)
                ctrlFKLengthKeyArray.append(fkKey)
                mc.selectKey(cl=True)
                mc.selectKey(limbChild, add=True, k=driverValue, attribute=drivenAttr)
                mc.setInfinity(poi='linear')

        return ctrlFKLengthKeyArray

    def makeFKStretchTwistsBak(self, bndJnt, crvArm, twistJnts):
        nameEdit = bndJnt.replace("JNT_BND_", "")

        crvInfo = nameEdit + "Info"
        armNrmlzDiv = nameEdit + "_normalize_DIV"
        mc.shadingNode("curveInfo", n=crvInfo, au=True)
        mc.shadingNode("multiplyDivide", n=armNrmlzDiv, au=True)

        crvArmShape = mc.listRelatives(crvArm, s=True)[0]
        mc.connectAttr("{0}.worldSpace".format(crvArmShape), "{1}.inputCurve".format(crvArmShape, crvInfo))

        mc.setAttr("{0}.operation".format(armNrmlzDiv), 2)
        mc.connectAttr("{0}.arcLength".format(crvInfo), "{0}.input1X".format(armNrmlzDiv))

        armLen = mc.getAttr("{0}.tx".format(mc.listRelatives(bndJnt, type="joint")[0]))  # get the joint child
        # divide arm length by its base length
        mc.setAttr("{0}.input2X".format(armNrmlzDiv), armLen)

        # connect to the segments' scaleX
        for i in range(len(twistJnts) - 1):
            mc.connectAttr("{0}.outputX".format(armNrmlzDiv), "{0}.scaleX".format(twistJnts[i]))

        return crvInfo, armNrmlzDiv

    def makeBndStretchTwists(self, bndJnt, crvArm, twistJnts, leftRight):
        if leftRight == self.valLeft:
            m = 1
        else:
            m = -1
        nameEdit = bndJnt.replace("JNT_BND_", "")

        crvInfo = nameEdit + "Info"
        armNrmlzDiv = nameEdit + "_normalize_DIV"
        mc.shadingNode("curveInfo", n=crvInfo, au=True)
        mc.shadingNode("multiplyDivide", n=armNrmlzDiv, au=True)

        crvArmShape = mc.listRelatives(crvArm, s=True)[0]
        mc.connectAttr("{0}.worldSpace".format(crvArmShape), "{1}.inputCurve".format(crvArmShape, crvInfo))

        mc.setAttr("{0}.operation".format(armNrmlzDiv), 2)
        mc.connectAttr("{0}.arcLength".format(crvInfo), "{0}.input1X".format(armNrmlzDiv))

        armLen = mc.getAttr("{0}.tx".format(mc.listRelatives(bndJnt, type="joint")[0])) * m  # get the joint child
        # divide arm length by its base length
        mc.setAttr("{0}.input2X".format(armNrmlzDiv), armLen)

        # connect to the segments' scaleX
        for i in range(len(twistJnts) - 1):
            mc.connectAttr("{0}.outputX".format(armNrmlzDiv), "{0}.scaleX".format(twistJnts[i]))

        return crvInfo, armNrmlzDiv

    def makeIKHandle(self, ctrlIKArm, ikJnts, leftRight):
        mc.rotate(0, 5, 0, ikJnts[1], r=True)
        mc.joint(ikJnts[1], e=True, spa=True)  # set the preferred angle

        mc.rotate(0, -5, 0, ikJnts[1], r=True)

        ikSolver = "ikRPsolver"
        ikSuffix = "arm"
        ikArms = CRU.createIKVal(ikJnts[0], ikJnts[-2], leftRight, ikSuffix, ikSolver)  # create the IK arms

        ikSolver = "ikSCsolver"
        ikSuffix = "hand"
        ikHands = CRU.createIKVal(ikJnts[-2], ikJnts[-1], leftRight, ikSuffix, ikSolver)  # create the IK hand

        mc.parent(ikArms[0], ikHands[0], ctrlIKArm)

        # mc.nodePreset(save=(ctrlIKArm, "smithers"))

        return ikArms, ikHands

    def makeIKStretch(self, bindJntTwistStart, bindJntTwistEnd, ikJnts, ctrlIKArm, leftRight):

        if leftRight == self.valLeft:
            # need to make adjustments for the values making a mirror
            m = 1
        else:
            m = -1

        locIKDistStart = "LOC_{0}arm_IK_lengthStart".format(leftRight)
        locIKDistEnd = "LOC_{0}arm_IK_lengthEnd".format(leftRight)
        distIKLen = "DIST_{0}arm_IK_length".format(leftRight)
        cycleVis = []
        cycleVis.append(locIKDistStart, )
        cycleVis.append(locIKDistEnd)
        cycleVis.append(distIKLen)

        mc.spaceLocator(p=(0, 0, 0), name=locIKDistStart)
        mc.spaceLocator(p=(0, 0, 0), name=locIKDistEnd)

        todelete = mc.pointConstraint(bindJntTwistStart, locIKDistStart)
        mc.delete(todelete)
        todelete1 = mc.pointConstraint(bindJntTwistEnd, locIKDistEnd)
        mc.delete(todelete1)

        distIKLenShape = CRU.createDistanceDimensionNode(locIKDistStart, locIKDistEnd, distIKLen)

        mc.parent(locIKDistEnd, ctrlIKArm)
        driverAttr = "distance"
        driverLen = mc.getAttr("{0}.{1}".format(distIKLenShape, driverAttr)) * m

        ikLowerArm = ikJnts[1]
        ikJntHand = ikJnts[-2]
        upperLimbLen = mc.getAttr("{0}.translateX".format(ikLowerArm))
        lowerLimbLen = mc.getAttr("{0}.translateX".format(ikJntHand))
        sumLegLen = (upperLimbLen + lowerLimbLen) * m

        drivenAttr = "translateX"

        ctrlIKLengthKeyArray = []

        # uses the total length to drive the length of the upper leg and  extrapolates it to infinity
        CRU.setDriverDrivenValues(distIKLenShape, driverAttr, ikLowerArm, drivenAttr, sumLegLen, upperLimbLen,
                                  modifyBoth="spline")
        CRU.setDriverDrivenValues(distIKLenShape, driverAttr, ikLowerArm, drivenAttr, sumLegLen * 2, upperLimbLen * 2,
                                  modifyBoth="spline")
        mc.selectKey(cl=True)
        mc.selectKey(ikJnts[1], add=True, k=sumLegLen * 2, attribute=drivenAttr)
        mc.setInfinity(poi='cycleRelative')
        ctrlIKLengthKeyArray.append("{0}_{1}".format(ikJnts[1], drivenAttr))

        # uses the total length to drive the length of the lower leg and  extrapolates it to infinity
        CRU.setDriverDrivenValues(distIKLenShape, driverAttr, ikJntHand, drivenAttr, sumLegLen, lowerLimbLen,
                                  modifyBoth="spline")
        CRU.setDriverDrivenValues(distIKLenShape, driverAttr, ikJntHand, drivenAttr, sumLegLen * 2, lowerLimbLen * 2,
                                  modifyBoth="spline")

        mc.selectKey(cl=True)
        mc.selectKey(ikJntHand, add=True, k=sumLegLen * 2, attribute=drivenAttr)
        mc.setInfinity(poi='cycleRelative')
        ctrlIKLengthKeyArray.append("{0}_{1}".format(ikJntHand, drivenAttr))
        for i in range(len(cycleVis)):
            mc.setAttr("{0}.visibility".format(cycleVis[i]), False)

        return locIKDistStart, locIKDistEnd, distIKLen, distIKLenShape, ctrlIKLengthKeyArray

    def makeElbowCtrl(self, leftRight, ikJnts, hdlArm, *args):
        if leftRight == self.valLeft:
            m = -1
        else:
            m = 1
        locElbow = "LOC_{0}elbow".format(leftRight)
        mc.spaceLocator(p=(0, 0, 0), name=locElbow)
        toDelete = mc.pointConstraint(ikJnts[1], locElbow)
        mc.delete(toDelete)
        armLength = mc.getAttr("{0}.tx".format(ikJnts[1]))
        mc.move(m * armLength / 2, locElbow, z=True, os=True)

        # polevector constrain
        mc.poleVectorConstraint(locElbow, hdlArm)

        # create a pyramid
        boxDimensionsLWH = [2, 2, -8]
        x = boxDimensionsLWH[0]
        y = boxDimensionsLWH[1]
        z = boxDimensionsLWH[2]

        toPass = [(0, 0, z),
                  (-x, y, 0), (-x, -y, 0), (0, 0, z),
                  (x, y, 0), (x, -y, 0), (0, 0, z),
                  (x, y, 0), (x, -y, 0), (-x, -y, 0), (-x, y, 0), (x, y, 0), ]
        ctrlElbow = "CTRL_{0}elbow".format(leftRight)

        try:
            ctrl = mc.curve(ctrlElbow, r=True, d=1, p=toPass, )
        except:
            ctrl = mc.curve(name=ctrlElbow, d=1, p=toPass, )
            # ctrl = mc.curve(name=ctrlName, p=toPass, d=1)
        todelete = mc.pointConstraint(locElbow, ctrlElbow)
        mc.delete(todelete)
        mc.makeIdentity(ctrlElbow, a=True)
        mc.parent(locElbow, ctrlElbow)

        mc.setAttr("{0}.visibility".format(locElbow), False)

        return locElbow, ctrlElbow

    def makeElbowSnap(self, ikJnts, ctrlIKArm, ctrlElbow, leftRight):
        cycleVis = []
        # create locators for distance nodes at the arm ik to the elbow
        locDistArmElbowStart = "LOC_{0}upperArm_to_elbow_lengthStart".format(leftRight)
        locDistArmElbowEnd = "LOC_{0}upperArm_to_elbow_lengthEnd".format(leftRight)
        distArmElbow = "DIST_{0}upperArm_to_elbow_length".format(leftRight)
        cycleVis.append(locDistArmElbowStart)
        cycleVis.append(locDistArmElbowEnd)
        cycleVis.append(distArmElbow)

        mc.spaceLocator(p=(0, 0, 0), name=locDistArmElbowStart)
        mc.spaceLocator(p=(0, 0, 0), name=locDistArmElbowEnd)

        CRU.constrainMove(ikJnts[0], locDistArmElbowStart, point=True)
        CRU.constrainMove(ctrlElbow, locDistArmElbowEnd, point=True)
        distArmElbowShape = CRU.createDistanceDimensionNode(locDistArmElbowStart, locDistArmElbowEnd, distArmElbow)

        ##########

        # create locators for distance nodes at the elbow control to the hand control
        locDistElbowHandStart = "LOC_{0}elbow_to_hand_lengthStart".format(leftRight)
        locDistElbowHandEnd = "LOC_{0}elbow_to_hand_lengthEnd".format(leftRight)
        distElbowHand = "DIST_{0}elbow_to_hand_length".format(leftRight)

        cycleVis.append(locDistElbowHandStart)
        cycleVis.append(locDistElbowHandEnd)
        cycleVis.append(distElbowHand)

        mc.spaceLocator(p=(0, 0, 0), name=locDistElbowHandStart)
        mc.spaceLocator(p=(0, 0, 0), name=locDistElbowHandEnd)

        CRU.constrainMove(ctrlElbow, locDistElbowHandStart, point=True)
        CRU.constrainMove(ctrlIKArm, locDistElbowHandEnd, point=True)
        distElbowHandShape = CRU.createDistanceDimensionNode(locDistElbowHandStart, locDistElbowHandEnd, distElbowHand)

        ##########
        # parent them appropriately
        mc.parent(locDistArmElbowEnd, ctrlElbow)
        mc.parent(locDistElbowHandStart, ctrlElbow)

        mc.parent(locDistElbowHandEnd, ctrlIKArm)

        ##########
        # Add elbow snap
        elbowSnapAttr = "elbowSnap"
        mc.addAttr(ctrlElbow, longName=elbowSnapAttr, at="float", k=True, min=0, max=1, dv=0)

        blndUpperArmStretchChoice = "{0}upperArm_stretchChoice".format(leftRight)
        mc.shadingNode("blendColors", au=True, name=blndUpperArmStretchChoice)

        mc.connectAttr("{0}.{1}".format(ctrlElbow, elbowSnapAttr), "{0}.blender".format(blndUpperArmStretchChoice))

        mc.connectAttr("{0}.distance".format(distArmElbowShape), "{0}.color1R".format(blndUpperArmStretchChoice))
        # put the animation output of the joint into the color2R
        mc.connectAttr("{0}_translateX.output".format(ikJnts[1]), "{0}.color2R".format(blndUpperArmStretchChoice))

        mc.connectAttr("{0}.outputR".format(blndUpperArmStretchChoice), "{0}.translateX".format(ikJnts[1]), f=True)

        blndLowerArmStretchChoice = "{0}lowerArm_stretchChoice".format(leftRight)
        mc.shadingNode("blendColors", au=True, name=blndLowerArmStretchChoice)

        mc.connectAttr("{0}.{1}".format(ctrlElbow, elbowSnapAttr), "{0}.blender".format(blndLowerArmStretchChoice))

        mc.connectAttr("{0}.distance".format(distElbowHandShape), "{0}.color1R".format(blndLowerArmStretchChoice))
        # put the animation output of the joint into the color2R
        mc.connectAttr("{0}_translateX.output".format(ikJnts[-2]), "{0}.color2R".format(blndLowerArmStretchChoice))

        mc.connectAttr("{0}.outputR".format(blndLowerArmStretchChoice), "{0}.translateX".format(ikJnts[-2]), f=True)

        ##########
        # hide the objects
        for i in range(len(cycleVis)):
            mc.setAttr("{0}.visibility".format(cycleVis[i]), False)

        return locDistArmElbowStart, locDistArmElbowEnd, distArmElbow, locDistElbowHandStart, \
               locDistElbowHandEnd, distElbowHand, distArmElbowShape, distElbowHandShape, \
               blndUpperArmStretchChoice, blndLowerArmStretchChoice

    def makeFKElbow(self, fkJnts, ctrlElbow):
        # duplicate the fk elbow
        fkJntsElbow = mc.duplicate(fkJnts[1], rc=True)

        mc.parent(fkJntsElbow[0], w=True)
        CRU.constrainMove(ctrlElbow, fkJntsElbow[0], point=True)
        for i in range(len(fkJntsElbow)):
            toRename = fkJntsElbow[i][:-1] + "Elbow"
            mc.rename(fkJntsElbow[i], toRename)
            fkJntsElbow[i] = toRename
        fkElbow = fkJntsElbow[0]
        # Parent under the left elbow control
        mc.parent(fkElbow, ctrlElbow)

        return fkJntsElbow, fkElbow

    def makeElbowFKIKSwitch(self, ctrlIKArm, ikJnts, fkJntsElbow, leftRight):
        ctrlIKArmKidsSetup = mc.listRelatives(ctrlIKArm, s=False)
        ctrlIKArmKids = []
        for i in range(len(ctrlIKArmKidsSetup)):
            # Add the non-shape children
            if not mc.objectType(ctrlIKArmKidsSetup[i], isType='nurbsCurve'):
                ctrlIKArmKids.append(ctrlIKArmKidsSetup[i])
        grpIKConstArm = "GRP_IKConst_{0}arm".format(leftRight)

        mc.group(n=grpIKConstArm, em=True, w=True)
        CRU.constrainMove(ikJnts[-2], grpIKConstArm, point=True)
        mc.parent(ctrlIKArmKids, grpIKConstArm)
        ##########
        # parent the grpIKConst to the control, then the FK Elbow hand joint
        prntTemp = mc.parentConstraint(ctrlIKArm, grpIKConstArm, w=0)[0]
        fkJntElbowHand = fkJntsElbow[-2]
        mc.parentConstraint(fkJntElbowHand, grpIKConstArm, mo=False)
        ##########
        # we are going to be doing some backtracking
        w0w1Attr = mc.listAttr(prntTemp)[-2:]
        rotVals = mc.getAttr("{0}.r".format(grpIKConstArm))[0]
        mc.setAttr("{0}.{1}".format(prntTemp, w0w1Attr[0]), 1)
        mc.setAttr("{0}.{1}".format(prntTemp, w0w1Attr[1]), 0)
        mc.delete(prntTemp)
        # unparent everything in grpIKConstArm and adjust the rotation
        mc.parent(ctrlIKArmKids, w=True)
        mc.setAttr("{0}.rx".format(grpIKConstArm), rotVals[0])
        mc.setAttr("{0}.ry".format(grpIKConstArm), rotVals[1])
        mc.setAttr("{0}.rz".format(grpIKConstArm), rotVals[2])

        # reparent what we unparented
        mc.parent(ctrlIKArmKids, grpIKConstArm)
        # we parent in this order because we do FK/IK. We can reverse this if we want FK to be 0
        grpIKConstArmConstraint = mc.parentConstraint(ctrlIKArm, grpIKConstArm, mo=True)[0]
        mc.parentConstraint(fkJntElbowHand, grpIKConstArm, mo=False)

        return grpIKConstArm, grpIKConstArmConstraint

    def makeElbowFKIKSwitchControl(self, ctrlElbow, grpIKConstArmConstraint, fkElbow, ctrlIKArm,
                                   ctrlArmSettings, ikVis,
                                   leftRight):

        # switch between on and off, and visibility on and off
        lNameAttr = "FKIK_lowerArmBlend"
        nName = "FK / IK Lower Arm Blend"
        mc.addAttr(ctrlElbow, ln=lNameAttr, nn=nName, min=0, max=1, attributeType="float", k=True, dv=1)

        self.tgpSetDriverSwitch2Vals(ctrlElbow, lNameAttr, grpIKConstArmConstraint, valsInOut="linear")

        # set visibility
        lNameAttrVis = "lowerArm_FKIK_visibility"
        nName = "Lower Arm FK / IK Visibility"
        mc.addAttr(ctrlElbow, ln=lNameAttrVis, nn=nName, attributeType="bool", k=True)

        tangentToUse = ["linear", "step"]
        visMin = 0.001

        mc.connectAttr("{0}.{1}".format(ctrlElbow, lNameAttrVis), "{0}.visibility".format(fkElbow))

        # set the FK to visible when not ctrlFKIK not 1 for arm attribute
        CRU.setVisibility(ctrlElbow, lNameAttr, ctrlElbow, lNameAttrVis, visMin, tangentToUse, True, True, False)

        # we can't just hide the IK Control so we need to make a group
        grpIKVisArm = "GRP_IK_vis_{0}arm".format(leftRight)

        mc.group(n=grpIKVisArm, em=True, w=True)
        mc.parent(ctrlIKArm, grpIKVisArm)
        mc.connectAttr("{0}.{1}".format(ctrlArmSettings, ikVis), "{0}.visibility".format(grpIKVisArm))

        CRU.setVisibility(ctrlElbow, lNameAttr, ctrlIKArm, "visibility", 1 - visMin, tangentToUse, False, True, True)
        CRU.lockHideCtrls(grpIKVisArm, translate=True, rotate=True, scale=True, )

        return lNameAttr, lNameAttrVis, grpIKVisArm

    def tgpSetDriverSwitch2Vals(self, driver, driverAttr, driven, valsInOut, *args):

        w0w1Attr = mc.listAttr(driven)[-2:]
        CRU.setDriverDrivenValues(driver, driverAttr, driven, w0w1Attr[0], drivenValue=0, driverValue=0,
                                  modifyBoth=valsInOut)
        CRU.setDriverDrivenValues(driver, driverAttr, driven, w0w1Attr[0], drivenValue=1, driverValue=1,
                                  modifyBoth=valsInOut)
        CRU.setDriverDrivenValues(driver, driverAttr, driven, w0w1Attr[1], drivenValue=0, driverValue=1,
                                  modifyBoth=valsInOut)
        CRU.setDriverDrivenValues(driver, driverAttr, driven, w0w1Attr[1], drivenValue=1, driverValue=0,
                                  modifyBoth=valsInOut)

    def makeShoulderIK(self, jntShoulders, bndStart, leftRight):

        hdlShoulder = "HDL_{0}shoulder".format(leftRight)
        effShoulder = "EFF_{0}shoulder".format(leftRight)
        ikShoulder = mc.ikHandle(n=hdlShoulder, sj=jntShoulders[0], ee=jntShoulders[-1], sol="ikSCsolver",
                                 ccv=False)
        mc.rename(ikShoulder[1], effShoulder)
        ikShoulder[1] = effShoulder
        locShldrTemp = "LOC_{0}shoulder".format(leftRight)
        mc.spaceLocator(p=(0, 0, 0), name=locShldrTemp)
        CRU.constrainMove(bndStart, locShldrTemp, point=True)
        mc.parent(hdlShoulder, locShldrTemp)

        mc.setAttr("{0}.v".format(locShldrTemp), False)

        return locShldrTemp, ikShoulder

    def makeShoulderStretchJoint(self, jntShoulders, locShldr, leftRight):
        if leftRight == self.valLeft:
            # need to make adjustments for the values making a mirror
            m = 1
        else:
            m = -1
        cycleVis = []
        # creates locators for the shoulders
        locShldrDistStart = "LOC_{0}shoulder_lengthStart".format(leftRight)
        locShldrDistEnd = "LOC_{0}shoulder_lengthEnd".format(leftRight)
        distShldr = "DIST_{0}shoulder_length".format(leftRight)

        cycleVis.append(locShldrDistStart)
        cycleVis.append(locShldrDistEnd)
        cycleVis.append(distShldr)

        mc.spaceLocator(p=(0, 0, 0), name=locShldrDistStart)
        mc.spaceLocator(p=(0, 0, 0), name=locShldrDistEnd)

        CRU.constrainMove(jntShoulders[0], locShldrDistStart, point=True)
        CRU.constrainMove(jntShoulders[-1], locShldrDistEnd, point=True)
        distShldrShape = CRU.createDistanceDimensionNode(locShldrDistStart, locShldrDistEnd, distShldr)

        mc.parent(locShldrDistEnd, locShldr)

        ikShoulderEnd = jntShoulders[-1]

        shoulderLen = mc.getAttr("{0}.translateX".format(ikShoulderEnd))

        driverAttr = "distance"
        sumLegLen = shoulderLen * m

        drivenAttr = "translateX"

        ctrlIKLengthKeyArray = []

        # uses the total length to drive the length of the upper leg and  extrapolates it to infinity
        CRU.setDriverDrivenValues(distShldrShape, driverAttr, ikShoulderEnd, drivenAttr, sumLegLen, shoulderLen,
                                  modifyBoth="spline")
        CRU.setDriverDrivenValues(distShldrShape, driverAttr, ikShoulderEnd, drivenAttr, sumLegLen * 2, shoulderLen * 2,
                                  modifyBoth="spline")

        mc.selectKey(cl=True)
        mc.selectKey(ikShoulderEnd, add=True, k=sumLegLen * 2, attribute=drivenAttr)
        mc.setInfinity(poi='cycleRelative')
        ctrlIKLengthKeyArray.append("{0}_{1}".format(ikShoulderEnd, drivenAttr))

        for i in range(len(cycleVis)):
            mc.setAttr("{0}.visibility".format(cycleVis[i]), False)

        return locShldrDistStart, locShldrDistEnd, distShldr, distShldrShape

    def makeShoulderStretchGeo(self, jntShoulders, leftRight):

        # allows the shoulder geo to be stretchable
        # creates multiply divide node
        mdNrmlzDiv = "{0}shoulder_normalize_DIV".format(leftRight)

        mc.shadingNode("multiplyDivide", n=mdNrmlzDiv, au=True)
        mc.setAttr("{0}.operation".format(mdNrmlzDiv), 2)  # set the operation to divide

        # gets default length, plug in default to divisor, base into dividend
        defShoulderLen = mc.getAttr("{0}.translateX".format(jntShoulders[-1]))
        mc.connectAttr("{0}.translateX".format(jntShoulders[-1]), "{0}.input1X".format(mdNrmlzDiv))
        mc.setAttr("{0}.input2X".format(mdNrmlzDiv), defShoulderLen, )

        geoName = jntShoulders[0].replace("JNT_BND_", "GEO_")

        mc.parent(geoName, jntShoulders[0])
        # gets the pivot location for the joint, assign it to the geo (need to do so for scale, rotate and transform
        pivotTranslate = mc.xform(jntShoulders[0], q=True, ws=True, rotatePivot=True)

        mc.makeIdentity(geoName, a=True, t=True, r=True, s=True)
        mc.xform(geoName, ws=True, rotatePivot=pivotTranslate)

        pivotRotate = mc.xform(jntShoulders[0], q=True, ws=True, rotateTranslation=True)
        mc.xform(geoName, ws=True, rotateTranslation=pivotRotate)

        pivotScale = mc.xform(jntShoulders[0], q=True, ws=True, scalePivot=True)
        mc.makeIdentity(geoName, a=True, t=True, r=True, s=True)
        mc.xform(geoName, ws=True, scalePivot=pivotScale)

        # connect the operation into the geo scale
        mc.connectAttr("{0}.outputX".format(mdNrmlzDiv), "{0}.scaleX".format(geoName))
        CRU.layerEdit(geoName, geoLayer=True)
        return

    def makeShoulderControl(self, jntShoulders, locShldrTemp, ctrlArmSettings, leftRight):

        ctrlShoulder = "CTRL_{0}shoulder".format(leftRight)

        defShoulderLen = mc.getAttr("{0}.translateX".format(jntShoulders[-1]))
        # create a pyramid
        if leftRight == self.valLeft:
            m = 1
        else:
            m = -1
        boxDimensionsLWH = [1, m * 4, 1]
        x = boxDimensionsLWH[0]
        y = boxDimensionsLWH[1]
        z = boxDimensionsLWH[2]
        toPass = [(0, y, 0),
                  (-x, 0, z), (-x, 0, -z), (0, y, 0),
                  (x, 0, z), (x, 0, -z), (0, y, 0),
                  (x, 0, z), (x, 0, -z), (-x, 0, -z), (-x, 0, z), (x, 0, z), ]

        try:
            ctrl = mc.curve(ctrlShoulder, r=True, d=1, p=toPass, )
        except:
            ctrl = mc.curve(name=ctrlShoulder, d=1, p=toPass, )

        CRU.constrainMove(jntShoulders[0], ctrlShoulder, parent=True)
        CRU.constrainMove(jntShoulders[-1], ctrlShoulder, point=True)

        mc.select(ctrlShoulder + ".cv[:]")
        mc.move(-defShoulderLen * 0.5, defShoulderLen * 1.25, 0, r=True, os=True)

        mc.makeIdentity(ctrlShoulder, apply=True, t=True, r=True, s=True)

        mc.parent(locShldrTemp, ctrlShoulder)

        # add attribute to ctrl arm settings for shoulder visibility
        lNameAttrVis = "shoulderVisibility"
        mc.addAttr(ctrlArmSettings, ln=lNameAttrVis, attributeType="bool", k=True)

        mc.setAttr("{0}.{1}".format(ctrlArmSettings, lNameAttrVis), True)
        mc.connectAttr("{0}.{1}".format(ctrlArmSettings, lNameAttrVis), "{0}.visibility".format(ctrlShoulder))
        CRU.lockHideCtrls(ctrlShoulder, scale=True, rotate=True, visibility=True)

        return ctrlShoulder

    def makeShoulderGroup(self, ctrlRoot, ctrlShoulder,
                          jntShoulders, jntIKShoulder,
                          locShldrDistStart, distShldr,
                          leftRight):
        jntShoulderBase = jntShoulders[0]
        grpDNTShoulder = "GRP_DO_NOT_TOUCH_{0}shoulder".format(leftRight)
        # create groups and organize them appropriately
        mc.group(n=grpDNTShoulder, em=True, w=True)
        mc.parent(jntShoulderBase, locShldrDistStart, distShldr, grpDNTShoulder)
        grpShoulder = "GRP_{0}shoulder".format(leftRight)

        mc.group(n=grpShoulder, em=True, w=True)
        mc.parent(ctrlShoulder, grpDNTShoulder, grpShoulder)
        mc.parent(grpShoulder, ctrlRoot)

        # TO DELETE this comment: Probably need to get rid of the Connect To Spine bit
        pivotTranslate = mc.xform(jntIKShoulder, q=True, ws=True, rotatePivot=True)
        mc.xform(grpShoulder, ws=True, pivots=pivotTranslate)

        mc.parentConstraint(jntIKShoulder, grpShoulder, mo=True)
        return grpShoulder, grpDNTShoulder

    def organizeArm(self, ctrlRoot, bndJnts, ikJnts, fkJnts,
                    bindJntTwistStart, bindJntTwistMid, bindJntTwistEnd,
                    twistJntsArrayOfArrays,
                    grpIKVisArm, grpIKConstArm, grpArmTwist,
                    distArmElbow, distElbowHand, distIKArmLen,
                    locDistArmElbowStart, locIKDistArmStart,
                    ctrlElbow,
                    jntShoulders,
                    leftRight, ikBndJnts=None):

        if ikBndJnts is None:
            dontSkipIkBnd = False

        else:
            dontSkipIkBnd = True
            # group all arm nodes under the arm
        grpArm = "GRP_{0}arm".format(leftRight)
        mc.group(n=grpArm, em=True, w=True)
        mc.parent(bndJnts[0], fkJnts[0], ikJnts[0], bindJntTwistEnd, bindJntTwistMid, bindJntTwistStart, grpArm)

        mc.parent(grpIKVisArm, grpIKConstArm, grpArmTwist, grpArm)
        mc.parent(locDistArmElbowStart, locIKDistArmStart, distArmElbow, distElbowHand, distIKArmLen, grpArm)
        mc.parent(ctrlElbow, grpArm)

        if dontSkipIkBnd:
            mc.parent(ikBndJnts[0], grpArm)

        for i in range(len(twistJntsArrayOfArrays)):
            mc.parent(twistJntsArrayOfArrays[i][0], grpArm)

        mc.parent(grpArm, ctrlRoot)

        ##########
        # organize the do not touch arm
        grpDNTArm = "GRP_DO_NOT_TOUCH_{0}arm".format(leftRight)
        mc.group(n=grpDNTArm, em=True, w=True)
        mc.parent(grpDNTArm, grpArm)
        # group everything so far except GRP_IK_vis, CTRL_l_elbow, and the FK  Jnts
        mc.parent(bndJnts[0], ikJnts[0], bindJntTwistStart, bindJntTwistMid, bindJntTwistEnd, grpDNTArm)
        mc.parent(grpIKConstArm, grpArmTwist, grpDNTArm)
        mc.parent(locDistArmElbowStart, locIKDistArmStart, distArmElbow, distElbowHand, distIKArmLen, grpDNTArm)
        for i in range(len(twistJntsArrayOfArrays)):
            mc.parent(twistJntsArrayOfArrays[i][0], grpDNTArm)

        if dontSkipIkBnd:
            mc.parent(ikBndJnts[0], grpDNTArm)

        # Group JNT_IK_l_upperArm, LOC_l_upperArm_to_elbowLengthStart, LOC_IK_l_arm_lengthStart
        grpIKConstArmBase = "GRP_IKConst_{0}armBase".format(leftRight)
        mc.group(n=grpIKConstArmBase, em=True, w=True)
        mc.parent(grpIKConstArmBase, grpDNTArm)

        # move the pivot to the base of the arm
        pivotTranslate = mc.xform(bndJnts[0], q=True, ws=True, rotatePivot=True)
        mc.xform(grpIKConstArmBase, ws=True, pivots=pivotTranslate)
        mc.parent(ikJnts[0], locDistArmElbowStart, locIKDistArmStart, grpIKConstArmBase)

        if dontSkipIkBnd:
            mc.parent(ikBndJnts[0], grpIKConstArmBase)
        # create a space locator
        locShoulderSpace = "LOC_shoulderSpace_{0}arm".format(leftRight)
        mc.spaceLocator(p=(0, 0, 0), name=locShoulderSpace)
        # I get this weird error where the GRP_BNDConst_r_arm_orientConstraint1 got rotated 360 degrees depending on the build, causing this weird error when switching between IK and FK arms
        grpAutoShldr = "GRP_AUTO_shoulderSpace_{0}arm".format(leftRight)
        mc.group(n=grpAutoShldr, em=True, w=True)

        grpOffsetShldr = "GRP_OFFSET_shoulderSpace_{0}arm".format(leftRight)
        mc.group(n=grpOffsetShldr, em=True, w=True)

        mc.parent(locShoulderSpace, grpAutoShldr)
        mc.parent(grpAutoShldr, grpOffsetShldr)

        mc.matchTransform(grpOffsetShldr, jntShoulders[-1], pos=True)
        # CRU.constrainMove(jntShoulders[-1], locShoulderSpace, point=True)
        mc.parent(grpOffsetShldr, jntShoulders[-1])

        mc.pointConstraint(locShoulderSpace, grpIKConstArmBase)
        ##########
        grpBNDConstArm = "GRP_BNDConst_{0}arm".format(leftRight)
        mc.group(n=grpBNDConstArm, em=True, w=True)
        mc.parent(grpBNDConstArm, grpDNTArm)
        mc.parent(bndJnts[0], grpBNDConstArm)

        # move to the pivot of the upper arm joint
        pivotTranslate = mc.xform(bndJnts[0], q=True, ws=True, rotatePivot=True)
        mc.xform(grpBNDConstArm, ws=True, pivots=pivotTranslate)
        mc.pointConstraint(locShoulderSpace, grpBNDConstArm)

        return grpArm, grpDNTArm, grpIKConstArmBase, grpBNDConstArm, locShoulderSpace

    def gimbalFix(self, grpArm, fkJnts, bndJnts, grpBNDConstArm, ctrlArmSettings, fkikBlendName, fkVis,
                  locShoulderSpace, leftRight):
        # creates an extra controller to help with
        nrVal = (1, 0, 0)
        sizeVal = 8.5
        ctrlGimbalCorr = "CTRL_gimbalCorr_{0}arm".format(leftRight)
        mc.circle(r=sizeVal, n=ctrlGimbalCorr, nr=nrVal)
        toDelete = "CTRL_gimbalCorrSub_{0}arm".format(leftRight)
        mc.circle(r=1, n=toDelete, nr=nrVal)
        ctrlGimbalCorrSubShp = mc.listRelatives(toDelete, s=True)[0]

        mc.select(toDelete + ".cv[:]")
        if leftRight is self.valLeft:
            m = -1
        else:
            m = 1
        mc.move(m * sizeVal, os=True, r=True, y=True)

        mc.parent(ctrlGimbalCorrSubShp, ctrlGimbalCorr, s=True, r=True)
        mc.select(cl=True)
        mc.delete(toDelete)

        # move and orient to the arm
        CRU.constrainMove(fkJnts[0], ctrlGimbalCorr, parent=True)
        mc.makeIdentity(ctrlGimbalCorr, apply=True, t=True, r=True, s=True)
        mc.parent(ctrlGimbalCorr, grpArm)
        mc.parent(fkJnts[0], ctrlGimbalCorr)
        ##########
        grpGimbalArm = "GRP_BNDGimbal_{0}arm".format(leftRight)
        mc.group(n=grpGimbalArm, em=True, p=grpBNDConstArm)

        pivotTranslate = mc.xform(bndJnts[0], q=True, ws=True, rotatePivot=True)
        mc.xform(grpGimbalArm, ws=True, pivots=pivotTranslate)

        mc.parent(bndJnts[0], grpGimbalArm)

        ##########
        blndGimbalToggle = "{0}arm_gimbalCorrToggle".format(leftRight)
        mc.shadingNode("blendColors", au=True, name=blndGimbalToggle)

        mc.connectAttr("{0}.rotateX".format(ctrlGimbalCorr), "{0}.color2R".format(blndGimbalToggle))
        mc.connectAttr("{0}.rotateY".format(ctrlGimbalCorr), "{0}.color2G".format(blndGimbalToggle))
        mc.connectAttr("{0}.rotateZ".format(ctrlGimbalCorr), "{0}.color2B".format(blndGimbalToggle))

        mc.setAttr("{0}.color1R".format(blndGimbalToggle), 0)
        mc.setAttr("{0}.color1G".format(blndGimbalToggle), 0)
        mc.setAttr("{0}.color1B".format(blndGimbalToggle), 0)

        mc.connectAttr("{0}.outputR".format(blndGimbalToggle), "{0}.rotateX".format(grpGimbalArm))
        mc.connectAttr("{0}.outputG".format(blndGimbalToggle), "{0}.rotateY".format(grpGimbalArm))
        mc.connectAttr("{0}.outputB".format(blndGimbalToggle), "{0}.rotateZ".format(grpGimbalArm))

        mc.connectAttr("{0}.{1}".format(ctrlArmSettings, fkikBlendName), "{0}.blender".format(blndGimbalToggle))
        mc.connectAttr("{0}.{1}".format(ctrlArmSettings, fkVis), "{0}.visibility".format(ctrlGimbalCorr))

        ##########
        grpFKConst = "GRP_FKConst_{0}arm".format(leftRight)
        mc.group(n=grpFKConst, em=True, p=grpArm)
        pivotTranslate = mc.xform(bndJnts[0], q=True, ws=True, rotatePivot=True)
        mc.xform(grpFKConst, ws=True, pivots=pivotTranslate)
        mc.parent(ctrlGimbalCorr, grpFKConst)

        mc.pointConstraint(locShoulderSpace, grpFKConst)

        return ctrlGimbalCorr, grpGimbalArm, blndGimbalToggle, grpFKConst

    def armSpaceSetup(self, locShoulderSpace, grpDNTTorso, ctrlRoot, grpFKConst, grpBNDConstArm, ctrlArmSettings,
                      colourTU, leftRight):
        # put the locators in the right places for limb switching
        locBodySpace = "LOC_bodySpace_{0}arm".format(leftRight)
        locRootSpace = "LOC_rootSpace_{0}arm".format(leftRight)

        mc.duplicate(locShoulderSpace, n=locBodySpace)

        mc.duplicate(locShoulderSpace, n=locRootSpace)
        mc.parent(locBodySpace, grpDNTTorso)
        mc.parent(locRootSpace, ctrlRoot)

        locArmFollowArray = [locShoulderSpace, locBodySpace, locRootSpace]

        # orient constraint these values
        fkOrientConstr = mc.orientConstraint(locShoulderSpace, locBodySpace, locRootSpace, grpFKConst)[0]
        bndOrientConstr = mc.orientConstraint(locShoulderSpace, locBodySpace, locRootSpace, grpBNDConstArm)[0]

        enumName = "FK_rotationSpace"
        enumVals = "shoulder:upperBody:root"

        CRU.makeLimbSwitchNoAutoLocsInPosition(ctrlArmSettings, locArmFollowArray, fkOrientConstr, enumVals, enumName)
        CRU.makeLimbSwitchNoAutoLocsInPosition(ctrlArmSettings, locArmFollowArray, bndOrientConstr, enumVals, enumName)

        return fkOrientConstr, bndOrientConstr

    def fixSegRotInheritsTransformFK(self, crvArms):
        # disable inherits transform
        for i in range(len(crvArms)):
            mc.setAttr("{0}.inheritsTransform".format(crvArms[i]), False)

    def fixSegRotInheritsTransformIK(self, bndOrientConstr, grpBNDConstArm, ctrlArmSettings, fkikBlendName, leftRight):
        # fix it so the IK is properly oriented
        blndBndOrntChoice = "{0}arm_BNDOrientChoice".format(leftRight)

        mc.shadingNode("blendColors", au=True, name=blndBndOrntChoice)

        mc.connectAttr("{0}.constraintRotateX".format(bndOrientConstr), "{0}.color2R".format(blndBndOrntChoice))
        mc.connectAttr("{0}.constraintRotateY".format(bndOrientConstr), "{0}.color2G".format(blndBndOrntChoice))
        mc.connectAttr("{0}.constraintRotateZ".format(bndOrientConstr), "{0}.color2B".format(blndBndOrntChoice))

        mc.setAttr("{0}.color1R".format(blndBndOrntChoice), 0)
        mc.setAttr("{0}.color1G".format(blndBndOrntChoice), 0)
        mc.setAttr("{0}.color1B".format(blndBndOrntChoice), 0)

        # plug this into the bnnd orient group
        mc.connectAttr("{0}.outputR".format(blndBndOrntChoice), "{0}.rotateX".format(grpBNDConstArm), f=True)
        mc.connectAttr("{0}.outputG".format(blndBndOrntChoice), "{0}.rotateY".format(grpBNDConstArm), f=True)
        mc.connectAttr("{0}.outputB".format(blndBndOrntChoice), "{0}.rotateZ".format(grpBNDConstArm), f=True)

        mc.connectAttr("{0}.{1}".format(ctrlArmSettings, fkikBlendName), "{0}.blender".format(blndBndOrntChoice))

    def cleanArm(self, fkJnts, grpFKConst, ctrlIKArm, fkJntsElbow, ctrlArmSettings):

        # We want to lock and hide as much as possible
        # Lock and hide all the controls on the elbow’s locators
        # Hide all the space locators (done already)
        # Add the shoulder joints to jnt_bnd_LYR (already done)
        # Add the geometry to the geo_LYR (already done)
        CRU.lockHideCtrls(ctrlArmSettings, translate=True, rotate=True, scale=True, visibility=True)
        # Lock and hide everything on FKConst
        CRU.lockHideCtrls(grpFKConst, rotate=True, scale=True, translate=True, visibility=True)
        # Lock and hide the scale and visibility of the IK arm control
        CRU.lockHideCtrls(ctrlIKArm, visibility=True, scale=True)

        # Lock and hide the non-length/rotate controls of the elbow FK controls
        for i in range(len(fkJntsElbow)):
            CRU.lockHideCtrls(fkJntsElbow[i], scale=True, translate=True, visibility=True)
            CRU.lockHideCtrls(fkJntsElbow[i], theVals=["radi"], channelBox=False)

        # Lock and hide the non-rotate and length attributes of the FK controls
        for i in range(len(fkJnts)):
            CRU.lockHideCtrls(fkJnts[i], scale=True, translate=True, visibility=True)
            CRU.lockHideCtrls(fkJnts[i], theVals=["radi"], channelBox=False)
        return

    def fixScaling(self, distShldrShape, distIKArmLenShape, ctrlRoot, jntShoulders, ikJnts, distArmElbowShape,
                   distElbowHandShape, blndUpperArmStretchChoice, blndLowerArmStretchChoice,
                   crvInfoUpper, armNrmlzDivUpper,
                   crvInfoLower, armNrmlzDivLower,
                   twistJntsUpper, twistJntsLower,
                   leftRight):
        if leftRight == self.valLeft:
            m = 1
        else:
            m = -1
        mdGScaleArmDiv = "globalScale_{0}arm_normalize_DIV".format(leftRight)
        mdGScaleShldrDiv = "globalScale_{0}shoulder_normalize_DIV".format(leftRight)

        mc.shadingNode("multiplyDivide", n=mdGScaleArmDiv, au=True)
        mc.shadingNode("multiplyDivide", n=mdGScaleShldrDiv, au=True)

        mc.setAttr("{0}.operation".format(mdGScaleArmDiv), 2)
        mc.setAttr("{0}.operation".format(mdGScaleShldrDiv), 2)

        mc.connectAttr("{0}.scaleX".format(ctrlRoot), "{0}.input2X".format(mdGScaleArmDiv))
        mc.connectAttr("{0}.scaleX".format(ctrlRoot), "{0}.input2X".format(mdGScaleShldrDiv))

        mc.connectAttr("{0}.distance".format(distIKArmLenShape), "{0}.input1X".format(mdGScaleArmDiv))
        mc.connectAttr("{0}.distance".format(distShldrShape), "{0}.input1X".format(mdGScaleShldrDiv))

        mc.connectAttr("{0}.outputX".format(mdGScaleShldrDiv), "{0}_translateX.input".format(jntShoulders[-1]), f=True)

        mc.connectAttr("{0}.outputX".format(mdGScaleArmDiv), "{0}_translateX.input".format(ikJnts[1]), f=True)
        mc.connectAttr("{0}.outputX".format(mdGScaleArmDiv), "{0}_translateX.input".format(ikJnts[2]), f=True)

        ##########
        # affect the elbows
        gScaleArmToElbowNrmlzDiv = "globalScale_{0}upperArm_to_elbowNrmlz_DIV".format(leftRight)
        gScaleElbowToHandNrmlzDiv = "globalScale_{0}elbow_to_handNrmlz_DIV".format(leftRight)

        mc.shadingNode("multiplyDivide", n=gScaleArmToElbowNrmlzDiv, au=True)
        mc.shadingNode("multiplyDivide", n=gScaleElbowToHandNrmlzDiv, au=True)

        mc.setAttr("{0}.operation".format(gScaleArmToElbowNrmlzDiv), 2)
        mc.setAttr("{0}.operation".format(gScaleElbowToHandNrmlzDiv), 2)

        # this is for the mirror values
        gScaleArmToElbowNrmlzInvertMult = "globalScale_{0}upperArm_to_ElbowInvert_MUL".format(leftRight)
        gScaleElbowToHandNrmlzInvertMult = "globalScale_{0}elbow_to_handInvert_MUL".format(leftRight)

        mc.shadingNode("multiplyDivide", n=gScaleArmToElbowNrmlzInvertMult, au=True)
        mc.shadingNode("multiplyDivide", n=gScaleElbowToHandNrmlzInvertMult, au=True)
        ##########

        mc.connectAttr("{0}.distance".format(distArmElbowShape), "{0}.input1X".format(gScaleArmToElbowNrmlzInvertMult))
        mc.connectAttr("{0}.distance".format(distElbowHandShape),
                       "{0}.input1X".format(gScaleElbowToHandNrmlzInvertMult))

        # multiplies by -1 if on the right
        mc.setAttr("{0}.input2X".format(gScaleArmToElbowNrmlzInvertMult), m)
        mc.setAttr("{0}.input2X".format(gScaleElbowToHandNrmlzInvertMult), m)

        mc.connectAttr("{0}.outputX".format(gScaleArmToElbowNrmlzInvertMult),
                       "{0}.input1X".format(gScaleArmToElbowNrmlzDiv))
        mc.connectAttr("{0}.outputX".format(gScaleElbowToHandNrmlzInvertMult),
                       "{0}.input1X".format(gScaleElbowToHandNrmlzDiv))

        mc.connectAttr("{0}.scaleX".format(ctrlRoot), "{0}.input2X".format(gScaleArmToElbowNrmlzDiv))
        mc.connectAttr("{0}.scaleX".format(ctrlRoot), "{0}.input2X".format(gScaleElbowToHandNrmlzDiv))

        mc.connectAttr("{0}.outputX".format(gScaleArmToElbowNrmlzDiv), "{0}.color1R".format(blndUpperArmStretchChoice),
                       f=True)
        mc.connectAttr("{0}.outputX".format(gScaleElbowToHandNrmlzDiv), "{0}.color1R".format(blndLowerArmStretchChoice),
                       f=True)

        ##########
        # affect the segments
        gScaleUpperNrmlzDive = "globalScale_{0}upperArm_normalize_DIV".format(leftRight)
        gScaleLowerNrmlzDive = "globalScale_{0}lowerArm_normalize_DIV".format(leftRight)

        mc.shadingNode("multiplyDivide", n=gScaleUpperNrmlzDive, au=True)
        mc.shadingNode("multiplyDivide", n=gScaleLowerNrmlzDive, au=True)

        mc.setAttr("{0}.operation".format(gScaleUpperNrmlzDive), 2)
        mc.setAttr("{0}.operation".format(gScaleLowerNrmlzDive), 2)

        mc.connectAttr("{0}.outputX".format(armNrmlzDivUpper), "{0}.input1X".format(gScaleUpperNrmlzDive))
        mc.connectAttr("{0}.outputX".format(armNrmlzDivLower), "{0}.input1X".format(gScaleLowerNrmlzDive))

        mc.connectAttr("{0}.scaleX".format(ctrlRoot), "{0}.input2X".format(gScaleUpperNrmlzDive))
        mc.connectAttr("{0}.scaleX".format(ctrlRoot), "{0}.input2X".format(gScaleLowerNrmlzDive))

        for i in range(len(twistJntsUpper) - 1):
            mc.connectAttr("{0}.outputX".format(gScaleUpperNrmlzDive), "{0}.scaleX".format(twistJntsUpper[i]), f=True)
        for i in range(len(twistJntsLower) - 1):
            mc.connectAttr("{0}.outputX".format(gScaleLowerNrmlzDive), "{0}.scaleX".format(twistJntsLower[i]), f=True)

        return

    def ikStretchOnOffNormal(self, ikJnts, ctrlArmSettings, blndUpperArmStretchChoice, blndLowerArmStretchChoice,
                             leftRight):
        # creates the IK Stretch on/off for the arm
        ikStretchAttr = "IK_stretch"
        enumVals = "on:off"
        mc.addAttr(ctrlArmSettings, longName=ikStretchAttr, at="enum", k=True, en=enumVals)

        condLowerArmIKStretch = "{0}lowerArm_IK_stretch_COND".format(leftRight)
        condHandIKStretch = "{0}hand_IK_stretch_COND".format(leftRight)

        self.makeIKStretchMethodNormal(ikJnts[1], condLowerArmIKStretch, ctrlArmSettings, ikStretchAttr,
                                       blndUpperArmStretchChoice)
        self.makeIKStretchMethodNormal(ikJnts[2], condHandIKStretch, ctrlArmSettings, ikStretchAttr,
                                       blndLowerArmStretchChoice)

        return

    def makeIKStretchMethodNormal(self, ikJnt, cond, ctrlArmSettings, ikStretchAttr, blendChoice):

        mc.shadingNode("condition", n=cond, au=True)
        len1 = mc.getAttr("{0}.translateX".format(ikJnt))

        mc.setAttr("{0}.colorIfFalse".format(cond), len1, 0, 0)

        mc.connectAttr("{0}.outputR".format(blendChoice), "{0}.colorIfTrueR".format(cond))

        mc.connectAttr("{0}.{1}".format(ctrlArmSettings, ikStretchAttr), "{0}.firstTerm".format(cond))
        mc.setAttr("{0}.secondTerm".format(cond), 0)
        mc.setAttr("{0}.operation".format(cond), 0)

        mc.connectAttr("{0}.outColorR".format(cond), "{0}.translateX".format(ikJnt), f=True)

    def ikStretchOnOffSpecial(self, ikJnts, ikBndJnts, ctrlArmSettings, leftRight):
        # creates the IK Stretch on/off for the elbow arm
        ikStretchAttr = "IK_stretch"
        enumVals = "on:off"
        mc.addAttr(ctrlArmSettings, longName=ikStretchAttr, at="enum", k=True, en=enumVals)

        condLowerArmIKStretch = "{0}lowerArm_IK_stretch_COND".format(leftRight)
        condHandIKStretch = "{0}hand_IK_stretch_COND".format(leftRight)

        self.makeIKStretchMethodSpecial(ikJnts[1], ikBndJnts[1], condLowerArmIKStretch, ctrlArmSettings, ikStretchAttr)
        self.makeIKStretchMethodSpecial(ikJnts[2], ikBndJnts[2], condHandIKStretch, ctrlArmSettings, ikStretchAttr)
        return

    def makeIKStretchMethodSpecial(self, ikJnt, ikBndJnt, cond, ctrlArmSettings, ikStretchAttr):

        mc.shadingNode("condition", n=cond, au=True)
        len1 = mc.getAttr("{0}.translateX".format(ikJnt))

        mc.setAttr("{0}.colorIfFalse".format(cond), len1, 0, 0)

        mc.connectAttr("{0}.translateX".format(ikJnt), "{0}.colorIfTrueR".format(cond))

        mc.connectAttr("{0}.{1}".format(ctrlArmSettings, ikStretchAttr), "{0}.firstTerm".format(cond))
        mc.setAttr("{0}.secondTerm".format(cond), 0)
        mc.setAttr("{0}.operation".format(cond), 0)

        mc.connectAttr("{0}.outColorR".format(cond), "{0}.translateX".format(ikBndJnt), f=True)

    def toggleShoulderStretch(self, jntShoulders, ctrlShoulder, leftRight):

        stretchAttr = "shoulderStretch"
        enumVals = "on:off"
        mc.addAttr(ctrlShoulder, longName=stretchAttr, at="enum", k=True, en=enumVals)

        # toggles the shoulder's stretch
        jntShoulderEnd = jntShoulders[-1]
        jntShoulderStart = jntShoulders[0]
        len = mc.getAttr("{0}.translateX".format(jntShoulderEnd))
        # creates the shoulder stretch condition
        shoulderStretchCond = "{0}shoulder_stretch_COND".format(leftRight)
        mc.shadingNode("condition", n=shoulderStretchCond, au=True)

        mc.connectAttr("{0}.{1}".format(ctrlShoulder, stretchAttr), "{0}.firstTerm".format(shoulderStretchCond))

        mc.setAttr("{0}.secondTerm".format(shoulderStretchCond), 0)
        mc.setAttr("{0}.operation".format(shoulderStretchCond), 0)

        # connects it to the conditional
        mc.connectAttr("{0}_translateX.output".format(jntShoulderEnd), "{0}.colorIfTrueR".format(shoulderStretchCond))
        mc.setAttr("{0}.colorIfFalseR".format(shoulderStretchCond), len)

        mc.connectAttr("{0}.outColorR".format(shoulderStretchCond), "{0}.translateX".format(jntShoulderEnd), f=True)
        return shoulderStretchCond

    def makeIKBndJnts(self, ikJnts):

        ikBndJnts = mc.duplicate(ikJnts[0], rc=True)
        for i in range(len(ikBndJnts)):
            renameVal = ikBndJnts[i][:-1].replace("_IK_", "_IKbnd_")
            mc.rename(ikBndJnts[i], renameVal)
            ikBndJnts[i] = renameVal
            mc.orientConstraint(ikJnts[i], ikBndJnts[i])
            if i != 0:
                mc.connectAttr("{0}.tx".format(ikJnts[i]), "{0}.tx".format(ikBndJnts[i]))

        return ikBndJnts

    def makeArmComplete(self, isLeft, leftRight,
                        jntArmArray,
                        colourTU, jntShoulderRoot,
                        jntIKShoulder, ctrlRoot,
                        grpDNTTorso,
                        grpSpineToggle,
                        cbSpecialStretch, checkGeo, checkToggleSpineStretch,
                        geoJntArray, *args):

        '''uArmLen = mc.getAttr("{0}.tx".format(mc.listRelatives(jntArmArray[0])[0]))
        lArmLen = mc.getAttr("{0}.tx".format(mc.listRelatives(jntArmArray[1])[0]))'''
        jntOrientTracking = []
        # Creating FK and IK Joints
        bndJnts, fkJnts, ikJnts = self.getBndFkIkJnts(jntArmArray)

        # we want to create FK controls for the limbs except the end
        fkJnts = self.createArmFKs(fkJnts, )

        # create the IK control without attaching it to anything
        name = "{0}arm".format(leftRight)
        ctrlIKArm = CRU.setupCtrl(name, colourTU=colourTU, addPrefix=True, boxDimensionsLWH=(3, 6, 6))[0]
        todelete = mc.pointConstraint(ikJnts[-2], ctrlIKArm)
        mc.delete(todelete)
        rotOrderTemp = mc.getAttr("{0}.rotateOrder".format(ikJnts[-2]))
        mc.setAttr("{0}.rotateOrder".format(ctrlIKArm), rotOrderTemp)

        if cbSpecialStretch:
            # this is for an experimental stretch toggle effect
            ikBndJnts = self.makeIKBndJnts(ikJnts)

        ##########
        # to delete test
        # if this works, delete the notes, otherwise delete this part
        # I want to see how 0-out the IK control works. If things mess up, try not including this step

        mc.makeIdentity(ctrlIKArm, apply=True, t=True, r=True, s=True)

        ##########
        # create the settings control
        name = "settings_" + leftRight + "arm"
        if cbSpecialStretch:
            ikJntsUse = ikBndJnts
        else:
            ikJntsUse = ikJnts
        ctrlArmSettings, fkikBlendName, fkVis, ikVis = self.createSettings(jntArmArray, isLeft, name, colourTU, fkJnts,
                                                                           ikJntsUse, bndJnts, ctrlIKArm)
        # set visibility
        tangentToUse = ["linear", "step"]

        CRU.setVisibility(ctrlArmSettings, fkikBlendName, ctrlArmSettings, fkVis, .999, tangentToUse, True, True, False)
        CRU.setVisibility(ctrlArmSettings, fkikBlendName, ctrlArmSettings, ikVis, .999, tangentToUse, False, True, True)

        ##########
        # Twistable segments
        # Adding the twist joints
        # twistJntsArrayOfArrays is an array of arrays

        defFKIKBlend = mc.getAttr("{0}.{1}".format(ctrlArmSettings, fkikBlendName))
        mc.setAttr("{0}.{1}".format(ctrlArmSettings, fkikBlendName), 0)
        geoJntArray, twistJntsArrayOfArrays = self.makeTwists(5, jntArmArray, geoJntArray, leftRight)
        mc.setAttr("{0}.{1}".format(ctrlArmSettings, fkikBlendName), defFKIKBlend)
        grpArmTwist = "GRP_{0}armTwist".format(leftRight)
        mc.group(n=grpArmTwist, em=True, w=True)

        ikUpperArm = self.makeCrvSpline(twistJntsArrayOfArrays[0], leftRight, "upperArm", grpArmTwist)
        ikLowerArm = self.makeCrvSpline(twistJntsArrayOfArrays[1], leftRight, "lowerArm", grpArmTwist)
        ikArms = [ikUpperArm, ikLowerArm]
        crvArms = [ikUpperArm[2], ikLowerArm[2]]

        bindJntTwistStart, bindJntTwistMid, bindJntTwistEnd = self.bindArmTwists(twistJntsArrayOfArrays, leftRight,
                                                                                 ikArms)

        # upperArm parentConstraints start, lowerArm parentConstraints mid, hand parentConstraints end
        mc.pointConstraint(jntArmArray[0], bindJntTwistStart)
        # mc.parentConstraint(jntArmArray[0], bindJntTwistStart) # this is the default, but I am experimenting a little
        mc.parentConstraint(jntArmArray[1], bindJntTwistMid)
        mc.parentConstraint(jntArmArray[2], bindJntTwistEnd)

        mc.setAttr("{0}.visibility".format(grpArmTwist), False)

        ##########
        # FK Stretch
        ctrlFKLengthKeyArray = self.makeFKStretchJnt(fkJnts, "Arm")
        # FK Scale Geometry

        crvInfoUpper, armNrmlzDivUpper = self.makeBndStretchTwists(bndJnts[0], crvArms[0], twistJntsArrayOfArrays[0],
                                                                   leftRight)
        crvInfoLower, armNrmlzDivLower = self.makeBndStretchTwists(bndJnts[1], crvArms[1], twistJntsArrayOfArrays[1],
                                                                   leftRight)
        ##########

        ##########
        # IK Arm
        ikArms, ikHands = self.makeIKHandle(ctrlIKArm, ikJnts, leftRight)
        hdlArm = ikArms[0]

        # IK Stretch
        vals = self.makeIKStretch(bindJntTwistStart, bindJntTwistEnd, ikJnts, ctrlIKArm, leftRight)
        locIKDistArmStart, locIKDistArmEnd, distIKArmLen, distIKArmLenShape, ctrlIKArmLengthKeyArray = vals

        ##########

        ##########
        # Snappable elbow
        # Elbow
        locElbow, ctrlElbow = self.makeElbowCtrl(leftRight, ikJnts, hdlArm)

        # Elbow Snap
        valsElbowSnap = self.makeElbowSnap(ikJnts, ctrlIKArm, ctrlElbow, leftRight)
        locDistArmElbowStart, locDistArmElbowEnd, distArmElbow, locDistElbowHandStart, \
        locDistElbowHandEnd, distElbowHand, distArmElbowShape, distElbowHandShape, \
        blndUpperArmStretchChoice, blndLowerArmStretchChoice = valsElbowSnap
        ##########
        # IK/FK hybrid elbow
        # Elbow FK Forearm
        fkJntsElbow, fkElbow = self.makeFKElbow(fkJnts, ctrlElbow)

        # Elbow FK IK Switch
        grpIKConstArm, grpIKConstArmConstraint = self.makeElbowFKIKSwitch(ctrlIKArm, ikJnts, fkJntsElbow, leftRight)

        lNameAttr, lNameAttrVis, grpIKVisArm = self.makeElbowFKIKSwitchControl(ctrlElbow, grpIKConstArmConstraint,
                                                                               fkElbow,
                                                                               ctrlIKArm, ctrlArmSettings, ikVis,
                                                                               leftRight)
        mc.connectAttr("{0}.{1}".format(ctrlArmSettings, ikVis), "{0}.visibility".format(ctrlElbow))
        CRU.lockHideCtrls(ctrlElbow, scale=True, visibility=True, rotate=True)

        ctrlFKElbowLengthKeyArray = self.makeFKStretchJnt(fkJntsElbow, "ArmElbow", add=False)

        ##########

        # Part 26: Translation-based shoulder rig
        jntShoulders = mc.listRelatives(jntShoulderRoot, type="joint")

        jntShoulders.append(jntShoulderRoot)
        jntShoulders.reverse()

        geoJntArray.extend(jntShoulders)
        bndStart = bndJnts[0]

        locShldrTemp, ikShoulder = self.makeShoulderIK(jntShoulders, bndStart, leftRight)

        # Shoulder Stretch
        locShldrDistStart, locShldrDistEnd, distShldr, distShldrShape = self.makeShoulderStretchJoint(jntShoulders,
                                                                                                      locShldrTemp,
                                                                                                      leftRight)

        if checkGeo:
            self.makeShoulderStretchGeo(jntShoulders, leftRight)

        ctrlShoulder = self.makeShoulderControl(jntShoulders, locShldrTemp, ctrlArmSettings, leftRight)

        # It's fine to put this here
        if checkGeo:
            defFKIKBlend = mc.getAttr("{0}.{1}".format(ctrlArmSettings, fkikBlendName))
            mc.setAttr("{0}.{1}".format(ctrlArmSettings, fkikBlendName), 0)
            CRU.tgpSetGeo(geoJntArray, setLayer=True, printOut=False)
            mc.setAttr("{0}.{1}".format(ctrlArmSettings, fkikBlendName), defFKIKBlend)
        ##########
        # Part 27: Arm global transform and cleanup
        # Shoulder Organizing
        grpShoulder, grpDNTShoulder = self.makeShoulderGroup(ctrlRoot, ctrlShoulder,
                                                             jntShoulders, jntIKShoulder,
                                                             locShldrDistStart, distShldr,
                                                             leftRight)

        if not cbSpecialStretch:
            ikBndJnts = None
            # Arm organizing
        grpArm, grpDNTArm, grpIKConstArmBase, grpBNDConstArm, locShoulderSpace = \
            self.organizeArm(ctrlRoot, bndJnts, ikJnts, fkJnts,
                             bindJntTwistStart, bindJntTwistMid, bindJntTwistEnd,
                             twistJntsArrayOfArrays,
                             grpIKVisArm, grpIKConstArm, grpArmTwist,
                             distArmElbow, distElbowHand, distIKArmLen,
                             locDistArmElbowStart, locIKDistArmStart,
                             ctrlElbow,
                             jntShoulders,
                             leftRight, ikBndJnts=ikBndJnts)
        '''grpArm, grpDNTArm, grpIKConstArmBase, grpBNDConstArm, locShoulderSpace = \
            self.organizeArmBak(ctrlRoot, bndJnts, ikJnts, fkJnts,
                             bindJntTwistStart, bindJntTwistMid, bindJntTwistEnd,
                             twistJntsArrayOfArrays,
                             grpIKVisArm, grpIKConstArm, grpArmTwist,
                             distArmElbow, distElbowHand, distIKArmLen,
                             locDistArmElbowStart, locIKDistArmStart,
                             ctrlElbow,
                             jntShoulders,
                             leftRight, ikBndJnts=ikBndJnts)'''

        ctrlGimbalCorr, grpGimbalArm, blndGimbalToggle, grpFKConst = self.gimbalFix(grpArm, fkJnts, bndJnts,
                                                                                    grpBNDConstArm, ctrlArmSettings,
                                                                                    fkikBlendName, fkVis,
                                                                                    locShoulderSpace,
                                                                                    leftRight)

        # Arm space
        fkOrientConstr, bndOrientConstr = self.armSpaceSetup(locShoulderSpace, grpDNTTorso, ctrlRoot, grpFKConst,
                                                             grpBNDConstArm, ctrlArmSettings,
                                                             colourTU, leftRight)

        # Geometry and Segments fix

        self.fixSegRotInheritsTransformFK(crvArms)
        self.fixSegRotInheritsTransformIK(bndOrientConstr, grpBNDConstArm, ctrlArmSettings, fkikBlendName, leftRight)

        # Clean up
        self.cleanArm(fkJnts, grpFKConst, ctrlIKArm, fkJntsElbow, ctrlArmSettings)
        if cbSpecialStretch:
            # set the visibility of the IKs to 0 if we are working with the ikBndJnts
            mc.setAttr("{0}.v".format(ikJnts[0]), False)

        # Root Transform Scaling
        twistJntsUpper, twistJntsLower = twistJntsArrayOfArrays
        # add the twists to the bnd_layer
        CRU.layerEdit(twistJntsUpper, bndLayer=True, noRecurse=True)
        CRU.layerEdit(twistJntsLower, bndLayer=True, noRecurse=True)

        self.fixScaling(distShldrShape, distIKArmLenShape, ctrlRoot, jntShoulders, ikJnts, distArmElbowShape,
                        distElbowHandShape, blndUpperArmStretchChoice, blndLowerArmStretchChoice,
                        crvInfoUpper, armNrmlzDivUpper,
                        crvInfoLower, armNrmlzDivLower,
                        twistJntsUpper, twistJntsLower,
                        leftRight)
        # Special: Turn off IK Stretch
        if cbSpecialStretch:
            self.ikStretchOnOffSpecial(ikJnts, ikBndJnts, ctrlArmSettings, leftRight)
        else:
            self.ikStretchOnOffNormal(ikJnts, ctrlArmSettings, blndUpperArmStretchChoice, blndLowerArmStretchChoice,
                                      leftRight)
        # Special: Turn off Shoulder Stretch
        if cbSpecialStretch:
            shoulderStretchCond = self.toggleShoulderStretch(jntShoulders, ctrlShoulder, leftRight)
        fkLayer = "{0}arm_FK_lyr".format(leftRight)
        ikLayer = "{0}arm_IK_lyr".format(leftRight)

        CRU.layerEdit(fkJnts, newLayerName=fkLayer, colourTU=colourTU)

        CRU.layerEdit(ctrlGimbalCorr, newLayerName=fkLayer)  # add the gimbal correction to the FK layer

        CRU.layerEdit(jntShoulders, bndLayer=True, noRecurse=True)
        CRU.layerEdit(jntShoulders[-1], bndAltLayer=True, noRecurse=True)

        CRU.layerEdit(ikJnts, newLayerName=ikLayer)

        if cbSpecialStretch:
            CRU.layerEdit(ikBndJnts, newLayerName=ikLayer)

        CRU.layerEdit(bndJnts, bndLayer=True, noRecurse=True)

        altBnds = [x for x in bndJnts if "arm" in x.lower() and "seg" not in x.lower() or "hand" in x.lower()]
        for i in range(len(twistJntsArrayOfArrays)):
            # put the last seg into the alt bnds since it shares the same space as lower arm's seg1 or hand
            altBnds.append(twistJntsArrayOfArrays[i][-1])
        # the jnt_BND_lyr is supposed to be for the skinning joints

        CRU.layerEdit(altBnds, bndAltLayer=True, noRecurse=True)

        CRU.layerEdit(ctrlElbow, newLayerName=ikLayer)
        CRU.layerEdit(ctrlIKArm, newLayerName=ikLayer)

        mc.setAttr("{0}.displayType".format(ikLayer), 0)
        mc.setAttr("{0}.color".format(ikLayer), 0)
        if isLeft:
            clrIKrgb = CRU.clrLeftIK
        else:
            clrIKrgb = CRU.clrRightIK
        mc.setAttr("{0}.overrideColorRGB".format(ikLayer), clrIKrgb[0], clrIKrgb[1], clrIKrgb[2])
        mc.setAttr("{0}.overrideRGBColors".format(ikLayer), 1)
        # appendix A
        if self.switchSetup:
            self.makeArmFKIKComplete(bndJnts, fkJnts, ctrlIKArm)

        # appendix B
        if checkToggleSpineStretch:
            self.setSpineStretchToggle(grpSpineToggle, grpShoulder)
        return

    def makeArmFKIKComplete(self, bndJnts, fkJnts, ctrlIK, ):
        fkSwitchJnts = self.makeFKSnapJnts(fkJnts, bndJnts)

        ctrlIKSwitch = self.makeIKSnap(ctrlIK, bndJnts)

        return

    def makeFKSnapJnts(self, fkJnts, bndJnts):
        fkSwitchJnts = []
        for i in range(len(fkJnts[:-1])):
            # create duplicates of everything except the last joint
            rename = fkJnts[i].replace("CTRL_FK_", "JNT_FKsnap_")
            mc.duplicate(fkJnts[i], n=rename, po=True)
            CRU.lockHideCtrls(rename, translate=True, visibility=True, attrVisible=True, toLock=False)
            mc.parent(rename, bndJnts[i])
            mc.setAttr("{0}.visibility".format(rename), False)
            CRU.lockHideCtrls(rename, visibility=True)
            fkSwitchJnts.append(rename)

        return fkSwitchJnts

    def makeIKSnap(self, ctrlIK, bndJnts):
        # create the hand IK and parent it under the hand
        ctrlIKSwitch = ctrlIK.replace("CTRL_", "GRP_IKsnap_")
        mc.duplicate(ctrlIK, n=ctrlIKSwitch, po=True)
        mc.parent(ctrlIKSwitch, bndJnts[-2])

        CRU.lockHideCtrls(ctrlIKSwitch, translate=True, visibility=True, attrVisible=True, toLock=False)
        mc.setAttr("{0}.visibility".format(ctrlIKSwitch), False)
        CRU.lockHideCtrls(ctrlIKSwitch, visibility=True)

        return ctrlIKSwitch

    '''def makeTwistsBak(self, numTwists, jntArmArray, geoJntArray, *args):
        numTwistsM1 = numTwists - 1

        twists = numTwists
        twistJntsArrayOfArrays = []

        for i in range(len(jntArmArray)):
            if "Arm" not in jntArmArray[i]:
                # skip everything if there's no arm in the
                continue
            twistJntsSubgroup = []
            val = str(jntArmArray[i])
            nextJnt = mc.listRelatives(val, c=True, type="joint")[0]
            nextJntXVal = mc.getAttr("{0}.tx".format(nextJnt))
            nextJntIncrement = nextJntXVal / (numTwistsM1)
            twistJnt = mc.duplicate(val, po=True, n="ToDelete")

            # create the joint twists at the proper location
            for x in range(twists):
                valx = x + 1
                twistTempName = "{0}_seg{1}".format(val, valx)

                twistTemp = mc.duplicate(twistJnt, n=twistTempName)[0]

                twistJntsSubgroup.append(twistTemp)

                mc.parent(twistTemp, jntArmArray[i])
                mc.setAttr("{0}.tx".format(twistTempName), nextJntIncrement * x)
                if x != 0:
                    # we want to skip for the first value for parenting the subjoints

                    mc.parent(twistTemp, twistJntsSubgroup[x - 1])

                geoJntArray.append(twistTempName)
            # puts the top value into worldspace
            mc.parent(twistJntsSubgroup[0], w=True)

            mc.delete(twistJnt)

            twistJntsArrayOfArrays.append(twistJntsSubgroup)

        return geoJntArray, twistJntsArrayOfArrays'''

    def makeTwists(self, numTwists, jntArmArray, geoJntArray, leftRight, *args):
        if leftRight == self.valLeft:
            locRotZ = 0
        else:
            locRotZ = 180
        numTwistsM1 = numTwists - 1

        twists = numTwists
        twistJntsArrayOfArrays = []

        for i in range(len(jntArmArray)):
            if "Arm" not in jntArmArray[i]:
                # skip everything if there's no arm in the
                continue
            twistJntsSubgroup = []
            val = str(jntArmArray[i])
            nextJnt = mc.listRelatives(val, c=True, type="joint")[0]
            nextJntXVal = mc.getAttr("{0}.tx".format(nextJnt))
            nextJntIncrement = nextJntXVal / (numTwistsM1)
            twistJnt = mc.duplicate(val, po=True, n="ToDelete")
            mc.rotate(locRotZ, twistJnt, z=True, os=True, r=True)
            if leftRight == self.valRight:
                mc.makeIdentity(twistJnt, r=True, a=True)

            # create the joint twists at the proper location
            for x in range(twists):
                valx = x + 1
                twistTempName = "{0}_seg{1}".format(val, valx)

                twistTemp = mc.duplicate(twistJnt, n=twistTempName)[0]

                twistJntsSubgroup.append(twistTemp)

                mc.parent(twistTemp, jntArmArray[i])
                mc.setAttr("{0}.tx".format(twistTempName), nextJntIncrement * x)
                if x != 0:
                    # we want to skip for the first value for parenting the subjoints

                    mc.parent(twistTemp, twistJntsSubgroup[x - 1])

                geoJntArray.append(twistTempName)
            # puts the top value into worldspace
            mc.parent(twistJntsSubgroup[0], w=True)

            mc.delete(twistJnt)

            twistJntsArrayOfArrays.append(twistJntsSubgroup)

        return geoJntArray, twistJntsArrayOfArrays

    def getBndFkIkJnts(self, jntArmArray, *args):
        # creates fk and ik, and renames them appropriately
        bndJnts = jntArmArray
        fkJnts = mc.duplicate(jntArmArray[0], rc=True)
        ikJnts = mc.duplicate(jntArmArray[0], rc=True)
        for i in range(len(fkJnts)):
            tempNameFK = fkJnts[i][:-1].replace("_BND_", "_FK_")
            tempNameIK = ikJnts[i][:-1].replace("_BND_", "_IK_")
            mc.rename(fkJnts[i], tempNameFK)
            mc.rename(ikJnts[i], tempNameIK)
            fkJnts[i] = tempNameFK
            ikJnts[i] = tempNameIK

        return bndJnts, fkJnts, ikJnts

    def makeCrvSpline(self, twistJntsSub, leftRight, name, grp=None, *args):
        pivotTranslate1 = mc.xform(twistJntsSub[0], q=True, ws=True, rotatePivot=True)
        pivotTranslate2 = mc.xform(twistJntsSub[-1], q=True, ws=True, rotatePivot=True)

        tempCurve = mc.curve(d=1, p=[(pivotTranslate1[0], pivotTranslate1[1], pivotTranslate1[2]),
                                     (pivotTranslate2[0], pivotTranslate2[1], pivotTranslate2[2])])
        effArm = "EFF_{0}{1}".format(leftRight, name)
        hdlArm = "HDL_{0}{1}".format(leftRight, name)
        crvArm = "CRV_{0}{1}".format(leftRight, name)
        mc.rename(tempCurve, crvArm)
        ikArm = mc.ikHandle(n=hdlArm, sj=twistJntsSub[0], ee=twistJntsSub[-1], c=crvArm, sol="ikSplineSolver",
                            ccv=False)
        mc.rename(ikArm[1], effArm)
        ikArm[1] = effArm
        ikArm.append(crvArm)

        if grp is not None:
            mc.parent(crvArm, hdlArm, grp)

        return ikArm

    def setupIkElblowArmTwist(self, ikOffsetCtrl, ikJnts, ikArms, isLeft, *args):
        elbowTwistAttr = "elbowTwist"
        mc.addAttr(ikOffsetCtrl[1], longName=elbowTwistAttr, at="float", k=True)

        mc.connectAttr("{0}.{1}".format(ikOffsetCtrl[1], elbowTwistAttr), ikJnts[1] + ".rotateY")

        armTwistAttr = "armTwist"
        mc.addAttr(ikOffsetCtrl[1], longName=armTwistAttr, at="float", k=True)

        ikCtrlArmTwistNode = "{0}_{1}_md".format(ikOffsetCtrl[1], armTwistAttr)
        mc.shadingNode("multiplyDivide", n=ikCtrlArmTwistNode, au=True)

        # creates nodes that will affect whether or not the twist will go one way or another
        mc.setAttr("{0}.operation".format(ikCtrlArmTwistNode), 2)
        if isLeft:
            mc.setAttr("{0}.i2x".format(ikCtrlArmTwistNode), 1)
        else:
            mc.setAttr("{0}.i2x".format(ikCtrlArmTwistNode), -1)

        mc.connectAttr("{0}.{1}".format(ikOffsetCtrl[1], armTwistAttr), ikCtrlArmTwistNode + ".i1x")
        mc.connectAttr("{0}.ox".format(ikCtrlArmTwistNode), ikArms[0] + ".twist")

    def createElbow(self, ikJntsDrive, leftRight, armLength, ikArms, isLeft, colourTU, *args):
        elbowName = "CTRL_" + leftRight + "elbow"

        elbowOffsetCtrl = []
        elbowOffsetCtrl.append(mc.group(n="OFFSET_" + elbowName, w=True, em=True))
        elbowOffsetCtrl.append(mc.spaceLocator(p=(0, 0, 0), name=elbowName)[0])
        elbowOffsetCtrl.append(mc.group(n="AUTO_" + elbowName, w=True, em=True))

        mc.parent(elbowOffsetCtrl[2], elbowOffsetCtrl[0])
        mc.parent(elbowOffsetCtrl[1], elbowOffsetCtrl[2])

        mc.setAttr("{0}.overrideEnabled".format(elbowOffsetCtrl[1]), 1)
        mc.setAttr("{0}.overrideColor".format(elbowOffsetCtrl[1]), colourTU)

        toDelete = mc.pointConstraint(ikJntsDrive, elbowOffsetCtrl[0])
        toDelete2 = mc.aimConstraint(ikJntsDrive[1], elbowOffsetCtrl[0], aim=(0, 0, 1))

        mc.delete(toDelete, toDelete2)

        if not isLeft:
            armLength = -armLength

        mc.move(armLength / 2, elbowOffsetCtrl[0], z=True, os=True)

        mc.poleVectorConstraint(elbowOffsetCtrl[1], ikArms[0])

        return elbowOffsetCtrl

    def createArmFKs(self, fkJnts, *args):
        # creates the FK arms
        iters = len(fkJnts[:-1])
        for i in range(iters):

            size = 10
            if i != iters - 1:
                armLen = mc.getAttr("{0}.tx".format(mc.listRelatives(fkJnts[i])[0]))

            else:
                armLen = 0
            # gets the shape of the FK
            ctrl, fkShape = CRU.createCTRLsFKDirect(fkJnts[i], size - 2 * i)
            fkJnts[i] = ctrl

            mc.select(fkShape + ".cv[:]")

            mc.move(armLen * 0.5, 0, 0, r=True, os=True)

        return fkJnts

    def setSpineStretchToggle(self, grpSpineToggle, grpShoulder):

        todelete = mc.listRelatives(grpShoulder, type="parentConstraint")[0]
        mc.delete(todelete)

        mc.parentConstraint(grpSpineToggle, grpShoulder, mo=True)
        return

    def tgpMakeBC(self, *args):
        symmetry = CRU.checkSymmetry()  # we want symmetry turned off for this process

        checkSelLeft = mc.radioButtonGrp("selArmType_rbg", q=True, select=True)
        mirrorSel = mc.radioButtonGrp("selArmMirrorType_rbg", q=True, select=True)

        checkGeo = mc.checkBox("selGeo_cb", q=True, v=True)
        self.switchSetup = mc.checkBox("selAddIKFKSwitching_cb", q=True, v=True)

        checkToggleSpineStretch = mc.checkBox("selStretchSpineToggle_cb", q=True, v=True)

        bndJnt = mc.textFieldButtonGrp("jointArmsLoad_tfbg", q=True, text=True)
        bndJnts = self.tgpGetJnts(bndJnt, "jointArmsLoad_tfbg", "joint", "Root Upper Arm Joint",
                                  ["JNT", "BND", "upperArm"])

        geoJntArray = self.jointArray[:]
        cbSpecialStretch = mc.checkBox("selSpecialStretch_cb", q=True, v=True)

        grpDNTTorsoCheck = mc.textFieldButtonGrp("grpTorsoDNTLoad_tf", q=True, text=True)
        grpDNTTorso = CRU.tgpGetTx(grpDNTTorsoCheck, "grpTorsoDNTLoad_tf", "transform", "DO NOT TOUCH Torso Group",
                                   ["GRP", "DO_NOT_TOUCH", "torso"],
                                   "Group")

        ctrlRootCheck = mc.textFieldButtonGrp("rootTrans_tfbg", q=True, text=True)
        ctrlRoot = CRU.tgpGetTx(ctrlRootCheck, "rootTrans_tfbg", "nurbsCurve", "Root Control",
                                ["CTRL", "rootTransform"],
                                "control")

        jntShoulderRootCheck = mc.textFieldButtonGrp("jointShoulderJntLoad_tfbg", q=True, text=True)
        jntShoulderRoot = CRU.tgpGetTx(jntShoulderRootCheck, "jointShoulderJntLoad_tfbg", "joint",
                                       "Root Shoulder Joint",
                                       ["JNT", "BND", "shoulder"])

        jntIKShoulderCheck = mc.textFieldButtonGrp("jntIKShoulderLoad_tf", q=True, text=True)
        jntIKShoulder = CRU.tgpGetTx(jntIKShoulderCheck, "jntIKShoulderLoad_tf", "joint", "IK Shoulder Joint",
                                     ["JNT", "_IK_", "shoulder"])

        if checkToggleSpineStretch:
            grpSpineToggleCheck = mc.textFieldButtonGrp("grpheadShoulders_tfbg", q=True, text=True)
            grpSpineToggle = CRU.tgpGetTx(grpSpineToggleCheck, "grpheadShoulders_tfbg", "transform",
                                          "Head Shoulders Group", ["GRP", "head", "shoulders"],
                                          "group")

        if mirrorSel == 1:
            mirrorRig = False
        else:
            mirrorRig = True

        jntArmArray = bndJnts[:]

        if checkSelLeft == 1:
            isLeft = True
            leftRight = "l_"
            leftRightMirror = "r_"
            colourTU = CRU.clrLeftFK
            colourTUMirror = CRU.clrRightFK
            leftRight = self.valLeft
            leftRightMirror = self.valRight
        else:
            isLeft = False
            leftRight = "r_"
            leftRightMirror = "l_"
            colourTU = CRU.clrRightFK
            colourTUMirror = CRU.clrLeftFK
            leftRight = self.valRight
            leftRightMirror = self.valLeft

        toReplace = "_" + leftRight
        toReplaceWith = "_" + leftRightMirror

        # make sure the selections are not empty
        checkList = [bndJnts]
        if checkList is None:
            checkList = [bndJnts]

        if ((checkList[0] == "") or (checkList[0] is None)):
            mc.warning("You are missing a selection!")
            return
        else:

            # CRU.createLocatorToDelete()

            # checks if the starting joint is correct to the direction we want
            if not (CRU.checkLeftRight(isLeft, jntArmArray[0])):
                # if the values are not lined up properly, break out
                mc.warning("You are selecting the incorrect side for the root shoulder joint")
                return

            if mirrorRig:
                mirrorBase = mc.mirrorJoint(jntArmArray[0], mirrorYZ=True, mirrorBehavior=True,
                                            searchReplace=[toReplace, toReplaceWith])
                jntShoulderRootMirror = mc.mirrorJoint(jntShoulderRoot, mirrorYZ=True, mirrorBehavior=True,
                                                       searchReplace=[toReplace, toReplaceWith])[0]

                # mc.parent(jntShoulderRootMirror, w=True)
            self.makeArmComplete(isLeft, leftRight,
                                 jntArmArray,
                                 colourTU, jntShoulderRoot,
                                 jntIKShoulder, ctrlRoot,
                                 grpDNTTorso,
                                 grpSpineToggle,
                                 cbSpecialStretch, checkGeo, checkToggleSpineStretch,
                                 geoJntArray)

            if mirrorRig:

                print("Mirroring")
                isLeftMirror = not isLeft
                # we need to create mirror names for the arms
                jntArmArrayMirror = []
                for jntAA in jntArmArray:
                    jntArmArrayMirror.append(jntAA.replace(toReplace, toReplaceWith))

                geoJntArrayMirror = []
                for mb in mirrorBase:

                    if mc.objectType(mb) == "joint" and "End" not in mb:
                        geoJntArrayMirror.append(mb)
                self.makeArmComplete(isLeftMirror, leftRightMirror,
                                     jntArmArrayMirror,
                                     colourTUMirror, jntShoulderRootMirror,
                                     jntIKShoulder, ctrlRoot,
                                     grpDNTTorso,
                                     grpSpineToggle,
                                     cbSpecialStretch, checkGeo, checkToggleSpineStretch,
                                     geoJntArrayMirror)

            # reset the symmetry to the default because otherwise we might get wonky results
            mc.symmetricModelling(symmetry=symmetry)
