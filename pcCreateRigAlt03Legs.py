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

import pcCreateRigAlt03LegsCode
from pcCreateRigAlt03LegsCode import pcCreateRigAlt03LegsCode as CRA3

reload(pcCreateRigAlt03LegsCode)


class pcCreateRigAlt03LegsTest(UI):
    def __init__(self):
        self.window = "bcWindow"
        self.title = "pcRigLegs"
        self.winSize = (500, 475)

        self.createUI()

    def createCustom(self, *args):
        # selection type

        mc.rowColumnLayout(nc=2, cw=[(1, 500), (2, 500)], cs=[1, 5], rs=[1, 3])

        mc.text(l="Select The Leg Root: ")
        mc.text(l="")
        mc.separator(st="in", h=17, w=500)
        mc.setParent("..")
        mc.rowColumnLayout(nc=3, cw=[(1, 125), (2, 125), (3, 200)], cs=[1, 5], rs=[1, 3],
                           cal=([1, "left"], [2, "left"], [3, "left"],))

        mc.text(l="Mirror Leg As Well?")
        # mc.setParent("..")
        mc.radioButtonGrp("selLegMirrorType_rbg", la2=["No", "Yes"], nrb=2, sl=2, cw2=[50, 50], )
        mc.text(l="")
        mc.checkBox("selCreateTwists_cb", l="Create Twists", en=True, v=True)
        mc.checkBox("selSpineEnd_cb", l="Connect To Hip", en=True, v=True)
        mc.checkBox("selAnkleTwist_cb", l="Includes Ankle Twist Bones", en=True, v=True)
        mc.setParent("..")
        mc.rowColumnLayout(nc=1, cw=[(1, 200)], cs=[1, 5], rs=[1, 3],
                           cal=([1, "left"]))
        mc.checkBox("selAddIKFKSwitching_cb", l="Include IK FK Switching Setup", en=True, v=True)
        mc.setParent("..")
        mc.separator(st="in", h=17, w=500)

        mc.rowColumnLayout(nc=3, cw=[(1, 100), (2, 200), (3, 150)], cs=[1, 5], rs=[1, 3],
                           cal=([1, "left"], [2, "left"], [3, "left"],))
        mc.text(l="Initial Limb: ")
        mc.radioButtonGrp("selLegType_rbg", la2=["Left", "Right"], nrb=2, sl=1, cw2=[50, 50], )
        mc.setParent("..")
        mc.separator(st="in", h=17, w=500)

        # sources
        mc.rowColumnLayout(nc=2, cw=[(1, 140), (2, 360)], cs=[1, 5], rs=[1, 3])
        mc.text(bgc=(0.85, 0.65, 0.25), l="Leg: ")
        mc.textFieldButtonGrp("jointLoad_tfbg", cw=(1, 300), bl="  Load  ", tx="JNT_BND_l_upperLeg")

        mc.text(bgc=(0.85, 0.65, 0.25), l="IK Hip Joint: ")
        mc.textFieldButtonGrp("jntIKHip_tfbg", cw=(1, 300), bl="  Load  ", tx="JNT_IK_hip")

        mc.text(bgc=(0.85, 0.65, 0.25), l="Do Not Touch Torso Group: ")
        mc.textFieldButtonGrp("grpTorsoDNT_tfbg", cw=(1, 300), bl="  Load  ", tx="GRP_DO_NOT_TOUCH_torso")

        mc.text(bgc=(0.85, 0.65, 0.25), l="Body CTRL: ")
        mc.textFieldButtonGrp("ctrlBody_tfbg", cw=(1, 300), bl="  Load  ", tx="CTRL_body")

        mc.text(bgc=(0.85, 0.65, 0.25), l="Root Transform Control: ")
        mc.textFieldButtonGrp("rootTrans_tfbg", cw=(1, 300), bl="  Load  ", tx="CTRL_rootTransform")

        mc.setParent("..")

        mc.separator(st="in", h=10, w=500)

        mc.rowColumnLayout(nc=2, cw=[(1, 100), (2, 370)], cs=[1, 5], rs=[1, 3])
        mc.checkBox("selGeo_cb", l="Affect Geometry", en=True, v=True)

        mc.setParent("..")

        # load buttons
        #
        mc.textFieldButtonGrp("jointLoad_tfbg", e=True, bc=self.loadSrc1Btn)

        mc.textFieldButtonGrp("jntIKHip_tfbg", e=True, bc=self.loadSrc2Btn)
        mc.textFieldButtonGrp("grpTorsoDNT_tfbg", e=True, bc=self.loadSrc3Btn)
        mc.textFieldButtonGrp("ctrlBody_tfbg", e=True, bc=self.loadSrc4Btn)
        mc.textFieldButtonGrp("rootTrans_tfbg", e=True, bc=self.loadSrc5Btn)

        self.selLoad = []
        self.jointArray = []
        mc.showWindow(self.window)

    def createButtonCmd(self, *args):
        mirrorSel = mc.radioButtonGrp("selLegMirrorType_rbg", q=True, select=True)
        lrSel = mc.radioButtonGrp("selLegType_rbg", q=True, select=True)

        cbTwists = mc.checkBox("selCreateTwists_cb", q=True, v=True)
        cbAnkleTwist = mc.checkBox("selAnkleTwist_cb", q=True, v=True)
        cbSwitchSetup = mc.checkBox("selAddIKFKSwitching_cb", q=True, v=True)
        cbGeo = mc.checkBox("selGeo_cb", q=True, v=True)
        cbHip = mc.checkBox("selSpineEnd_cb", q=True, v=True)

        bndJnt = mc.textFieldButtonGrp("jointLoad_tfbg", q=True, text=True)
        jntIKHipCheck = mc.textFieldButtonGrp("jntIKHip_tfbg", q=True, text=True)
        grpDNTTorsoCheck = mc.textFieldButtonGrp("grpTorsoDNT_tfbg", q=True, text=True)
        ctrlBodyCheck = mc.textFieldButtonGrp("ctrlBody_tfbg", q=True, text=True)
        ctrlRootTransCheck = mc.textFieldButtonGrp("rootTrans_tfbg", q=True, text=True)

        cra3 = CRA3(mirrorSel, lrSel,
                    cbTwists,cbAnkleTwist, cbSwitchSetup, cbGeo, cbHip,
                    bndJnt, jntIKHipCheck, grpDNTTorsoCheck,
                    ctrlBodyCheck, ctrlRootTransCheck
                    )

    def loadSrc1Btn(self):
        self.selSrc1 = CRU.tgpLoadJntsBtn("jointLoad_tfbg", "joint", "Root Leg Joint", ["JNT", "upper", "Leg"])
        print(self.selSrc1)

    def loadSrc2Btn(self):
        self.selSrc2 = CRU.tgpLoadTxBtn("jntIKHip_tfbg", "joint", "IK Hip Joint", ["JNT", "hip", "IK"])
        print(self.selSrc2)

    def loadSrc3Btn(self):
        self.selSrc3 = CRU.tgpLoadTxBtn("grpTorsoDNT_tfbg", "transform", "Torso DO NOT TOUCH",
                                        ["GRP", "DO", "NOT", "TOUCH"],
                                        "group")
        print(self.selSrc3)

    def loadSrc4Btn(self):
        self.selSrc4 = CRU.tgpLoadTxBtn("ctrlBody_tfbg", "nurbsCurve", "COG Control", ["CTRL", "COG"],
                                        "control")
        print(self.selSrc4)

    def loadSrc5Btn(self):
        self.selSrc5 = CRU.tgpLoadTxBtn("rootTrans_tfbg", "nurbsCurve", "Root Transform Control",
                                        ["CTRL", "rootTransform"], "control")
        print(self.selSrc5)

    def loadSrc6Btn(self):
        self.selSrc6 = CRU.tgpLoadTxBtn("grpTorsoDNT_tfbg", "transform", "Torso DO NOT TOUCH",
                                        ["GRP", "DO", "NOT", "TOUCH"],
                                        "group")
        print(self.selSrc6)
