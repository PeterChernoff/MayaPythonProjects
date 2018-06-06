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

import pcCreateRigAlt02HeadCode
from pcCreateRigAlt02HeadCode import pcCreateRigAlt02HeadCode as CRA2

reload(pcCreateRigAlt02HeadCode)


class pcCreateRigAlt02HeadTest(UI):
    def __init__(self):
        self.window = "bcWindow"
        self.title = "pcRigHead"
        self.winSize = (500, 550)

        self.createUI()

    def createCustom(self, *args):
        '''
        #
        #
        #
        #
        #
        '''
        # selection type
        mc.rowColumnLayout(nc=2, cw=[(1, 500), (2, 500)], cs=[1, 5], rs=[1, 3])

        mc.text(l="Select The BND Neck Root: ")
        mc.text(l="")
        mc.setParent("..")
        mc.separator(st="in", h=17, w=500)
        mc.checkBox("selSpineEnd_cb", l="Connect To Spine", en=True, v=True)

        mc.separator(st="in", h=17, w=500)

        # sources
        mc.rowColumnLayout(nc=2, cw=[(1, 140), (2, 360)], cs=[1, 5], rs=[1, 3])
        mc.text(bgc=(0.85, 0.65, 0.25), l="Neck Start Joint: ")
        mc.textFieldButtonGrp("jointLoad_tfbg", cw=(1, 300), bl="  Load  ", tx="JNT_BND_neck1")

        mc.text(bgc=(0.85, 0.65, 0.25), l="IK Shoulder Joint: ")
        mc.textFieldButtonGrp("jntIKShoulderLoad_tf", cw=(1, 300), bl="  Load  ", tx="JNT_IK_shoulder")

        mc.text(bgc=(0.85, 0.65, 0.25), l="Torso DNT Group: ")
        mc.textFieldButtonGrp("grpTorsoDNT_tfbg", cw=(1, 300), bl="  Load  ", tx="GRP_DO_NOT_TOUCH_torso")

        mc.text(bgc=(0.85, 0.65, 0.25), l="Root Transform Control: ")
        mc.textFieldButtonGrp("rootTrans_tfbg", cw=(1, 300), bl="  Load  ", tx="CTRL_rootTransform")

        mc.text(bgc=(0.85, 0.65, 0.25), l="Head Joint Extras: ")
        mc.textFieldButtonGrp("jntHead_tfbg", cw=(1, 300), bl="  Load  ", tx="JNT_BND_head")

        mc.text(bgc=(0.85, 0.65, 0.25), l="Shoulder Control: ")
        mc.textFieldButtonGrp("ctrlShoulderLoad_tf", cw=(1, 300), bl="  Load  ", tx="CTRL_shoulder")

        mc.text(bgc=(0.85, 0.65, 0.25), l="Spine End Joint: ")
        mc.textFieldButtonGrp("jntSpineEndLoad_tf", cw=(1, 300), bl="  Load  ", tx="JNT_BND_spineEnd")

        mc.separator(st="in", h=15, w=500)
        mc.setParent("..")

        mc.rowColumnLayout(nc=2, cw=[(1, 100), (2, 400)], cs=[1, 5], rs=[1, 3])
        mc.checkBox("selGeo_cb", l="Affect Geometry", en=True, v=True)

        mc.setParent("..")
        mc.separator(st="in", h=15, w=500)

        # Attributes
        mc.rowColumnLayout(nc=2, cw=[(1, 100), (2, 370)], cs=[1, 5], rs=[1, 3])
        mc.text(l="Extra Controls: ")
        mc.checkBoxGrp("attrSelExtra_rbg", la2=["Jaw", "Eyes", ],
                       ncb=2, va2=[1, 1], cw2=[70, 60])

        mc.setParent("..")
        mc.separator(st="in", h=15, w=500)

        mc.rowColumnLayout(nc=2, cw=[(1, 100), (2, 370)], cs=[1, 5], rs=[1, 3])
        mc.text(l="Toggle\nStretchable: ")
        mc.checkBoxGrp("setStretch_rgp", la2=["Torso", "Neck", ],
                       ncb=2, va2=[1, 1], cw2=[70, 60])

        mc.setParent("..")

        mc.separator(st="in", h=15, w=500)

        # load buttons
        mc.textFieldButtonGrp("jointLoad_tfbg", e=True, bc=self.loadSrc1Btn)
        mc.textFieldButtonGrp("jntIKShoulderLoad_tf", e=True, bc=self.loadSrc2Btn)
        mc.textFieldButtonGrp("grpTorsoDNT_tfbg", e=True, bc=self.loadSrc3Btn)
        mc.textFieldButtonGrp("rootTrans_tfbg", e=True, bc=self.loadSrc4Btn)
        mc.textFieldButtonGrp("jntHead_tfbg", e=True, bc=self.loadSrc5Btn)
        mc.textFieldButtonGrp("ctrlShoulderLoad_tf", e=True, bc=self.loadSrc6Btn)
        mc.textFieldButtonGrp("jntSpineEndLoad_tf", e=True, bc=self.loadSrc7Btn)

        mc.showWindow(self.window)

    def createButtonCmd(self, *args):
        cbGeo = mc.checkBox("selGeo_cb", q=True, v=True)
        cbSpine = mc.checkBox("selSpineEnd_cb", q=True, v=True)

        jntIKShoulderCheck = mc.textFieldButtonGrp("jntIKShoulderLoad_tf", q=True, text=True)
        grpTorsoDNTCheck = mc.textFieldButtonGrp("grpTorsoDNT_tfbg", q=True, text=True)

        ctrlRootTransCheck = mc.textFieldButtonGrp("rootTrans_tfbg", q=True, text=True)
        bndJnt = mc.textFieldButtonGrp("jointLoad_tfbg", q=True, text=True)
        jntHead = mc.textFieldButtonGrp("jntHead_tfbg", q=True, text=True)

        ctrlShoulderCheck = mc.textFieldButtonGrp("ctrlShoulderLoad_tf", q=True, text=True)
        jntSpineEndCheck = mc.textFieldButtonGrp("jntSpineEndLoad_tf", q=True, text=True)

        cbJaw = mc.checkBoxGrp("attrSelExtra_rbg", q=True, v1=True)
        cbEyes = mc.checkBoxGrp("attrSelExtra_rbg", q=True, v2=True)

        cbTorso = mc.checkBoxGrp("setStretch_rgp", q=True, v1=True)
        cbNeck = mc.checkBoxGrp("setStretch_rgp", q=True, v2=True)

        cra2 = CRA2(cbGeo, cbSpine,
                    jntIKShoulderCheck, grpTorsoDNTCheck,
                    ctrlRootTransCheck, bndJnt, jntHead,
                    ctrlShoulderCheck, jntSpineEndCheck,
                    cbJaw, cbEyes,
                    cbTorso, cbNeck, )

    def loadSrc1Btn(self):
        self.selSrc1 = CRU.tgpLoadJntsBtn("jointLoad_tfbg", "joint", "Root Neck Joint", ["JNT", "BND", "neck", "1"])
        print(self.selSrc1)

    def loadSrc2Btn(self):
        self.selSrc2 = CRU.tgpLoadTxBtn("jntIKShoulderLoad_tf", "joint", "IK Shoulder Joint",
                                        ["JNT", "_IK_", "shoulder"], "control")
        print(self.selSrc2)

    def loadSrc3Btn(self):
        self.selSrc3 = CRU.tgpLoadTxBtn("grpTorsoDNT_tfbg", "transform", "DO NOT TOUCH Torso Group",
                                        ["GRP", "DO", "NOT", "TOUCH"],
                                        "group")
        print(self.selSrc3)

    def loadSrc4Btn(self):
        self.selSrc4 = CRU.tgpLoadTxBtn("rootTrans_tfbg", "nurbsCurve", "Root Transform Control",
                                        ["CTRL", "rootTransform"], "control")
        print(self.selSrc4)

    def loadSrc5Btn(self):
        self.selSrc5 = CRU.tgpLoadJntsBtn("jntHead_tfbg", "joint", "Head Joint",
                                          ["JNT", "BND", "head"])
        print(self.selSrc5)

    def loadSrc6Btn(self):
        self.selSrc6 = CRU.tgpLoadTxBtn("ctrlShoulderLoad_tf", "nurbsCurve", "Shoulder Control",
                                        ["CTRL", "shoulder"], "Control")
        print(self.selSrc6)

    def loadSrc7Btn(self):
        self.selSrc7 = CRU.tgpLoadTxBtn("jntSpineEndLoad_tf", "joint", "Spine End",
                                        ["JNT", "BND", "spineEnd"])
        print(self.selSrc7)
