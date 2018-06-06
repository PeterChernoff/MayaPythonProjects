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

'''
import tgpBlendColors as bc
reload(bc)
bc.tgpBlendColors()

'''

import pcCreateRigAlt00AUtilities

reload(pcCreateRigAlt00AUtilities)
from pcCreateRigAlt00AUtilities import pcCreateRigUtilities as CRU

import pcCreateRigAlt04FeetCode
from pcCreateRigAlt04FeetCode import pcCreateRigAlt04FeetCode as CRA4

reload(pcCreateRigAlt04FeetCode)


class pcCreateRigAlt04FeetTest(UI):
    def __init__(self):
        self.window = "bcWindow"
        self.title = "pcRigFeet"
        self.winSize = (500, 325)

        self.createUI()

    def createCustom(self, *args):
        # selection type

        mc.rowColumnLayout(nc=2, cw=[(1, 500), (2, 500)], cs=[1, 5], rs=[1, 3])

        mc.text(l="Select The Heel Locator: ")
        mc.text(l="")
        mc.separator(st="in", h=17, w=500)
        mc.setParent("..")
        mc.rowColumnLayout(nc=3, cw=[(1, 125), (2, 150), (3, 150)], cs=[1, 5], rs=[1, 3],
                           cal=([1, "left"], [2, "left"], [3, "left"],))

        mc.text(l="Mirror Foot As Well?")
        # mc.setParent("..")
        mc.radioButtonGrp("selLegMirrorType_rbg", la2=["No", "Yes"], nrb=2, sl=2, cw2=[50, 50], )
        mc.text(l="")
        mc.setParent("..")
        mc.separator(st="in", h=20, w=500)

        mc.rowColumnLayout(nc=3, cw=[(1, 100), (2, 200), (3, 150)], cs=[1, 5], rs=[1, 3],
                           cal=([1, "left"], [2, "left"], [3, "left"],))
        mc.text(l="Initial Limb: ")
        mc.radioButtonGrp("selLegType_rbg", la2=["Left", "Right"], nrb=2, sl=1, cw2=[50, 50], )
        mc.setParent("..")
        mc.separator(st="in", h=20, w=500)

        # sources
        mc.rowColumnLayout(nc=2, cw=[(1, 100), (2, 380)], cs=[1, 5], rs=[1, 3])
        mc.text(bgc=(0.85, 0.65, 0.25), l="Heel Locator: ")
        mc.textFieldButtonGrp("locLoad_tfbg", cw=(1, 322), bl="  Load  ", tx="LOC_l_heel")

        mc.text(bgc=(0.85, 0.65, 0.25), l="IK Foot CTRL: ")
        mc.textFieldButtonGrp("ctrlIKFootLoad_tf", cw=(1, 322), bl="  Load  ", tx="CTRL_l_foot")

        mc.setParent("..")

        mc.separator(st="in", h=20, w=500)

        # load buttons
        #

        mc.textFieldButtonGrp("locLoad_tfbg", e=True, bc=self.loadSrc1Btn)
        mc.textFieldButtonGrp("ctrlIKFootLoad_tf", e=True, bc=self.loadSrc2Btn)
        # mc.textFieldButtonGrp("jntLegLoad_tf", e=True, bc=self.loadSrc3Btn)

        self.selLoad = []
        self.locArray = []
        mc.showWindow(self.window)

    def createButtonCmd(self, *args):
        mirrorSel = mc.radioButtonGrp("selLegMirrorType_rbg", q=True, select=True)
        lrSel = mc.radioButtonGrp("selLegType_rbg", q=True, select=True)

        locName = mc.textFieldButtonGrp("locLoad_tfbg", q=True, text=True)
        ctrlIKFootCheck = mc.textFieldButtonGrp("ctrlIKFootLoad_tf", q=True, text=True)

        cra4 = CRA4(mirrorSel, lrSel,
                    locName, ctrlIKFootCheck,
                    )

    def loadSrc1Btn(self):
        self.selSrc1 = CRU.tgpLoadLocsBtn("locLoad_tfbg", "locator", "Heel Locator", ["LOC", "heel"])
        print(self.selSrc1)

    def loadSrc2Btn(self):
        self.selSrc2 = CRU.tgpLoadTxBtn("ctrlIKFootLoad_tf", "nurbsCurve", "IK Foot Control", ["CTRL", "foot"],
                                        "control")
        print(self.selSrc2)
