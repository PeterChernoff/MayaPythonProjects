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

import pcCreateRig00AUtilities

reload(pcCreateRig00AUtilities)
from pcCreateRig00AUtilities import pcCreateRigUtilities as CRU


class pcCreateRig11SpaceSwitching(UI):
    def __init__(self):

        self.window = "bcWindow"
        self.title = "pcSpaceSwitching"
        self.winSize = (500, 600)

        self.createUI()

    def createCustom(self, *args):
        # selection type

        mc.rowColumnLayout(nc=2, cw=[(1, 500), (2, 500)], cs=[1, 5], rs=[1, 1])
        mc.text(l="Select The Upper Arm and/or Leg FK: ")
        mc.text(l="")
        mc.separator(st="in", h=17, w=500)
        mc.setParent("..")

        mc.rowColumnLayout(nc=3, cw=[(1, 125), (2, 150), (3, 150)], cs=[1, 5], rs=[1, 1],
                           cal=([1, "left"], [2, "left"], [3, "left"],))
        mc.text(l="Mirror Limb(s) As Well?")
        # mc.setParent("..")
        mc.radioButtonGrp("selLegMirrorType_rbg", la2=["No", "Yes"], nrb=2, sl=2, cw2=[50, 50], )
        mc.text(l="")
        mc.setParent("..")
        mc.separator(st="in", h=10, w=500)

        mc.rowColumnLayout(nc=4, cw=[(1, 125), (2, 150), (3, 150), (4, 150)], cs=[1, 5], rs=[1, 1],
                           cal=([1, "left"], [2, "left"], [3, "left"], [4, "left"],))
        mc.text(l="Limbs to Use:")
        # mc.setParent("..")
        mc.radioButtonGrp("selLimbSideType_rbg", la3=["Arm", "Leg", "Both"], nrb=3, sl=3, cw3=[50, 50, 50], )
        mc.text(l="")
        mc.setParent("..")
        mc.separator(st="in", h=10, w=500)

        mc.rowColumnLayout(nc=3, cw=[(1, 100), (2, 200), (3, 150)], cs=[1, 5], rs=[1, 3],
                           cal=([1, "left"], [2, "left"], [3, "left"],))
        mc.text(l="Initial Limb: ")
        mc.radioButtonGrp("selLeftRight_rbg", la2=["Left", "Right"], nrb=2, sl=1, cw2=[50, 50], )
        mc.setParent("..")
        mc.separator(st="in", h=10, w=500)

        # sources
        mc.rowColumnLayout(nc=2, cw=[(1, 100), (2, 380)], cs=[1, 5], rs=[1, 3])
        mc.text(bgc=(0.85, 0.65, 0.25), l="Upper Arm FK: ")
        mc.textFieldButtonGrp("ctrlArm_tfbg", cw=(1, 322), bl="  Load  ", tx="CTRL_FK_l_upperArm")

        mc.text(bgc=(0.85, 0.65, 0.25), l="Shoulder CTRL: ")
        mc.textFieldButtonGrp("ctrlShoulder_tfbg", cw=(1, 322), bl="  Load  ", tx="CTRL_l_shoulder")

        mc.text(bgc=(0.85, 0.65, 0.25), l="IK Chest CTRL: ")
        mc.textFieldButtonGrp("ctrlIKChestLoad_tf", cw=(1, 322), bl="  Load  ", tx="CTRL_IK_chest")

        mc.setParent("..")

        mc.separator(st="in", h=10, w=500)

        mc.rowColumnLayout(nc=2, cw=[(1, 100), (2, 380)], cs=[1, 5], rs=[1, 3])
        mc.text(bgc=(0.85, 0.65, 0.25), l="Upper Leg FK: ")
        mc.textFieldButtonGrp("ctrlLeg_tfbg", cw=(1, 322), bl="  Load  ", tx="CTRL_FK_l_upperLeg")

        mc.text(bgc=(0.85, 0.65, 0.25), l="FK Hip CTRL: ")
        mc.textFieldButtonGrp("ctrlFKHip_tfbg", cw=(1, 322), bl="  Load  ", tx="CTRL_FK_hip")

        mc.text(bgc=(0.85, 0.65, 0.25), l="IK Hip CTRL: ")
        mc.textFieldButtonGrp("ctrlIKHip_tfbg", cw=(1, 322), bl="  Load  ", tx="CTRL_IK_hip")

        mc.setParent("..")

        mc.separator(st="in", h=10, w=500)

        mc.rowColumnLayout(nc=2, cw=[(1, 100), (2, 380)], cs=[1, 5], rs=[1, 3])

        mc.text(bgc=(0.85, 0.65, 0.25), l="COG CTRL: ")
        mc.textFieldButtonGrp("ctrlCOG_tfbg", cw=(1, 322), bl="  Load  ", tx="CTRL_COG")

        mc.text(bgc=(0.85, 0.65, 0.25), l="Group LOC Follow: ")
        mc.textFieldButtonGrp("grpLOCFollow_tfbg", cw=(1, 322), bl="  Load  ", tx="GRP_LOC_follow")

        mc.setParent("..")

        mc.separator(st="in", h=10, w=500)

        # load buttons
        #

        mc.textFieldButtonGrp("ctrlArm_tfbg", e=True, bc=self.loadSrc1Btn)
        mc.textFieldButtonGrp("ctrlShoulder_tfbg", e=True, bc=self.loadSrc2Btn)
        mc.textFieldButtonGrp("ctrlIKChestLoad_tf", e=True, bc=self.loadSrc3Btn)

        mc.textFieldButtonGrp("ctrlLeg_tfbg", e=True, bc=self.loadSrc4Btn)
        mc.textFieldButtonGrp("ctrlFKHip_tfbg", e=True, bc=self.loadSrc5Btn)
        mc.textFieldButtonGrp("ctrlIKHip_tfbg", e=True, bc=self.loadSrc6Btn)

        mc.textFieldButtonGrp("ctrlCOG_tfbg", e=True, bc=self.loadSrc7Btn)
        mc.textFieldButtonGrp("grpLOCFollow_tfbg", e=True, bc=self.loadSrc8Btn)

        self.selLoad = []
        self.locArray = []
        mc.showWindow(self.window)

    def createButtonCmd(self, *args):
        self.tgpMakeBC()

    def loadSrc1Btn(self):
        self.selSrc1 = self.tgpLoadTxBtn("ctrlArm_tfbg", "nurbsCurve", "Upper Arm FK", ["CTRL", "FK", "upperArm"])
        print(self.selSrc1)

    def loadSrc2Btn(self):
        self.selSrc2 = self.tgpLoadTxBtn("ctrlShoulder_tfbg", "nurbsCurve", "Shoulder Control", ["CTRL", "shoulder"],
                                         "control")
        print(self.selSrc2)

    def loadSrc3Btn(self):
        self.selSrc3 = self.tgpLoadTxBtn("ctrlIKChestLoad_tf", "nurbsCurve", "IK Chest Control",
                                         ["CTRL", "chest", "IK"],
                                         "control")
        print(self.selSrc3)

    def loadSrc4Btn(self):
        self.selSrc4 = self.tgpLoadTxBtn("ctrlLeg_tfbg", "nurbsCurve", "Upper Leg FK", ["CTRL", "FK", "upperLeg"])
        print(self.selSrc4)

    def loadSrc5Btn(self):
        self.selSrc5 = self.tgpLoadTxBtn("ctrlFKHip_tfbg", "nurbsCurve", "FK Hip Control", ["CTRL", "FK", "hip"],
                                         "control")
        print(self.selSrc5)

    def loadSrc6Btn(self):
        self.selSrc6 = self.tgpLoadTxBtn("ctrlIKHip_tfbg", "nurbsCurve", "IK Hip Control", ["CTRL", "hip", "IK"],
                                         "control")
        print(self.selSrc6)

    def loadSrc7Btn(self):
        self.selSrc7 = self.tgpLoadTxBtn("ctrlCOG_tfbg", "nurbsCurve", "COG Control", ["CTRL", "COG"],
                                         "control")
        print(self.selSrc7)

    def loadSrc8Btn(self):
        self.selSrc8 = self.tgpLoadTxBtn("grpLOCFollow_tfbg", "transform", "World Follow Group",
                                         ["GRP", "LOC", "follow"],
                                         "group")
        print(self.selSrc8)

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

    def makeLimb(self, ctrlLimb, locLimbFollowArray, listParents, enumName, enumVals, colourTU, *args):

        # get the auto_ctrl of the limb
        autoCtrlLimb = mc.listRelatives(ctrlLimb, p=True, c=False)[0]

        for i in range(len(locLimbFollowArray)):
            # creates locator, then moves to upperArm FK control
            locName = locLimbFollowArray[i]

            mc.spaceLocator(p=(0, 0, 0), name=locName)
            locShape = mc.listRelatives(locName, s=True)[0]

            mc.setAttr("{0}.localScaleX".format(locShape), 15)

            mc.setAttr("{0}.localScaleY".format(locShape), 15)
            mc.setAttr("{0}.localScaleZ".format(locShape), 15)

            mc.setAttr('{0}.overrideEnabled'.format(locName), 1)
            mc.setAttr("{0}.overrideColor".format(locName), colourTU)

            toDelete = mc.parentConstraint(ctrlLimb, locName)[0]
            mc.delete(toDelete)
            mc.parent(locName, listParents[i])

        mc.addAttr(ctrlLimb, longName=enumName, at="enum", k=True, en=enumVals)
        # create oreient constraints for the arm locators
        limbFollowOrntConstr = mc.orientConstraint(locLimbFollowArray, autoCtrlLimb, mo=True)[0]

        limbSpaceFollow = mc.listAttr(limbFollowOrntConstr)[-4:]
        for i in range(len(limbSpaceFollow)):
            # set the driven key to 1 and the undriven keys to 0

            CRU.setDriverDrivenValues(ctrlLimb, enumName, limbFollowOrntConstr, limbSpaceFollow[i], i, 1)
            for i2 in range(len(limbSpaceFollow)):
                if i2 != i:
                    # need to have the second to last value be i, not i2
                    CRU.setDriverDrivenValues(ctrlLimb, enumName, limbFollowOrntConstr, limbSpaceFollow[i2], i, 0)

        for i in range(len(locLimbFollowArray)):
            mc.setAttr("{0}.visibility".format(locLimbFollowArray[i]), False)
            CRU.lockHideCtrls(locLimbFollowArray[i], scale=True, visible=True)

    def makeArm(self, ctrlLimb, ctrlShoulder, ctrlChest, ctrlCOG, grpFollow, leftRight, colourTU, *args):
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

        self.makeLimb(ctrlLimb, locArmFollowArray, listParents, enumName, enumVals, colourTU)

    def makeLeg(self, ctrlLimb, ctrlHipFK, ctrlHipIK, ctrlCOG, grpFollow, leftRight, colourTU, *args):

        locArmFollowArray = []
        locShoulder = "LOC_" + leftRight + "legFKHipFollow"
        locArmFollowArray.append(locShoulder)
        locTorso = "LOC_" + leftRight + "legIKHipFollow"
        locArmFollowArray.append(locTorso)
        locCOG = "LOC_" + leftRight + "legCOGFollow"
        locArmFollowArray.append(locCOG)
        locWorld = "LOC_" + leftRight + "legWorldFollow"
        locArmFollowArray.append(locWorld)

        listParents = [ctrlHipFK, ctrlHipIK, ctrlCOG, grpFollow]

        enumName = "fkLegFollow"
        enumVals = "fkHip:ikHip:COG:world"

        self.makeLimb(ctrlLimb, locArmFollowArray, listParents, enumName, enumVals, colourTU)

    def tgpMakeBC(self, *args):

        mirrorSel = mc.radioButtonGrp("selLegMirrorType_rbg", q=True, select=True)
        limbType = mc.radioButtonGrp("selLimbSideType_rbg", q=True, select=True)
        checkSelLeft = mc.radioButtonGrp("selLeftRight_rbg", q=True, select=True)

        if limbType == 1:
            useArm = True
            useLeg = False
        elif limbType == 2:
            useArm = False
            useLeg = True
        else:
            useLeg = True
            useArm = True

        ctrlArm = mc.textFieldButtonGrp("ctrlArm_tfbg", q=True, text=True)
        ctrlShoulder = mc.textFieldButtonGrp("ctrlShoulder_tfbg", q=True, text=True)
        ctrlChest = mc.textFieldButtonGrp("ctrlIKChestLoad_tf", q=True, text=True)

        ctrlLeg = mc.textFieldButtonGrp("ctrlLeg_tfbg", q=True, text=True)
        ctrlHipFK = mc.textFieldButtonGrp("ctrlFKHip_tfbg", q=True, text=True)
        ctrlHipIK = mc.textFieldButtonGrp("ctrlIKHip_tfbg", q=True, text=True)

        ctrlCOG = mc.textFieldButtonGrp("ctrlCOG_tfbg", q=True, text=True)
        grpFollow = mc.textFieldButtonGrp("grpLOCFollow_tfbg", q=True, text=True)

        if not ctrlCOG:
            mc.warning("You need to select COG Control")
            return

        if not grpFollow:
            mc.warning("You need to select the World Follow Group")
            return

        if useArm:
            if not ctrlArm:
                mc.warning("You need to select the FK Arm Control")
                return
            if not ctrlShoulder:
                mc.warning("You need to select the Shoulder Control")
                return
            if not ctrlChest:
                mc.warning("You need to select the IK Chest Control")
                return

        if useLeg:
            if not ctrlLeg:
                mc.warning("You need to select the FK Leg Control")
                return
            if not ctrlHipFK:
                mc.warning("You need to select the FK Hip Control")
                return
            if not ctrlHipIK:
                mc.warning("You need to select the IK Hip Control")
                return

        if mirrorSel == 1:
            mirrorRig = False
        else:
            mirrorRig = True

        if checkSelLeft == 1:
            isLeft = True
            leftRight = "l_"
            leftRightMirror = "r_"

            colourTU = 14
            colourTUMirror = 13
        else:
            isLeft = False
            leftRight = "r_"
            leftRightMirror = "l_"
            colourTU = 13
            colourTUMirror = 14

        leftRightReplace = "_" + leftRight
        leftRightReplaceMirror = "_" + leftRightMirror

        # make sure the selections are not empty
        checkList = [ctrlArm]
        if ((checkList[0] == "")):
            mc.warning("You are missing a selection!")
            return
        else:
            # CRU.createLocatorToDelete()
            if useArm:
                if not (CRU.checkLeftRight(isLeft, ctrlArm)):
                    # if the values are not lined up properly, break out
                    mc.warning("You are selecting the incorrect side for the FK Upper Arm Control")
                    return
                if not (CRU.checkLeftRight(isLeft, ctrlShoulder)):
                    # if the values are not lined up properly, break out
                    mc.warning("You are selecting the incorrect side for the Shoulder")
                    return
                # give us the name for the mirrored upper body parts
                if mirrorRig:
                    ctrlArmMirror = ctrlArm.replace(leftRightReplace, leftRightReplaceMirror)
                    ctrlShoulderMirror = ctrlShoulder.replace(leftRightReplace, leftRightReplaceMirror)
            if useLeg:
                if not (CRU.checkLeftRight(isLeft, ctrlLeg)):
                    # if the values are not lined up properly, break out
                    mc.warning("You are selecting the incorrect side for the FK Upper Leg Control")
                    return
                # give us the name for the mirrored lower body parts
                if mirrorRig:
                    ctrlLegMirror = ctrlLeg.replace(leftRightReplace, leftRightReplaceMirror)

            if useArm:
                self.makeArm(ctrlArm, ctrlShoulder, ctrlChest, ctrlCOG, grpFollow, leftRight, colourTU)

            if useLeg:
                self.makeLeg(ctrlLeg, ctrlHipFK, ctrlHipIK, ctrlCOG, grpFollow, leftRight, colourTU)

            if mirrorRig:
                if useArm:
                    self.makeArm(ctrlArmMirror, ctrlShoulderMirror, ctrlChest, ctrlCOG, grpFollow, leftRightMirror,
                                 colourTUMirror)
                if useLeg:
                    self.makeLeg(ctrlLegMirror, ctrlHipFK, ctrlHipIK, ctrlCOG, grpFollow, leftRightMirror,
                                 colourTUMirror)
