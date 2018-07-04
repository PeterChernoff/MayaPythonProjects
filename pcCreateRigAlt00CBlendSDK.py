'''
Created on May 30, 2014
for Tin Girl Book and game project

@author: Eyal Assaf
'''
import maya.cmds as mc
# import tgpUtils as ut
from functools import partial
from tgpBaseUI import BaseUI as UI

import pcCreateRigAlt00AUtilities

reload(pcCreateRigAlt00AUtilities)

from pcCreateRigAlt00AUtilities import pcCreateRigUtilities as CRU
from pcCreateRigAlt00DRenameBlendshapeCopies import pcCreateRigAlt00DRenameBlendshapeCopies as CRAd

import pcCreateRigAlt00CBlendSDKCode

reload(pcCreateRigAlt00CBlendSDKCode)
from pcCreateRigAlt00CBlendSDKCode import pcCreateRigAlt00CBlendSDKCode as CRAc


class pcCreateRigAlt00CBlendSDK(UI):
    def __init__(self):

        self.window = "bcWindow"
        self.title = "pcRigBlendSDK"
        self.winSize = (500, 200)

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

        mc.text(l="Select the Mesh")

        mc.text(l="")

        mc.setParent("..")
        mc.separator(st="in", h=15, w=500)

        # sources

        mc.rowColumnLayout(nc=2, cw=[(1, 100), (2, 380)], cs=[1, 5], rs=[1, 3])

        mc.text(bgc=(0.85, 0.65, 0.25), l="Geometry: ")
        mc.textFieldButtonGrp("mshCharLoad_tf", cw=(1, 322), bl="  Load  ", tx="GEO_woman")

        mc.setParent("..")
        mc.separator(st="in", h=15, w=500)
        # load buttons
        #

        mc.textFieldButtonGrp("mshCharLoad_tf", e=True, bc=self.loadSrc1Btn)

        self.selLoad = []
        self.ctrlsArray = []
        mc.showWindow(self.window)

    def createButtonCmd(self, *args):

        mc.textFieldButtonGrp("mshCharLoad_tf", e=True, bc=self.loadSrc1Btn)

        mshCharCheck = mc.textFieldButtonGrp("mshCharLoad_tf", q=True, text=True)
        mshChar = self.tgpGetTx(mshCharCheck, "mshCharLoad_tf", "mesh", "Body mesh", ["GEO"])

        CRAc(mshChar, renameVals=True)

    def loadSrc1Btn(self):
        self.selSrc1 = self.tgpLoadTxBtn("mshCharLoad_tf", "mesh", "Body mesh", ["GEO"])
        print(self.selSrc1)

    def tgpLoadTxBtn(self, loadBtn, objectType, objectDesc, keywords, objectNickname=None):
        if objectNickname is None:
            objectNickname = objectType

        self.selLoad = []
        self.selLoad = mc.ls(sl=True, fl=True, type="transform")

        if (len(self.selLoad) != 1):
            mc.warning("Select only the {0}".format(objectDesc))
            return
        else:
            selName = self.selLoad[0]
            selName = self.tgpGetTx(selName, loadBtn, objectType, objectDesc, keywords, objectNickname)

            return selName

    def tgpGetTx(self, selName, loadBtn, objectType, objectDesc, keywords, objectNickname=None, ):

        if CRU.checkObjectType(selName) != objectType:
            mc.warning("{0} should be a {1}".format(objectDesc, objectNickname))
            return

        if not all(word.lower() in selName.lower() for word in keywords):
            mc.warning("That is the wrong {0}. Select the {1}".format(objectNickname, objectDesc))
            return
        mc.textFieldButtonGrp(loadBtn, e=True, tx=selName)
        return selName
