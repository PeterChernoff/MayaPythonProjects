'''
Created on May 30, 2014
for Tin Girl Book and game project

@author: Eyal Assaf
'''
import maya.cmds as mc
# import tgpUtils as ut
from functools import partial
from tgpBaseUI import BaseUI as UI

import pcCreateRig00AUtilities

import pcCreateRigAlt00AUtilities

reload(pcCreateRigAlt00AUtilities)
from pcCreateRigAlt00AUtilities import pcCreateRigUtilities as CRU


class pcCreateRigAlt05Arms(UI):
    def __init__(self):

        self.window = "bcWindow"
        self.title = "pcRigArms"
        self.winSize = (500, 475)

        self.createUI()

    def createCustom(self, *args):
        # selection type

        mc.rowColumnLayout(nc=2, cw=[(1, 500), (2, 500)], cs=[1, 5], rs=[1, 3])

        mc.text(l="Select The Shoulder Root: ")
        mc.text(l="")
        mc.separator(st="in", h=17, w=500)
        mc.setParent("..")
        mc.rowColumnLayout(nc=3, cw=[(1, 125), (2, 150), (3, 150)], cs=[1, 5], rs=[1, 3],
                           cal=([1, "left"], [2, "left"], [3, "left"],))

        mc.text(l="Mirror Arm As Well?")
        # mc.setParent("..")
        mc.radioButtonGrp("selArmMirrorType_rbg", la2=["No", "Yes"], nrb=2, sl=1, cw2=[50, 50], )
        mc.text(l="")
        mc.checkBox("selSpineEnd_cb", l="Connect To Spine", en=True, v=False)
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
        mc.textFieldButtonGrp("jointArmsLoad_tfbg", cw=(1, 322), bl="  Load  ")

        '''mc.text(bgc=(0.85, 0.65, 0.25), l="Shoulder Joint: ")
        mc.textFieldButtonGrp("jointShoulderLoad_tfbg", cw=(1, 322), bl="  Load  ")'''

        mc.text(bgc=(0.85, 0.65, 0.25), l="Shoulder IK Joint: ")
        mc.textFieldButtonGrp("jntIKShoulderLoad_tf", cw=(1, 322), bl="  Load  ", tx="JNT_IK_spine_6")

        mc.setParent("..")

        mc.separator(st="in", h=17, w=500)
        mc.rowColumnLayout(nc=2, cw=[(1, 100), (2, 380)], cs=[1, 5], rs=[1, 3])

        mc.text(bgc=(0.85, 0.65, 0.25), l="COG CTRL: ")
        mc.textFieldButtonGrp("ctrlCOG_tfbg", cw=(1, 322), bl="  Load  ", tx="CTRL_COG")

        mc.setParent("..")

        mc.separator(st="in", h=17, w=500)

        mc.rowColumnLayout(nc=2, cw=[(1, 100), (2, 370)], cs=[1, 5], rs=[1, 3])
        mc.checkBox("selGeo_cb", l="Affect Geometry", en=True, v=False)
        mc.setParent("..")

        # load buttons
        mc.textFieldButtonGrp("jointArmsLoad_tfbg", e=True, bc=self.loadSrc1Btn)
        # mc.textFieldButtonGrp("jointShoulderLoad_tfbg", e=True, bc=self.loadSrc2Btn)
        mc.textFieldButtonGrp("jntIKShoulderLoad_tf", e=True, bc=self.loadSrc3Btn)

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
        self.se2Src2 = self.tgpLoadJntsBtn("jointShoulderLoad_tfbg", "joint", "Root Shoulder Joint",
                                           ["JNT", "BND", "shoulder"])
        print(self.selSrc2)

    def loadSrc3Btn(self):
        self.selSrc3 = self.tgpLoadTxBtn("jntIKShoulderLoad_tf", "joint", "IK Shoulder Joint",
                                         ["JNT", "_IK_", "shoulder"])
        print(self.selSrc3)

    '''def loadSrc4Btn(self):
        self.selSrc4 = self.tgpLoadJntsBtn("ctrlIKChestLoad_tf", "nurbsCurve", "IK Chest Control",
                                           ["CTRL", "chest", "IK"],
                                           "control")
        print(self.selSrc4)'''

    def loadSrc5Btn(self):
        self.selSrc5 = self.tgpLoadTxBtn("ctrlCOG_tfbg", "nurbsCurve", "COG Control", ["CTRL", "COG"],
                                         "control")
        print(self.selSrc5)

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

            # removes if the last joint is End
            self.jointRoot = self.selLoad[0]

        return self.jointArray

    def tgpCreateLimbFKIFList(self, jntsTemp, textToReplace="", textReplacement="", stripLastVal=0, deleteThis=True,
                              renameThis=True, addToEnd="", *args):
        jntsReturn = []
        # creates a set of values. Normally, we want to delete, but we can also create a list from the values that simply don't include problematic node
        stripLastVal1 = stripLastVal * (-1)
        for i in range(len(jntsTemp)):
            toTest = jntsTemp[i]
            if mc.objectType(toTest) == "joint":
                if "Twist" in toTest:
                    if deleteThis:
                        mc.delete(toTest)
                else:
                    if stripLastVal1 == 0:
                        temp = toTest
                    else:
                        temp = toTest[:stripLastVal1]
                    toRename = temp.replace(textToReplace, textReplacement) + addToEnd  # strip off the last character
                    if renameThis:
                        mc.rename(toTest, toRename)
                    jntsReturn.append(toRename)
            else:
                if deleteThis:
                    mc.delete(toTest)

        return jntsReturn

    def tgpSetDriverArmFKIKSwitch(self, driver, driverAttr, driven, *args):
        w0w1Attr = mc.listAttr(driven)[-2:]
        CRU.setDriverDrivenValues(driver, driverAttr, driven, w0w1Attr[0], drivenValue=0, driverValue=1,
                                  modifyBoth="linear")
        CRU.setDriverDrivenValues(driver, driverAttr, driven, w0w1Attr[0], drivenValue=1, driverValue=0,
                                  modifyBoth="linear")
        CRU.setDriverDrivenValues(driver, driverAttr, driven, w0w1Attr[1], drivenValue=0, driverValue=0,
                                  modifyBoth="linear")
        CRU.setDriverDrivenValues(driver, driverAttr, driven, w0w1Attr[1], drivenValue=1, driverValue=1,
                                  modifyBoth="linear")

    def tgpAutoClavicleRotate(self, autoClav, targetLimb, ctrlClav, autoClavVal, *args):
        str = ""
        axes = ["X", "Y", "Z"]
        for ax in axes:
            # AUTO_CTRL_l_clavicle.rotateX = JNT_l_upperArm.rotateX * CTRL_l_clavicle.autoClavicle;
            str += "{0}.rotate{1} = {2}.rotate{1} * {3}.{4};\n".format(autoClav, ax, targetLimb, ctrlClav, autoClavVal)
        return str

    def makeArmSwitch(self, ctrlLimb, ctrlShoulder, ctrlChest, ctrlCOG, grpFollow, leftRight, colourTU, *args):
        locArmFollowArray = []
        locShoulder = "LOC_" + leftRight + "armShoulderFollow"
        locArmFollowArray.append(locShoulder)
        locTorso = "LOC_" + leftRight + "armTorsoFollow"
        locArmFollowArray.append(locTorso)
        locCOG = "LOC_" + leftRight + "armCOGFollow"
        locArmFollowArray.append(locCOG)
        locWorld = "LOC_" + leftRight + "armWorldFollow"
        locArmFollowArray.append(locWorld)

        listParents = [ctrlShoulder, ctrlChest, ctrlCOG, grpFollow]

        enumName = "fkArmFollow"
        enumVals = "shoulder:torso:COG:world"

        CRU.makeLimbSwitch(ctrlLimb, locArmFollowArray, listParents, enumName, enumVals, colourTU)

    def createSettings(self, jntArmArray, isLeft, name, colourTU, fkJnts, ikJnts, bndJnts, ctrlIKArm, *args):
        ctrlArmSettings = CRU.createNailNoOffset(jntArmArray[-2], isLeft, name, bodySize=15, headSize=2,
                                                 colour=colourTU,
                                                 pnt=True)

        grpSettings = "GRP_settings"
        if not mc.objExists(grpSettings):
            mc.group(n=grpSettings, w=True, em=True)
        mc.parent(ctrlArmSettings, grpSettings)
        CRU.layerEdit(grpSettings, newLayerName="settings_LYR", colourTU=9)

        # creates the FKIK blend control

        fkikBlendName = "fkik_blend"
        fkikBlendNiceName = "FK / IK Blend"
        # NOTE: we make the default value 0.5 for testing purposes
        mc.addAttr(ctrlArmSettings, longName=fkikBlendName, niceName=fkikBlendNiceName, at="float", k=True, min=0,
                   max=1, dv=0.5)

        CRU.makeBlendBasic(fkJnts, ikJnts, bndJnts, ctrlArmSettings, fkikBlendName, rotate=True, translate=True)
        # connect the visibility of the controllers
        fkVis = "FK_visibility"
        ikVis = "IK_visibility"

        mc.addAttr(ctrlArmSettings, longName=fkVis, at="bool", k=True)
        mc.addAttr(ctrlArmSettings, longName=ikVis, at="bool", k=True)
        mc.connectAttr("{0}.{1}".format(ctrlArmSettings, fkVis), "{0}.visibility".format(fkJnts[0]))
        mc.connectAttr("{0}.{1}".format(ctrlArmSettings, ikVis), "{0}.visibility".format(ikJnts[0]))
        mc.connectAttr("{0}.{1}".format(ctrlArmSettings, ikVis), "{0}.visibility".format(ctrlIKArm)) # this may need to be edited

        mc.setAttr("{0}.{1}".format(ctrlArmSettings, fkVis), True)
        mc.setAttr("{0}.{1}".format(ctrlArmSettings, ikVis), True)

        return ctrlArmSettings, fkikBlendName, fkVis, ikVis

    def bindArmTwists(self, twistJntsArrayOfArrays, leftRight, ikArms, *args):

        bindJntTwistStart = "JNT_{0}arm_bindStart".format(leftRight)
        bindJntTwistMid = "JNT_{0}arm_bindMid".format(leftRight)
        bindJntTwistEnd = "JNT_{0}arm_bindEnd".format(leftRight)

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

        ###########
        # bind the curves to the twists
        crvUpperArm = ikArms[0][2]
        crvLowerArm = ikArms[1][2]

        self.bindTwistControls(crvUpperArm, bindJntTwistStart, bindJntTwistMid)
        self.bindTwistControls(crvLowerArm, bindJntTwistMid, bindJntTwistEnd)
        ###########
        # activate the advanced Twist Control

        hdlUpperArm = ikArms[0][0]
        hdlLowerArm = ikArms[1][0]

        self.advancedTwistControls(hdlUpperArm, bindJntTwistStart, bindJntTwistMid)
        self.advancedTwistControls(hdlLowerArm, bindJntTwistMid, bindJntTwistEnd)
        ###########

        return bindJntTwistStart, bindJntTwistMid, bindJntTwistEnd

    def bindTwistControls(self, crvToUse, startJnt, endJnt):
        mc.select(crvToUse, endJnt, startJnt)
        skinName = crvToUse.replace("CRV_", "")
        skinName = skinName + "_skinCluster"

        # mc.skinCluster (ikHip, ikShoulder, crvSpine, sm=0, nw = 1)

        scls = mc.skinCluster(endJnt, startJnt, crvToUse, name=skinName, toSelectedBones=True,
                              bindMethod=0, skinMethod=0, normalizeWeights=1, maximumInfluences=2)[0]

    def advancedTwistControls(self, hdlArm, startJnt, endJnt):

        mc.setAttr('{0}.dTwistControlEnable'.format(hdlArm), True)

        # World Up Type to Object Rotation Up (Start/End)
        mc.setAttr('{0}.dWorldUpType'.format(hdlArm), 4)

        # forward to positive x
        mc.setAttr('{0}.dForwardAxis'.format(hdlArm), 0)

        # up to negative z
        mc.setAttr('{0}.dWorldUpAxis'.format(hdlArm), 4)

        # Up Vector and Up Vector 2 to 0, 0, 1
        mc.setAttr('{0}.dWorldUpVectorX'.format(hdlArm), 0)
        mc.setAttr('{0}.dWorldUpVectorY'.format(hdlArm), 0)
        mc.setAttr('{0}.dWorldUpVectorZ'.format(hdlArm), 1)

        mc.setAttr('{0}.dWorldUpVectorEndX'.format(hdlArm), 0)
        mc.setAttr('{0}.dWorldUpVectorEndY'.format(hdlArm), 0)
        mc.setAttr('{0}.dWorldUpVectorEndZ'.format(hdlArm), 1)

        # connects the joints to the right place
        mc.connectAttr(startJnt + ".worldMatrix[0]", hdlArm + ".dWorldUpMatrix")
        mc.connectAttr(endJnt + ".worldMatrix[0]", hdlArm + ".dWorldUpMatrixEnd")

        mc.setAttr('{0}.dTwistValueType'.format(hdlArm), 0)


    def makeFKStretch(self, fkJnts, *args):

        ctrlFKLengthKeyArray = []
        for i in range(len(fkJnts)):
            fkJnt = fkJnts[i]
            if "Arm" in fkJnt[-3:]:
                drivenAttr = "translateX"
                limbChild = mc.listRelatives(fkJnt, typ="joint")[0]
                legLen = mc.getAttr("{0}.{1}".format(limbChild, drivenAttr))
                length = "length"
                driverValue = 1
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

    def makeFKStretchGeo(self, bndJnt, crvArm, twistJnts):
        nameEdit = bndJnt.replace("JNT_BND_", "")

        crvInfo = nameEdit +"Info"
        armNormalizeDiv = nameEdit + "normalize_DIV"
        mc.shadingNode("curveInfo", n=crvInfo, au=True)
        mc.shadingNode("multiplyDivide", n=armNormalizeDiv, au=True)


        crvArmShape = mc.listRelatives(crvArm, s=True)[0]
        mc.connectAttr("{0}.worldSpace".format(crvArmShape), "{1}.inputCurve".format(crvArmShape, crvInfo))

        mc.setAttr("{0}.operation".format(armNormalizeDiv), 2)
        mc.connectAttr("{0}.arcLength".format(crvInfo), "{0}.input1X".format(armNormalizeDiv))

        armLen = mc.getAttr("{0}.tx".format(mc.listRelatives(bndJnt, type="joint")[0])) # get the joint child
        # divide arm length by its base length
        mc.setAttr("{0}.input2X".format(armNormalizeDiv),armLen)

        # connect to the segments' scaleX
        for i in range(len(twistJnts)-1):
            mc.connectAttr("{0}.outputX".format(armNormalizeDiv), "{0}.scaleX".format(twistJnts[i]))

    def makeIKHandle(self, ctrlIKArm, ikJnts, leftRight):
        mc.rotate( 0, 5, 0, ikJnts[1], r=True)
        mc.joint(ikJnts[1], e=True, spa=True) # set the preferred angle

        mc.rotate( 0, -5, 0, ikJnts[1], r=True)

        ikSolver = "ikRPsolver"
        ikSuffix = "arm"
        ikArms = CRU.createIKVal(ikJnts[0], ikJnts[-2], leftRight, ikSuffix, ikSolver) # create the IK arms

        ikSolver = "ikSCsolver"
        ikSuffix = "hand"
        ikHands = CRU.createIKVal(ikJnts[-2], ikJnts[-1], leftRight, ikSuffix, ikSolver) # create the IK hand

        mc.parent(ikArms[0], ikHands[0], ctrlIKArm)

        mc.nodePreset(save=(ctrlIKArm, "smithers"))


        return ikArms, ikHands
    def makeIKStretch(self, bindJntTwistStart, bindJntTwistEnd, ikJnts, ctrlIKArm, leftRight):

        if leftRight == self.valLeft:
            # need to make adjustments for the values making a mirror
            m = 1
        else:
            m = -1

        locIKDistStart = "loc_{0}arm_IK_lengthStart".format(leftRight)
        locIKDistEnd = "loc_{0}arm_IK_lengthEnd".format(leftRight)
        distIKLen= "dist_{0}arm_IK_length".format(leftRight)



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

        return locIKDistStart, locIKDistEnd, distIKLen, distIKLenShape, ctrlIKLengthKeyArray

    def makeElbowCtrl(self, leftRight, ikJnts, *args):
        locElbow = "loc_{0}elbow".format(leftRight)
        mc.spaceLocator(p=(0, 0, 0), name=locElbow)[0]
        toDelete = mc.pointConstraint(ikJnts[1], locElbow)
        mc.delete(toDelete)
        armLength = mc.getAttr("{0}.tx".format(ikJnts[1]))
        mc.move(-armLength/2, locElbow, z=True, os=True)

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

        return locElbow, ctrlElbow
    def makeArmComplete(self, isLeft, leftRight,
                        jntArmArray,
                        colourTU, jntShoulderRoot,
                        ctrlIKShoulder,
                        checkboxSpine, checkGeo,
                        geoJntArray, *args):

        uArmLen = mc.getAttr("{0}.tx".format(mc.listRelatives(jntArmArray[0])[0]))
        lArmLen = mc.getAttr("{0}.tx".format(mc.listRelatives(jntArmArray[1])[0]))

        # Creating FK and IK Joints
        bndJnts, fkJnts, ikJnts = self.getBndFkIkJnts(jntArmArray)

        fkLayer = "{0}arm_FK_lyr".format(leftRight)
        ikLayer = "{0}arm_IK_lyr".format(leftRight)
        CRU.layerEdit(fkJnts, newLayerName=fkLayer)
        CRU.layerEdit(ikJnts, newLayerName=ikLayer)

        # we want to create FK controls for the limbs except the end
        fkJnts = self.createArmFKs(fkJnts, )

        # create the IK control without attaching it to anything
        name = "{0}arm".format(leftRight)
        ctrlIKArm = CRU.setupCtrl(name, colour=colourTU, addPrefix=True, boxDimensionsLWH=(3, 6, 6))[0]
        todelete = mc.pointConstraint(ikJnts[-2], ctrlIKArm)
        mc.delete(todelete)
        rotOrderTemp = mc.getAttr("{0}.rotateOrder".format(ikJnts[-2]))
        mc.setAttr("{0}.rotateOrder".format(ctrlIKArm), rotOrderTemp)


        ######
        # to delete test
        # if this works, delete the notes, otherwise delete this part
        # I want to see how 0-out the IK control works. If things mess up, try not including this step

        mc.makeIdentity(ctrlIKArm, apply=True, t=True, r=True, s=True)

        #####
        # create the settings control
        name = "settings_" + leftRight + "arm"
        ctrlArmSettings, fkikBlendName, fkVis, ikVis = self.createSettings(jntArmArray, isLeft, name, colourTU, fkJnts,
                                                                           ikJnts, bndJnts, ctrlIKArm)

        ##########
        # Twistable segments
        # Adding the twist joints
        # twistJntsArrayOfArrays is an array of arrays
        geoJntArray, twistJntsArrayOfArrays = self.makeTwists(5, jntArmArray, geoJntArray)
        grpArmTwist = "GRP_{0}armTwist".format(leftRight)
        mc.group(n=grpArmTwist, em=True, w=True)

        ikUpperArm = self.makeCrvSpline(twistJntsArrayOfArrays[0], leftRight, "upperArm", grpArmTwist)
        ikLowerArm = self.makeCrvSpline(twistJntsArrayOfArrays[1], leftRight, "lowerArm", grpArmTwist)

        ikArms = [ikUpperArm, ikLowerArm]
        crvArms = [ikUpperArm[2], ikLowerArm[2]]

        bindJntTwistStart, bindJntTwistMid, bindJntTwistEnd = self.bindArmTwists(twistJntsArrayOfArrays, leftRight,
                                                                                 ikArms)
        # upperArm parentConstraints start, lowerArm parentConstraints mid, hand parentConstraints end
        mc.parentConstraint(jntArmArray[0], bindJntTwistStart)
        mc.parentConstraint(jntArmArray[1], bindJntTwistMid)
        mc.parentConstraint(jntArmArray[2], bindJntTwistEnd)

        # temp to delete this geo binding
        CRU.tgpSetGeo(geoJntArray, setLayer=True, printOut=False)

        ##########
        # FK Stretch
        ctrlFKLengthKeyArray = self.makeFKStretch(fkJnts)
        # FK Scale Geometry
        self.makeFKStretchGeo(bndJnts[0], crvArms[0], twistJntsArrayOfArrays[0])
        self.makeFKStretchGeo(bndJnts[1], crvArms[1], twistJntsArrayOfArrays[1])
        ##########


        ##########
        # IK Arm
        ikArms, ikHands = self.makeIKHandle(ctrlIKArm, ikJnts, leftRight)

        # IK Stretch
        vals = self.makeIKStretch(bindJntTwistStart, bindJntTwistEnd, ikJnts, ctrlIKArm, leftRight)
        locIKDistArmStart, locIKDistArmEnd, distIKArmLen, distIKArmLenShape, ctrlIKArmLengthKeyArray = vals

        ##########

        ##########
        # Snappable elbow
        # Elbow
        locElbow, ctrlElbow = self.makeElbowCtrl(leftRight, ikJnts, )


        # Elbow Snap
        self.makeElbowSnap(ctrlElbow, ikJnts, leftRight)
        ##########




        return
        # NOTE: I use a slightly different order than the originals, leaving the SetGeo section to the lat

        fkLen = len(fkJnts)
        ikLen = len(ikJnts)
        bndLen = len(bndJnts)

        if bndLen != fkLen or bndLen != ikLen:
            mc.warning("Your arm joints are somehow not equal")
            return
        else:
            ikFkJntConstraints = []
            for i in range(bndLen):
                temp = mc.orientConstraint(fkJnts[i], ikJnts[i], bndJnts[i])[0]
                ikFkJntConstraints.append(temp)

        for i in range(len(ikFkJntConstraints)):
            self.tgpSetDriverArmFKIKSwitch(ctrlFKIKAttr, ikFkJntConstraints[i])

        # create the shoulder control
        shoulderOffsetCtrl = self.setupShoulder(jntShoulderRoot, bndJnts, fkJntOffsetCtrls, colourTU)

        # create the clavicle
        if jntClavicle:
            clavicleOffsetCtrl = self.setupClavicle(jntClavicle, colourTU, leftRight, shoulderOffsetCtrl, jntArmArray)

        # create the scapula
        if jntScapula:
            scapulaOffsetCtrl = self.setupScapula(jntScapula, colourTU, leftRight, shoulderOffsetCtrl, )

        # for testing purposes only, setting the IK to active:
        mc.setAttr("{0}.{1}".format(ctrlFKIKAttr), 0.5)

        # Setting up the IK Arm
        ikOffsetCtrl, ikArms, ikJntsDrive, ikSide = self.createArmIK(ikJnts, leftRight, colourTU, isLeft)
        # create the twists
        self.setupIkElblowArmTwist(ikOffsetCtrl, ikJnts, ikArms, isLeft)

        # change the rotation order
        rotationChange = [ikJnts[1], jntArmArray[1], fkJnts[1], ikJntsDrive[1], fkJntOffsetCtrls[1][1]]

        CRU.changeRotateOrder(rotationChange, "YZX")

        # Adding the Elbow Control
        elbowOffsetCtrl = self.createElbow(ikJntsDrive, leftRight, armLength, ikArms, isLeft, colourTU, )

        # Adding Space Switching
        # NOTE: This is something I added from the finalizing section
        if checkboxSwitch:
            # self.makeArmSwitch(ctrlLimb, ctrlShoulder, ctrlChest, ctrlCOG, grpFollow, leftRight, colourTU)
            self.makeArmSwitch(fkJntOffsetCtrls[0][1], shoulderOffsetCtrl[1], ctrlIKChest, ctrlCOG, grpFollow,
                               leftRight, colourTU)
        # Organize the rig
        self.armCleanUp(fkJnts, ikJnts, ikJntsDrive, bndJnts,
                        jntShoulderRoot, jntScapula, jntClavicle,
                        checkboxSpine,
                        shoulderOffsetCtrl, scapulaOffsetCtrl, clavicleOffsetCtrl,
                        ikOffsetCtrl, elbowOffsetCtrl, ikArms, ctrlIKShoulder,
                        ikSide, fkJntOffsetCtrls, ctrlFKIKAttr)

        if checkGeo:
            CRU.tgpSetGeo(geoJntArray, setLayer=True)

    def makeTwists(self, numTwists, jntArmArray, geoJntArray, *args):
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

    def setupShoulder(self, jntShoulderRoot, bndJnts, fkJntOffsetCtrls, colourTU, *args):
        shoulderOffsetCtrl = CRU.createCTRLs(jntShoulderRoot, size=5, ornt=True, colour=colourTU)
        shoulderLength = mc.getAttr("{0}.ty".format(bndJnts[0]))

        mc.select(shoulderOffsetCtrl[1] + ".cv[:]")
        mc.move(-shoulderLength * 0.65, shoulderLength * 0.8, 0, r=True, ls=True)

        mc.parent(fkJntOffsetCtrls[0][0], shoulderOffsetCtrl[1])

        return shoulderOffsetCtrl

    def setupClavicle(self, jointClavicle, colourTU, leftRight, shoulderOffsetCtrl, jntArmArray, *args):
        jntClav = jointClavicle[0]
        childClavicle = mc.listRelatives(jntClav, c=True, type="joint")[0]
        clavLength = mc.getAttr("{0}.ty".format(childClavicle))
        clavicleOffsetCtrl = CRU.createCTRLs(jntClav, size=6, ornt=True, colour=colourTU, orientVal=(0, 0, 1),
                                             sectionsTU=6)
        mc.select(clavicleOffsetCtrl[1] + ".cv[:]")
        mc.move(clavLength * 0.5, clavLength * 0.5, 0, r=True, ls=True)
        autoAttrName = "autoClavicle"
        mc.addAttr(clavicleOffsetCtrl, longName=autoAttrName, at="float", k=True, min=0, max=1, dv=0.05)
        autoName = clavicleOffsetCtrl[2]
        xprNameClav = "expr_" + leftRight + "clavicle"

        # AUTO_CTRL_l_clavicle.rotateX = JNT_l_upperArm.rotateX * CTRL_l_clavicle.autoClavicle;
        exprStringClav = self.tgpAutoClavicleRotate(autoName, jntArmArray[0], clavicleOffsetCtrl[1],
                                                    autoAttrName)

        mc.expression(s=exprStringClav, n=xprNameClav)
        mc.parent(clavicleOffsetCtrl[0], shoulderOffsetCtrl[1])

        return clavicleOffsetCtrl

    def setupScapula(self, jointScapula, colourTU, leftRight, shoulderOffsetCtrl, *args):
        jntScap = jointScapula[0]
        childScap = mc.listRelatives(jntScap, c=True, type="joint")[0]
        scapLength = mc.getAttr("{0}.ty".format(childScap))
        scapulaOffsetCtrl = CRU.createCTRLs(jntScap, size=6, ornt=True, colour=colourTU, orientVal=(1, 0, 0),
                                            sectionsTU=8)

        mc.select(scapulaOffsetCtrl[1] + ".cv[:]")
        mc.move(-scapLength * 0.5, scapLength * 0.5, 0, r=True, ls=True)
        autoAttrName = "autoScapula"
        mc.addAttr(scapulaOffsetCtrl, longName=autoAttrName, at="float", k=True, min=0, max=1, dv=0.5)
        autoName = scapulaOffsetCtrl[2]
        xprNameScap = "expr_" + leftRight + "scapula"

        # AUTO_CTRL_l_scapula.rotateX = -1*CTRL_l_shoulder.rotateZ * CTRL_l_scapula.autoScapula;
        exprStringScap = "{0}.rotateX = -1*{1}.rotateZ * {2}.{3};\n".format(autoName, shoulderOffsetCtrl[1],
                                                                            scapulaOffsetCtrl[1], autoAttrName)

        mc.expression(s=exprStringScap, n=xprNameScap)
        mc.parent(scapulaOffsetCtrl[0], shoulderOffsetCtrl[1])

        return scapulaOffsetCtrl

    def createArmIK(self, ikJnts, leftRight, colourTU, isLeft, *args):

        ikJntsTDriveTemp = mc.duplicate(ikJnts[0], rc=True)
        ikJntsDrive = self.tgpCreateLimbFKIFList(ikJntsTDriveTemp, addToEnd="Drive", stripLastVal=1)

        ikSide = leftRight + "arm"

        ikArmName = "IK_" + ikSide
        effArmName = "EFF_" + ikSide
        ikArms = mc.ikHandle(n=ikArmName, sj=ikJntsDrive[0], ee=ikJntsDrive[-1], sol="ikRPsolver")
        mc.rename(ikArms[1], effArmName)
        ikArms[1] = effArmName

        # fkJntOffsetCtrls.append(CRU.createCTRLs(temp, size=9, ornt=True, colour=colourTU, orientVal=(0, 1, 0)))
        ikOffsetCtrl = CRU.createCTRLs(ikArms[0], pnt=True, colour=colourTU, addPrefix=True, boxDimensionsLWH=[5, 5, 5])

        fkOrntUpperArm1 = mc.orientConstraint(ikJntsDrive[0], ikJnts[0])[0]
        fkOrntLowerArm1 = mc.orientConstraint(ikJntsDrive[1], ikJnts[1], skip="y")[0]

        return ikOffsetCtrl, ikArms, ikJntsDrive, ikSide

    def armCleanUp(self, fkJnts, ikJnts, ikJntsDrive, bndJnts,
                   jntShoulderRoot, jntScapula, jntClavicle,
                   checkboxSpine,
                   shoulderOffsetCtrl, scapulaOffsetCtrl, clavicleOffsetCtrl,
                   ikOffsetCtrl, elbowOffsetCtrl, ikArms, ctrlIKShoulder, ikSide, fkJntOffsetCtrls,
                   ctrlFKIKAttr, *args):

        mc.parent(fkJnts[0], ikJnts[0], ikJntsDrive[0], jntShoulderRoot)

        if checkboxSpine:
            mc.parentConstraint(ctrlIKShoulder, shoulderOffsetCtrl[0], mo=True)

        mc.pointConstraint(shoulderOffsetCtrl[1], jntShoulderRoot)

        # group OFFSET_CTRL_IK_l_arm, OFFSET_CTRL_l_elbow into GRP_CTRL_IK_l_arm
        ikGrpCtrlName = "GRP_CTRL_IK_" + ikSide
        ikGrpCtrl = mc.group(n=ikGrpCtrlName, w=True, em=True)

        mc.parent(ikOffsetCtrl[0], elbowOffsetCtrl[0], ikGrpCtrl)

        # group IK_l_arm, JNT_l_shouder into GRP_jnt_l_arm
        armGrpRigName = "GRP_jnt_" + ikSide
        armRigGrp = mc.group(n=armGrpRigName, w=True, em=True)

        mc.parent(ikArms[0], jntShoulderRoot, armRigGrp)

        # creating lists to set invisible
        fksToVisible = [fkJntOffsetCtrls[0][1], fkJnts[0]]
        iksToVisible = [ikOffsetCtrl[1], ikJnts[0], ikJntsDrive[0], elbowOffsetCtrl[1]]
        tangentToUse = ["linear", "step"]
        visMin = 0.001

        # set the FK to visible when not ctrlFKIK not 1 for arm attribute
        for i in range(len(fksToVisible)):
            CRU.setDriverDrivenValues(ctrlFKIK, ctrlFKIKAttr, fksToVisible[i], "visibility", drivenValue=True,
                                      driverValue=0, modifyInOut=tangentToUse)
            CRU.setDriverDrivenValues(ctrlFKIK, ctrlFKIKAttr, fksToVisible[i], "visibility", drivenValue=True,
                                      driverValue=1 - visMin, modifyInOut=tangentToUse)
            CRU.setDriverDrivenValues(ctrlFKIK, ctrlFKIKAttr, fksToVisible[i], "visibility", drivenValue=False,
                                      driverValue=1, modifyInOut=tangentToUse)

        tangentToUse = ["linear", "step"]
        # set the IK to visible when not ctrlFKIK not 0 for arm attribute
        for i in range(len(iksToVisible)):
            CRU.setDriverDrivenValues(ctrlFKIK, ctrlFKIKAttr, iksToVisible[i], "visibility", drivenValue=False,
                                      driverValue=0, modifyInOut=tangentToUse)
            CRU.setDriverDrivenValues(ctrlFKIK, ctrlFKIKAttr, iksToVisible[i], "visibility", drivenValue=True,
                                      driverValue=visMin, modifyInOut=tangentToUse)
            CRU.setDriverDrivenValues(ctrlFKIK, ctrlFKIKAttr, iksToVisible[i], "visibility", drivenValue=True,
                                      driverValue=1, modifyInOut=tangentToUse)

        # locking and hiding the IK controls
        CRU.lockHideCtrls(ikOffsetCtrl[1], rotate=True, scale=True, visible=True)
        for fkJntOC in fkJntOffsetCtrls:
            CRU.lockHideCtrls(fkJntOC[1], translate=True, scale=True)
            CRU.lockHideCtrls(fkJntOC[1], visible=True, toLock=False)
        CRU.lockHideCtrls(shoulderOffsetCtrl[1], translate=True, scale=True, visible=True)
        CRU.lockHideCtrls(scapulaOffsetCtrl[1], translate=True, scale=True, visible=True)
        CRU.lockHideCtrls(clavicleOffsetCtrl[1], translate=True, scale=True, visible=True)
        CRU.lockHideCtrls(elbowOffsetCtrl[1], rotate=True, scale=True, visible=True)

        # hiding the visibility for the FK

        # locking and hiding the effectors and IK
        # to delete: May need to not have this hidden
        mc.setAttr("{0}.visibility".format(ikArms[0]), False)
        CRU.lockHideCtrls(ikArms[0], visible=True)
        CRU.lockHideCtrls(ikArms[1], visible=True)

        CRU.layerEdit(ikJnts, ikLayer=True, noRecurse=True)
        CRU.layerEdit(fkJnts, fkLayer=True, noRecurse=True)
        CRU.layerEdit(ikJntsDrive, ikdriveLayer=True, noRecurse=True)
        CRU.layerEdit(bndJnts, bndLayer=True, noRecurse=True)
        CRU.layerEdit(jntShoulderRoot, bndLayer=True, noRecurse=True)
        CRU.layerEdit(jntScapula, bndLayer=True, noRecurse=True)
        CRU.layerEdit(jntClavicle, bndLayer=True, noRecurse=True)

    def tgpMakeBC(self, *args):

        checkSelLeft = mc.radioButtonGrp("selArmType_rbg", q=True, select=True)
        mirrorSel = mc.radioButtonGrp("selArmMirrorType_rbg", q=True, select=True)

        checkGeo = mc.checkBox("selGeo_cb", q=True, v=True)

        # self.jntNames = mc.textFieldButtonGrp("jointShoulderLoad_tfbg", q=True, text=True)
        self.jntNames = mc.textFieldButtonGrp("jointArmsLoad_tfbg", q=True, text=True)
        geoJntArray = self.jointArray[:]
        checkboxSpine = mc.checkBox("selSpineEnd_cb", q=True, v=True)

        ctrlCOG = mc.textFieldButtonGrp("ctrlCOG_tfbg", q=True, text=True)

        self.valLeft = "l_"
        self.valRight = "r_"

        if checkboxSpine:
            ctrlIKShoulder = mc.textFieldButtonGrp("jntIKShoulderLoad_tf", q=True, text=True)
        else:
            ctrlIKShoulder = None

        if mirrorSel == 1:
            mirrorRig = False
        else:
            mirrorRig = True

        jntArmArray = self.jointArray[:]

        if checkSelLeft == 1:
            isLeft = True
            leftRight = "l_"
            leftRightMirror = "r_"
            colourTU = 14
            colourTUMirror = 13
            leftRight = self.valLeft
            leftRightMirror = self.valRight
        else:
            isLeft = False
            leftRight = "r_"
            leftRightMirror = "l_"
            colourTU = 13
            colourTUMirror = 14
            leftRight = self.valRight
            leftRightMirror = self.valLeft

        toReplace = "_" + leftRight
        toReplaceWith = "_" + leftRightMirror

        # make sure the selections are not empty
        checkList = [self.jntNames]

        if ((checkList[0] == "")):
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

                jntShoulderRootMirror = mirrorBase[0]
                # mc.parent(jntShoulderRootMirror, w=True)
            jntShoulderRoot = "toDelete"
            self.makeArmComplete(isLeft, leftRight,
                                 jntArmArray,
                                 colourTU, jntShoulderRoot,
                                 ctrlIKShoulder,
                                 checkboxSpine, checkGeo,
                                 geoJntArray)

            if mirrorRig:

                print("Mirroring")

                isLeftMirror = not isLeft
                # we need to create mirror names for the arms
                jntArmArrayMirror = []
                for jntAA in jntArmArray:
                    jntArmArrayMirror.append(jntAA.replace(toReplace, toReplaceWith))
                jntClavicleMirror = []
                for clav in jntClavicle:
                    jntClavicleMirror.append(clav.replace(toReplace, toReplaceWith))
                jntScapulaMirror = []
                for scap in jntScapula:
                    jntScapulaMirror.append(scap.replace(toReplace, toReplaceWith))
                geoJntArrayMirror = []
                for mb in mirrorBase:

                    if mc.objectType(mb) == "joint" and "End" not in mb:
                        geoJntArrayMirror.append(mb)
                self.makeArmComplete(isLeftMirror, leftRightMirror,
                                     jntArmArrayMirror, jntClavicleMirror, jntScapulaMirror,
                                     colourTUMirror, jntShoulderRootMirror,
                                     ctrlFKIKAttrMirror, ctrlIKShoulder, checkboxTwists,
                                     checkboxSpine, checkGeo,
                                     checkboxSwitch, ctrlIKChest, ctrlCOG, grpFollow,
                                     geoJntArrayMirror)
