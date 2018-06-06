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

import pcCreateRigAlt00AUtilities

reload(pcCreateRigAlt00AUtilities)
from pcCreateRigAlt00AUtilities import pcCreateRigUtilities as CRU

import pcCreateRigAlt05ArmsCode

reload(pcCreateRigAlt05ArmsCode)
from pcCreateRigAlt05ArmsCode import pcCreateRigAlt05ArmsCode as CRA5


class pcCreateRigAlt05ArmsTest(UI):
    def __init__(self):
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
        mirrorSel = mc.radioButtonGrp("selArmMirrorType_rbg", q=True, select=True)
        lrSel = mc.radioButtonGrp("selArmType_rbg", q=True, select=True)

        cbGeo = mc.checkBox("selGeo_cb", q=True, v=True)
        cbSwitchSetup = mc.checkBox("selAddIKFKSwitching_cb", q=True, v=True)
        cbToggleSpineStretch = mc.checkBox("selStretchSpineToggle_cb", q=True, v=True)
        cbSpecialStretch = mc.checkBox("selSpecialStretch_cb", q=True, v=True)

        bndJnt = mc.textFieldButtonGrp("jointArmsLoad_tfbg", q=True, text=True)
        jntShoulderRootCheck = mc.textFieldButtonGrp("jointShoulderJntLoad_tfbg", q=True, text=True)
        jntIKShoulderCheck = mc.textFieldButtonGrp("jntIKShoulderLoad_tf", q=True, text=True)
        grpDNTTorsoCheck = mc.textFieldButtonGrp("grpTorsoDNTLoad_tf", q=True, text=True)

        ctrlRootCheck = mc.textFieldButtonGrp("rootTrans_tfbg", q=True, text=True)
        grpSpineToggleCheck = mc.textFieldButtonGrp("grpheadShoulders_tfbg", q=True, text=True)

        cra5 = CRA5(mirrorSel, lrSel,
                 cbGeo, cbSwitchSetup, cbToggleSpineStretch, cbSpecialStretch,
                 bndJnt, jntShoulderRootCheck, jntIKShoulderCheck, grpDNTTorsoCheck,
                 ctrlRootCheck, grpSpineToggleCheck)

    def loadSrc1Btn(self):
        self.selSrc1 = CRU.tgpLoadJntsBtn("jointArmsLoad_tfbg", "joint", "Root Upper Arm Joint",
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
