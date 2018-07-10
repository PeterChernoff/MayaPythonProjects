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

import pcCreateRigAlt00AUtilities

reload(pcCreateRigAlt00AUtilities)

from pcCreateRigAlt00AUtilities import pcCreateRigUtilities as CRU

import pcCreateRigAlt06HandsCode

reload(pcCreateRigAlt06HandsCode)
from pcCreateRigAlt06HandsCode import pcCreateRigAlt06HandsCode as CRA6


class pcCreateRigAlt06Hands(UI):
    def __init__(self):

        self.window = "bcWindow"
        self.title = "pcRigHands"
        self.winSize = (500, 450)

        self.createUI()

    def createCustom(self, *args):
        # selection type

        mc.rowColumnLayout(nc=2, cw=[(1, 500), (2, 500)], cs=[1, 5], rs=[1, 3])

        mc.text(l="Select The Hand Base Joint: ")
        mc.text(l="")
        mc.separator(st="in", h=17, w=500)
        mc.setParent("..")
        mc.rowColumnLayout(nc=3, cw=[(1, 125), (2, 150), (3, 150)], cs=[1, 5], rs=[1, 3],
                           cal=([1, "left"], [2, "left"], [3, "left"],))

        mc.text(l="Mirror Hand As Well?")
        # mc.setParent("..")
        mc.radioButtonGrp("selHandMirrorType_rbg", la2=["No", "Yes"], nrb=2, sl=2, cw2=[50, 50], )
        mc.text(l="")
        mc.setParent("..")
        mc.separator(st="in", h=20, w=500)

        mc.rowColumnLayout(nc=3, cw=[(1, 100), (2, 200), (3, 150)], cs=[1, 5], rs=[1, 3],
                           cal=([1, "left"], [2, "left"], [3, "left"],))
        mc.text(l="Initial Limb: ")
        mc.radioButtonGrp("selHandType_rbg", la2=["Left", "Right"], nrb=2, sl=1, cw2=[50, 50], )
        mc.setParent("..")
        mc.separator(st="in", h=20, w=500)

        # sources
        mc.rowColumnLayout(nc=2, cw=[(1, 100), (2, 380)], cs=[1, 5], rs=[1, 3])
        mc.text(bgc=(0.85, 0.65, 0.25), l="handBase Joint: ")
        mc.textFieldButtonGrp("jntFingersLoad_tfbg", cw=(1, 322), bl="  Load  ", tx="JNT_BND_l_handBase")

        mc.text(bgc=(0.85, 0.65, 0.25), l="Palm Loc: ")
        mc.textFieldButtonGrp("locPalmLoad_tf", cw=(1, 322), bl="  Load  ", tx="LOC_l_palmInner")

        mc.text(bgc=(0.85, 0.65, 0.25), l="Arm Bind End: ")
        mc.textFieldButtonGrp("jntBindEndLoad_tf", cw=(1, 322), bl="  Load  ", tx="JNT_l_arm_bindEnd")

        mc.text(bgc=(0.85, 0.65, 0.25), l="Root Transform\nControl: ")
        mc.textFieldButtonGrp("rootTrans_tfbg", cw=(1, 322), bl="  Load  ", tx="CTRL_rootTransform")

        mc.text(bgc=(0.85, 0.65, 0.25), l="Arm's Hand Joint: ")
        mc.textFieldButtonGrp("jntHandLoad_tfbg", cw=(1, 322), bl="  Load  ", tx="JNT_BND_l_hand")

        mc.text(bgc=(0.85, 0.65, 0.25), l="Arm Control\nSettings: ")
        mc.textFieldButtonGrp("ctrlSettingsLoad_tfbg", cw=(1, 322), bl="  Load  ", tx="CTRL_settings_l_arm")

        mc.setParent("..")

        mc.separator(st="in", h=20, w=500)

        mc.rowColumnLayout(nc=2, cw=[(1, 100), (2, 370)], cs=[1, 5], rs=[1, 3])
        mc.checkBox("selGeo_cb", l="Affect Geometry", en=True, v=True)

        mc.setParent("..")

        # load buttons
        #

        mc.textFieldButtonGrp("jntFingersLoad_tfbg", e=True, bc=self.loadSrc1Btn)
        mc.textFieldButtonGrp("locPalmLoad_tf", e=True, bc=self.loadSrc2Btn)
        mc.textFieldButtonGrp("jntBindEndLoad_tf", e=True, bc=self.loadSrc3Btn)
        mc.textFieldButtonGrp("rootTrans_tfbg", e=True, bc=self.loadSrc4Btn)
        mc.textFieldButtonGrp("jntHandLoad_tfbg", e=True, bc=self.loadSrc5Btn)
        mc.textFieldButtonGrp("ctrlSettingsLoad_tfbg", e=True, bc=self.loadSrc6Btn)

        self.selLoad = []
        self.jntsArray = []
        self.locArray = []
        mc.showWindow(self.window)

    def createButtonCmd(self, *args):

        lrSel = mc.radioButtonGrp("selHandType_rbg", q=True, select=True)
        mirrorSel = mc.radioButtonGrp("selHandMirrorType_rbg", q=True, select=True)
        cbGeo = mc.checkBox("selGeo_cb", q=True, v=True)
        jntFingerNamesCheck = mc.textFieldButtonGrp("jntFingersLoad_tfbg", q=True, text=True)
        locPalmCheck = mc.textFieldButtonGrp("locPalmLoad_tf", q=True, text=True)
        jntBindEndCheck = mc.textFieldButtonGrp("jntBindEndLoad_tf", q=True, text=True)
        ctrlRootTransCheck = mc.textFieldButtonGrp("rootTrans_tfbg", q=True, text=True)
        jntArmHandBndCheck = mc.textFieldButtonGrp("jntHandLoad_tfbg", q=True, text=True)
        ctrlSettingsCheck = mc.textFieldButtonGrp("ctrlSettingsLoad_tfbg", q=True, text=True)

        CRA6(lrSel=lrSel, mirrorSel=mirrorSel, cbGeo=cbGeo, jntFingerNamesCheck=jntFingerNamesCheck,
             locPalmCheck=locPalmCheck, jntBindEndCheck=jntBindEndCheck,ctrlRootTransCheck=ctrlRootTransCheck,
             jntArmHandBndCheck=jntArmHandBndCheck,ctrlSettingsCheck=ctrlSettingsCheck)

    def loadSrc1Btn(self):
        self.selSrc1 = CRU.tgpLoadJntsBtn("jntFingersLoad_tfbg", "joint", "Hand Base Joint", ["jnt", "handBase"],
                                          "joint")
        print(self.selSrc1)

    def loadSrc2Btn(self):
        self.selSrc2 = CRU.tgpLoadLocsBtn("locPalmLoad_tf", "locator", "Inner Palm Locator", ["loc", "palmInner"],
                                          "locator")
        print(self.selSrc2)

    def loadSrc3Btn(self):
        self.selSrc3 = CRU.tgpLoadTxBtn("jntBindEndLoad_tf", "joint", "Hand Base Joint", ["jnt", "arm", "bindEnd"],
                                        "joint")
        print(self.selSrc3)

    def loadSrc4Btn(self):
        self.selSrc4 = CRU.tgpLoadTxBtn("rootTrans_tfbg", "nurbsCurve", "Root Transform\nControl",
                                        ["ctrl", "rootTransform"], "control")
        print(self.selSrc4)

    def loadSrc5Btn(self):
        self.selSrc5 = CRU.tgpLoadTxBtn("jntHandLoad_tfbg", "joint", "Hand Joint",
                                        ["jnt", "bnd", "hand", ], "joint")
        print(self.selSrc5)

    def loadSrc6Btn(self):
        self.selSrc6 = CRU.tgpLoadTxBtn("ctrlSettingsLoad_tfbg", "nurbsCurve", "Arm Control Setting",
                                        ["ctrl", "arm", "settings", ], "control")
        print(self.selSrc6)
