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
# This program assumes there are no toes in the original.
import pcCreateRig00AUtilities
from pcCreateRig00AUtilities import pcCreateRigUtilities as CRU

reload(pcCreateRig00AUtilities)


class pcCreateRig09Cleanup(UI):
    def __init__(self):

        self.window = "bcWindow"
        self.title = "pcRigCleanup"
        self.winSize = (500, 650)

        self.createUI()

    def createCustom(self, *args):
        '''
        #
        #
        #
        #
        #
        '''

        mc.rowColumnLayout(nc=2, cw=[(1, 500), (2, 500)], cs=[1, 5], rs=[1, 3])

        mc.text(l="Select the Various Groups and Controls")
        mc.text(l="")

        mc.setParent("..")
        mc.separator(st="in", h=15, w=500)

        # sources
        mc.rowColumnLayout(nc=2, cw=[(1, 100), (2, 320)], cs=[1, 5], rs=[1, 3])

        mc.text(bgc=(0.85, 0.65, 0.25), l="Final Name: ")
        mc.textField("charNameLoad_tf", w=322, tx="char_male")

        mc.setParent("..")
        mc.separator(st="in", h=15, w=500)

        # sources
        mc.rowColumnLayout(nc=2, cw=[(1, 100), (2, 380)], cs=[1, 5], rs=[1, 3])

        mc.text(bgc=(0.85, 0.65, 0.25), l="Left Leg Group: ")
        mc.textFieldButtonGrp("grpLLegLoad_tf", cw=(1, 322), bl="  Load  ", tx="GRP_rig_l_leg")
        mc.text(bgc=(0.85, 0.65, 0.25), l="Right Leg Group: ")
        mc.textFieldButtonGrp("grpRLegLoad_tf", cw=(1, 322), bl="  Load  ", tx="GRP_rig_r_leg")
        mc.text(bgc=(0.85, 0.65, 0.25), l="Left Arm Group: ")
        mc.textFieldButtonGrp("grpLArmLoad_tf", cw=(1, 322), bl="  Load  ", tx="GRP_rig_l_arm")
        mc.text(bgc=(0.85, 0.65, 0.25), l="Right Arm Group: ")
        mc.textFieldButtonGrp("grpRArmLoad_tf", cw=(1, 322), bl="  Load  ", tx="GRP_rig_r_arm")

        mc.setParent("..")
        mc.separator(st="in", h=15, w=500)

        mc.rowColumnLayout(nc=2, cw=[(1, 100), (2, 380)], cs=[1, 5], rs=[1, 3])

        mc.text(bgc=(0.85, 0.65, 0.25), l="Ctrl FK/IK: ")
        mc.textFieldButtonGrp("ctrlFKIKLoad_tfbg", cw=(1, 322), bl="  Load  ", tx="CTRL_fkikSwitch")
        mc.text(bgc=(0.85, 0.65, 0.25), l="Ctrl COG: ")
        mc.textFieldButtonGrp("ctrlCOGLoad_tfbg", cw=(1, 322), bl="  Load  ", tx="CTRL_COG")

        mc.setParent("..")
        mc.separator(st="in", h=15, w=500)

        mc.rowColumnLayout(nc=2, cw=[(1, 120), (2, 380)], cs=[1, 5], rs=[1, 3])

        mc.text(bgc=(0.85, 0.65, 0.25), l="Torso Group: ")
        mc.textFieldButtonGrp("grpTorsoLoad_tfbg", cw=(1, 300), bl="  Load  ", tx="GRP_rig_torso")
        mc.text(bgc=(0.85, 0.65, 0.25), l="Do Not Touch Group: ")
        mc.textFieldButtonGrp("grpDNTLoad_tfbg", cw=(1, 300), bl="  Load  ", tx="GRP_doNotTouch_spine")
        mc.text(bgc=(0.85, 0.65, 0.25), l="Offset Ctrl Eyes: ")
        mc.textFieldButtonGrp("grpOffsetEyesLoad_tfbg", cw=(1, 300), bl="  Load  ", tx="OFFSET_CTRL_eyes")
        mc.text(bgc=(0.85, 0.65, 0.25), l="Offset Ctrl COG: ")
        mc.textFieldButtonGrp("grpOffsetCogLoad_tfbg", cw=(1, 300), bl="  Load  ", tx="OFFSET_CTRL_COG")

        mc.setParent("..")
        mc.separator(st="in", h=15, w=500)

        mc.rowColumnLayout(nc=2, cw=[(1, 120), (2, 380)], cs=[1, 5], rs=[1, 3])

        mc.text(bgc=(0.85, 0.65, 0.25), l="Follow Group: ")
        mc.textFieldButtonGrp("grpFollowLoad_tfbg", cw=(1, 300), bl="  Load  ", tx="GRP_LOC_follow")

        mc.setParent("..")
        mc.separator(st="in", h=15, w=500)

        mc.rowColumnLayout(nc=2, cw=[(1, 120), (2, 370)], cs=[1, 5], rs=[1, 3])

        mc.text(bgc=(0.85, 0.65, 0.25), l="Extra Geo Group: ")
        mc.textFieldButtonGrp("grpGeoLoad_tfbg", cw=(1, 300), bl="  Load  ", tx="male_geo_grp")

        mc.setParent("..")
        mc.separator(st="in", h=15, w=500)

        mc.rowColumnLayout(nc=2, cw=[(1, 100), (2, 370)], cs=[1, 5], rs=[1, 3])
        mc.checkBox("selGeo_cb", l="Affect Geometry", en=True, v=True)

        mc.setParent("..")

        # load buttons
        #

        mc.textFieldButtonGrp("grpLLegLoad_tf", e=True, bc=self.loadSrc1Btn)
        mc.textFieldButtonGrp("grpRLegLoad_tf", e=True, bc=self.loadSrc2Btn)
        mc.textFieldButtonGrp("grpLArmLoad_tf", e=True, bc=self.loadSrc3Btn)
        mc.textFieldButtonGrp("grpRArmLoad_tf", e=True, bc=self.loadSrc4Btn)

        mc.textFieldButtonGrp("ctrlFKIKLoad_tfbg", e=True, bc=self.loadSrc5Btn)
        mc.textFieldButtonGrp("ctrlCOGLoad_tfbg", e=True, bc=self.loadSrc6Btn)

        mc.textFieldButtonGrp("grpTorsoLoad_tfbg", e=True, bc=self.loadSrc7Btn)
        mc.textFieldButtonGrp("grpDNTLoad_tfbg", e=True, bc=self.loadSrc8Btn)
        mc.textFieldButtonGrp("grpOffsetEyesLoad_tfbg", e=True, bc=self.loadSrc9Btn)
        mc.textFieldButtonGrp("grpOffsetCogLoad_tfbg", e=True, bc=self.loadSrc10Btn)

        mc.textFieldButtonGrp("grpFollowLoad_tfbg", e=True, bc=self.loadSrc11Btn)
        mc.textFieldButtonGrp("grpGeoLoad_tfbg", e=True, bc=self.loadSrc12Btn)

        self.selLoad = []
        self.ctrlsArray = []
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
        self.selSrc1 = self.tgpLoadTxBtn("grpLLegLoad_tf", "transform", "Left Leg Group", ["GRP", "rig", "_l_", "leg"], "group")
        print(self.selSrc1)

    def loadSrc2Btn(self):
        self.selSrc2 = self.tgpLoadTxBtn("grpRLegLoad_tf", "transform", "Right Leg Group", ["GRP", "rig", "_r_", "leg"], "group")
        print(self.selSrc2)

    def loadSrc3Btn(self):
        self.selSrc3 = self.tgpLoadTxBtn("grpLArmLoad_tf", "transform", "Left Arm Group", ["GRP", "rig", "_l_", "arm"], "group")
        print(self.selSrc3)

    def loadSrc4Btn(self):
        self.selSrc4 = self.tgpLoadTxBtn("grpRArmLoad_tf", "transform", "Right Arm Group", ["GRP", "rig", "_r_", "arm"], "group")
        print(self.selSrc4)

    def loadSrc5Btn(self):
        self.selSrc5 = self.tgpLoadTxBtn("ctrlFKIKSwitch_tfbg", "nurbsCurve", "FK/IK Switch Control",
                                         ["CTRL", "fk", "ik", "Switch"], "control")
        print(self.selSrc5)

    def loadSrc6Btn(self):
        self.selSrc6 = self.tgpLoadTxBtn("grpRLegLoad_tf", "nurbsCurve, ""COG control", ["CTRL", "COG"], "control")
        print(self.selSrc6)

    def loadSrc7Btn(self):
        self.selSrc7 = self.tgpLoadTxBtn("grpTorsoLoad_tfbg", "transform", "Torso Rig", ["GRP", "rig", "torso"], "group")
        print(self.selSrc7)

    def loadSrc8Btn(self):
        self.selSrc8 = self.tgpLoadTxBtn("grpDNTLoad_tfbg", "transform","doNotTouch Spine Group", ["GRP", "doNotTouch", "spine"], "group")
        print(self.selSrc8)

    def loadSrc9Btn(self):
        self.selSrc9 = self.tgpLoadTxBtn("grpOffsetEyesLoad_tfbg", "transform", "Eyes Offset", ["OFFSET", "eyes"], "offset")
        print(self.selSrc9)

    def loadSrc10Btn(self):
        self.selSrc10 = self.tgpLoadTxBtn("grpOffsetCogLoad_tfbg", "transform", "COG Offset", ["OFFSET", "COG"], "offset")
        print(self.selSrc10)

    def loadSrc11Btn(self):
        self.selSrc11 = self.tgpLoadTxBtn("grpFollowLoad_tfbg", "transform", "Follow Group", ["GRP", "LOC", "follow"], "group")
        print(self.selSrc11)

    def loadSrc12Btn(self):
        self.selSrc12 = self.tgpLoadTxBtn("grpGeoLoad_tfbg", "geometry group", ["geo", "grp"])
        print(self.selSrc12)


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

    def tgpMakeBC(self, *args):

        checkGeo = mc.checkBox("selGeo_cb", q=True, v=True)

        charName = mc.textField("charNameLoad_tf", q=True, text=True)
        if charName == "":
            charName = "defaultPerson"

        print(charName)

        grpLLeg = mc.textFieldButtonGrp("grpLLegLoad_tf", q=True, text=True)
        grpRLeg = mc.textFieldButtonGrp("grpRLegLoad_tf", q=True, text=True)
        grpLArm = mc.textFieldButtonGrp("grpLArmLoad_tf", q=True, text=True)
        grpRArm = mc.textFieldButtonGrp("grpRArmLoad_tf", q=True, text=True)

        isLeft = True
        isLeftMirror = False
        if not (CRU.checkLeftRight(isLeft, grpLLeg)):
            # if the values are not lined up properly, break out
            mc.warning("You are selecting the incorrect side for the left leg group")
            return

        if not (CRU.checkLeftRight(isLeftMirror, grpRLeg)):
            # if the values are not lined up properly, break out
            mc.warning("You are selecting the incorrect side for the right leg group")
            return

        if not (CRU.checkLeftRight(isLeft, grpLArm)):
            # if the values are not lined up properly, break out
            mc.warning("You are selecting the incorrect side for the left arm group")
            return

        if not (CRU.checkLeftRight(isLeftMirror, grpRArm)):
            # if the values are not lined up properly, break out
            mc.warning("You are selecting the incorrect side for the right arm group")
            return

        ctrlFKIKSwitch = mc.textFieldButtonGrp("ctrlFKIKLoad_tfbg", q=True, text=True)
        ctrlCOG = mc.textFieldButtonGrp("ctrlCOGLoad_tfbg", q=True, text=True)

        grpTorso = mc.textFieldButtonGrp("grpTorsoLoad_tfbg", q=True, text=True)
        grpDNTouch = mc.textFieldButtonGrp("grpDNTLoad_tfbg", q=True, text=True)
        offsetEyes = mc.textFieldButtonGrp("grpOffsetEyesLoad_tfbg", q=True, text=True)
        offsetCog = mc.textFieldButtonGrp("grpOffsetCogLoad_tfbg", q=True, text=True)

        grpFollow = mc.textFieldButtonGrp("grpFollowLoad_tfbg", q=True, text=True)

        grpGeo = mc.textFieldButtonGrp("grpGeoLoad_tfbg", q=True, text=True)

        # CRU.createLocatorToDelete()

        # parent CTRL_fkikSwtich under ctrlCOG (Center Of Gravity) if you haven't already
        try:
            mc.parent(ctrlFKIKSwitch, ctrlCOG)
        except:
            mc.warning("{0} is already parented to {1}".format(ctrlFKIKSwitch, ctrlCOG))
        # parent the legs into GRP_rig_leg
        grpLegs = mc.group(name="GRP_rig_leg", em=True)
        mc.parent(grpLLeg, grpRLeg, grpLegs)

        # parent the arms into GRP_rig_arm
        grpArms = mc.group(name="GRP_rig_arm", em=True)
        mc.parent(grpLArm, grpRArm, grpArms)

        # parent offset eyes, offset cog, and spine do not touch under GRP_rig_torso
        mc.parent(offsetEyes, offsetCog, grpDNTouch, grpTorso)

        # create a group called GRP_rig, parent the torso, leg, arm and follow groups
        grpRig = mc.group(name="GRP_rig", em=True)
        mc.parent(grpTorso, grpLegs, grpArms, grpFollow, grpRig)

        # create the globalSRT
        toDelete = mc.spaceLocator(name="globalSRT", p=(0, 0, 0))[0]
        offsetCtrlGlobalSRT = CRU.createCTRLs(toDelete, addPrefix=True, size=80, orientVal=(0, -1, 0), sectionsTU=3, colour=6)
        mc.delete(toDelete)
        cvsToMove = mc.select(offsetCtrlGlobalSRT[1] + ".cv[:]")
        mc.move(25, cvsToMove, z=True, r=True, wd=True, ls=True)

        mc.parent(grpRig, offsetCtrlGlobalSRT[1])

        # creating the char group
        charGrp = mc.group(name=charName, em=True)

        if checkGeo:
            mc.parent(grpGeo, charGrp)
        mc.parent(offsetCtrlGlobalSRT[0], charGrp)









