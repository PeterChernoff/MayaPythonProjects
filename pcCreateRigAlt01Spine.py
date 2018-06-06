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
from pcCreateRigAlt00AUtilities import pcCreateRigUtilities as CRU
reload(pcCreateRigAlt00AUtilities)

import pcCreateRigAlt01SpineCode
from pcCreateRigAlt01SpineCode import pcCreateRigAlt01SpineCode as CRA1
reload(pcCreateRigAlt01SpineCode)


class pcCreateRigAlt01SpineTest(UI):
    def __init__(self):
        self.window = "bcWindow"
        self.title = "pcRigSpine"
        self.winSize = (500, 320)

        self.createUI()

    def createCustom(self, *args):
        # selection type
        mc.rowColumnLayout(nc=2, cw=[(1, 500), (2, 500)], cs=[1, 5], rs=[1, 3])

        mc.text(l="Select The BND Spine Root: ")
        mc.text(l="")

        mc.setParent("..")
        mc.separator(st="in", h=17, w=500)

        # sources
        mc.rowColumnLayout(nc=2, cw=[(1, 100), (2, 380)], cs=[1, 5], rs=[1, 3])
        mc.text(bgc=(0.85, 0.65, 0.25), l="BND Spine Joints: ")
        mc.textFieldButtonGrp("jointLoad_tfbg", cw=(1, 322), bl="  Load  ", tx="JNT_BND_spine1")

        mc.setParent("..")

        mc.separator(st="in", h=17, w=500)

        mc.rowColumnLayout(nc=2, cw=[(1, 120), (2, 380)], cs=[1, 5], rs=[1, 3])
        mc.checkBox("selGeo_cb", l="Affect Geometry", en=True, v=True)
        mc.checkBox("selStretch_cb", l="Include Stretchable Spine Toggle", en=True, v=True)
        mc.setParent("..")
        # load buttons
        mc.textFieldButtonGrp("jointLoad_tfbg", e=True, bc=self.loadSrc1Btn)

        mc.showWindow(self.window)

    def createButtonCmd(self, *args):
        checkGeo = mc.checkBox("selGeo_cb", q=True, v=True)
        checkStretch = mc.checkBox("selStretch_cb", q=True, v=True)
        bndJnt = mc.textFieldButtonGrp("jointLoad_tfbg", q=True, text=True)
        cra1 = CRA1(checkGeo, checkStretch, bndJnt)

    def loadSrc1Btn(self):
        self.selSrc1 = CRU.tgpLoadJntsBtn("jointLoad_tfbg", "joint", "Root Spine BND", ["JNT", "_BND_", "spine", "1"])
        print(self.selSrc1)
