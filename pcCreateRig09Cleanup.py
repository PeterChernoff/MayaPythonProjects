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
import pcCreateRigUtilities
from pcCreateRigUtilities import pcCreateRigUtilities as CRU

reload(pcCreateRigUtilities)


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
        mc.separator(st="in", h=20, w=500)
        # sources
        mc.rowColumnLayout(nc=2, cw=[(1, 100), (2, 370)], cs=[1, 5], rs=[1, 3])

        mc.text(bgc=(0.85, 0.65, 0.25), l="Left Leg Group: ")
        mc.textFieldButtonGrp("grpLLegLoad_tf", cw=(1, 322), bl="  Load  ", tx="GRP_rig_l_leg")
        mc.text(bgc=(0.85, 0.65, 0.25), l="Right Leg Group: ")
        mc.textFieldButtonGrp("grpRLegLoad_tf", cw=(1, 322), bl="  Load  ", tx="GRP_rig_r_leg")
        mc.text(bgc=(0.85, 0.65, 0.25), l="Left Arm Group: ")
        mc.textFieldButtonGrp("grpLArmLoad_tf", cw=(1, 322), bl="  Load  ", tx="GRP_rig_l_arm")
        mc.text(bgc=(0.85, 0.65, 0.25), l="Right Arm Group: ")
        mc.textFieldButtonGrp("grpRArmLoad_tf", cw=(1, 322), bl="  Load  ", tx="GRP_rig_r_arm")

        mc.setParent("..")
        mc.separator(st="in", h=20, w=500)

        mc.rowColumnLayout(nc=2, cw=[(1, 100), (2, 370)], cs=[1, 5], rs=[1, 3])

        mc.text(bgc=(0.85, 0.65, 0.25), l="Ctrl FK/IK: ")
        mc.textFieldButtonGrp("ctrlFKIKLoad_tfbg", cw=(1, 322), bl="  Load  ", tx="CTRL_fkikSwitch")
        mc.text(bgc=(0.85, 0.65, 0.25), l="Ctrl COG: ")
        mc.textFieldButtonGrp("ctrlCOGLoad_tfbg", cw=(1, 322), bl="  Load  ", tx="CTRL_COG")

        mc.setParent("..")
        mc.separator(st="in", h=20, w=500)

        mc.rowColumnLayout(nc=2, cw=[(1, 100), (2, 370)], cs=[1, 5], rs=[1, 3])

        mc.text(bgc=(0.85, 0.65, 0.25), l="Torso Group: ")
        mc.textFieldButtonGrp("grpTorsoLoad_tfbg", cw=(1, 322), bl="  Load  ", tx="GRP_rig_torso")
        mc.text(bgc=(0.85, 0.65, 0.25), l="Do Not Touch Group: ")
        mc.textFieldButtonGrp("grpDNTLoad_tfbg", cw=(1, 322), bl="  Load  ", tx="GRP_doNotTouch_spine")
        mc.text(bgc=(0.85, 0.65, 0.25), l="Offset Ctrl Eyes: ")
        mc.textFieldButtonGrp("grpOffsetEyesLoad_tfbg", cw=(1, 322), bl="  Load  ", tx="OFFSET_CTRL_eyes")
        mc.text(bgc=(0.85, 0.65, 0.25), l="Offset Ctrl COG: ")
        mc.textFieldButtonGrp("grpOffsetCogLoad_tfbg", cw=(1, 322), bl="  Load  ", tx="OFFSET_CTRL_COG")

        mc.setParent("..")
        mc.separator(st="in", h=20, w=500)

        mc.rowColumnLayout(nc=2, cw=[(1, 100), (2, 370)], cs=[1, 5], rs=[1, 3])

        mc.text(bgc=(0.85, 0.65, 0.25), l="Follow Group: ")
        mc.textFieldButtonGrp("grpFollowLoad_tfbg", cw=(1, 322), bl="  Load  ", tx="GRP_LOC_follow")

        mc.setParent("..")
        mc.separator(st="in", h=20, w=500)

        mc.rowColumnLayout(nc=2, cw=[(1, 100), (2, 370)], cs=[1, 5], rs=[1, 3])

        mc.text(bgc=(0.85, 0.65, 0.25), l="Remaining Geo Group: ")
        mc.textFieldButtonGrp("grpGeoLoad_tfbg", cw=(1, 322), bl="  Load  ", tx="male_geo_grp")

        mc.setParent("..")
        mc.separator(st="in", h=20, w=500)

        mc.rowColumnLayout(nc=2, cw=[(1, 100), (2, 370)], cs=[1, 5], rs=[1, 3])
        mc.checkBox("selGeo_cb", l="Affect Geometry", en=True, v=True)

        mc.setParent("..")

        mc.separator(st="in", h=20, w=500)

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
        self.grpSel = self.tgpLoadGrpBtn("grpLLegLoad_tf", "left leg", ["GRP", "rig", "_l_", "leg"])

    def loadSrc2Btn(self):
        self.grpSel = self.tgpLoadGrpBtn("grpRLegLoad_tf", "right leg", ["GRP", "rig", "_r_", "leg"])

    def loadSrc3Btn(self):
        self.grpSel = self.tgpLoadGrpBtn("grpLArmLoad_tf", "left arm", ["GRP", "rig", "_l_", "arm"])

    def loadSrc4Btn(self):
        self.grpSel = self.tgpLoadGrpBtn("grpRArmLoad_tf", "right arm", ["GRP", "rig", "_r_", "arm"])

    def loadSrc5Btn(self):
        self.grpSel = self.tgpLoadCurvBtn("grpLLegLoad_tf", "fkikSwitch", ["CTRL", "fkikSwitch"])

    def loadSrc6Btn(self):
        self.grpSel = self.tgpLoadCurvBtn("grpRLegLoad_tf", "COG", ["CTRL", "COG"])

    def loadSrc7Btn(self):
        self.grpSel = self.tgpLoadGrpBtn("grpTorsoLoad_tfbg", "torso rig", ["GRP", "rig", "torso"])

    def loadSrc8Btn(self):
        self.grpSel = self.tgpLoadGrpBtn("grpDNTLoad_tfbg", "spine doNotTouch", ["GRP", "doNotTouch", "spine"])

    def loadSrc9Btn(self):
        self.grpSel = self.tgpLoadGrpBtn("grpOffsetEyesLoad_tfbg", "eyes offset", ["OFFSET", "eyes"])

    def loadSrc10Btn(self):
        self.grpSel = self.tgpLoadGrpBtn("grpOffsetCogLoad_tfbg", "COG offset", ["OFFSET", "COG"])

    def loadSrc11Btn(self):
        self.grpSel = self.tgpLoadGrpBtn("grpFollowLoad_tfbg", "follow", ["GRP", "LOC", "follow"])

    def loadSrc12Btn(self):
        self.grpSel = self.tgpLoadGrpBtn("grpGeoLoad_tfbg", "geo", ["geo", "grp"])

    def tgpLoadGrpBtn(self, loadBtn, type, keywords):
        self.selLoad = []
        # self.selLoad = mc.ls(sl=True, fl=True, type="nurbsCurve")
        self.selLoad = mc.ls(sl=True, fl=True, type="transform")

        if (len(self.selLoad) != 1):
            mc.warning("Select only the {0} group".format(type))
            return
        else:

            if CRU.checkObjectType(self.selLoad[0]) != "transform":
                mc.warning("You should be selecting a group")
                return
            selName = self.selLoad[0]
            print(keywords)
            print(selName)
            print(selName.lower())
            if not all(word.lower() in selName.lower() for word in keywords):
                mc.warning("That is the wrong group")
                return

            mc.textFieldButtonGrp(loadBtn, e=True, tx=selName)
            return selName

    def tgpLoadCurvBtn(self, loadBtn, type, keywords):
        self.selLoad = []
        # self.selLoad = mc.ls(sl=True, fl=True, type="nurbsCurve")
        self.selLoad = mc.ls(sl=True, fl=True, type="transform")

        if (len(self.selLoad) != 1):
            mc.warning("Select only the {0} control".format(type))
            return
        else:

            if CRU.checkObjectType(self.selLoad[0]) != "nurbsCurve":
                mc.warning("You should be selecting a curve")
                return
            selName = self.selLoad[0]

            if not all(word.lower() in selName.lower() for word in keywords):
                mc.warning("That is the wrong curve")
                return
            mc.textFieldButtonGrp(loadBtn, e=True, tx=selName)
            return selName


    def tgpMakeBC(self, *args):


        grpLLeg = mc.textFieldButtonGrp("grpLLegLoad_tf", q=True, text=True)
        grpRLeg = mc.textFieldButtonGrp("grpRLegLoad_tf", q=True, text=True)
        grpLArm = mc.textFieldButtonGrp("grpLArmLoad_tf", q=True, text=True)
        grpRArm = mc.textFieldButtonGrp("grpRArmLoad_tf", q=True, text=True)

        jntMasterToes = mc.textFieldButtonGrp("jntToesLoad_tf", q=True, text=True)
        grpLegs = mc.textFieldButtonGrp("grpLegLoad_tfbg", q=True, text=True)


        mc.textFieldButtonGrp("ctrlFKIKLoad_tfbg", e=True, bc=self.loadSrc5Btn)
        mc.textFieldButtonGrp("ctrlCOGLoad_tfbg", e=True, bc=self.loadSrc6Btn)

        mc.textFieldButtonGrp("grpTorsoLoad_tfbg", e=True, bc=self.loadSrc7Btn)
        mc.textFieldButtonGrp("grpDNTLoad_tfbg", e=True, bc=self.loadSrc8Btn)
        mc.textFieldButtonGrp("grpOffsetEyesLoad_tfbg", e=True, bc=self.loadSrc9Btn)
        mc.textFieldButtonGrp("grpOffsetCogLoad_tfbg", e=True, bc=self.loadSrc10Btn)

        mc.textFieldButtonGrp("grpFollowLoad_tfbg", e=True, bc=self.loadSrc11Btn)
        mc.textFieldButtonGrp("grpGeoLoad_tfbg", e=True, bc=self.loadSrc12Btn)
