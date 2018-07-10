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

import pcCreateRigAlt00ECreateRig
from pcCreateRigAlt00ECreateRig import pcCreateRigAlt00ECreateRig as CRAE

reload(pcCreateRigAlt00ECreateRig)


class pcCreateRigAlt00FCreateRigUI(UI):
    def __init__(self):
        self.window = "bcWindow"
        self.title = "pcRigComplete"
        self.winSize = (500, 200)

        self.createUI()

    def createCustom(self, *args):
        # selection type
        mc.rowColumnLayout(nc=2, cw=[(1, 500), (2, 500)], cs=[1, 5], rs=[1, 3])

        mc.text(l="Run The Script")
        mc.text(l="")

        mc.setParent("..")
        mc.separator(st="in", h=17, w=500)

        mc.rowColumnLayout(nc=2, cw=[(1, 120), (2, 380)], cs=[1, 5], rs=[1, 3])
        mc.checkBox("selGeo_cb", l="Affect Geometry", en=True, v=False)

        mc.setParent("..")
        # load buttons

        mc.showWindow(self.window)

    def createButtonCmd(self, *args):
        cbGeo = mc.checkBox("selGeo_cb", q=True, v=True)
        CRAE(cbGeo)
