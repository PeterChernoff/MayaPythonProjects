'''
Created on May 30, 2014
for Tin Girl Book and game project

@author: Eyal Assaf
'''
import maya.cmds as mc
# import tgpUtils as ut
from functools import partial
from tgpBaseUI import BaseUI as UI

import pcCreateRigUtilities
from pcCreateRigUtilities import pcCreateRigUtilities as CRU

reload(pcCreateRigUtilities)


class pcCreateRigHead(UI):
    def __init__(self):

        self.window = "bcWindow"
        self.title = "pcRigHead"
        self.winSize = (500, 320)

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

        mc.text(l="Select The Neck Root: ")
        mc.text(l="")
        mc.checkBox("selGeo_cb", l="Affect Geometry", en=True, v=True)
        mc.setParent("..")
        mc.separator(st="in", h=20, w=500)
        mc.checkBox("selSpineEnd_cb", l="Connect To Spine", en=True, v=True)

        mc.separator(st="in", h=20, w=500)

        # sources
        mc.rowColumnLayout(nc=2, cw=[(1, 100), (2, 370)], cs=[1, 5], rs=[1, 3])
        mc.text(bgc=(0.85, 0.65, 0.25), l="Joints: ")
        mc.textFieldButtonGrp("jointLoad_tfbg", cw=(1, 322), bl="  Load  ")

        mc.setParent("..")

        mc.rowColumnLayout(nc=2, cw=[(1, 100), (2, 370)], cs=[1, 5], rs=[1, 3])
        mc.text(bgc=(0.85, 0.65, 0.25), l="IK Chest CTRL: ")
        mc.textFieldButtonGrp("ctrlIKChestLoad_tf", cw=(1, 322), bl="  Load  ", tx="CTRL_IK_chest")

        mc.setParent("..")

        mc.rowColumnLayout(nc=2, cw=[(1, 100), (2, 370)], cs=[1, 5], rs=[1, 3])
        mc.text(bgc=(0.85, 0.65, 0.25), l="Spine Rig GRP: ")
        mc.textFieldButtonGrp("jointJNTSpine_tfbg", cw=(1, 322), bl="  Load  ", tx="GRP_JNT_spine")

        mc.setParent("..")

        mc.rowColumnLayout(nc=2, cw=[(1, 100), (2, 370)], cs=[1, 5], rs=[1, 3])
        mc.text(bgc=(0.85, 0.65, 0.25), l="COG: ")
        mc.textFieldButtonGrp("cog_tfbg", cw=(1, 322), bl="  Load  ", tx="CTRL_COG")

        mc.setParent("..")

        mc.separator(st="in", h=20, w=500)

        # Attributes


        # load buttons
        mc.textFieldButtonGrp("jointLoad_tfbg", e=True, bc=self.loadSrc1Btn)
        mc.textFieldButtonGrp("ctrlIKChestLoad_tf", e=True, bc=self.loadSrc2Btn)
        mc.textFieldButtonGrp("jointJNTSpine_tfbg", e=True, bc=self.loadSrc3Btn)
        mc.textFieldButtonGrp("cog_tfbg", e=True, bc=self.loadSrc4Btn)

        #
        #

        #

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
        '''self.src1Sel = self.tgpLoadTxBtn("jointLoad_tfbg", "selType_rbg", "selGeo_cb")'''
        self.jntSel = self.tgpLoadTxBtn("jointLoad_tfbg")
        print(self.jntSel)

    def loadSrc2Btn(self):
        '''self.src1Sel = self.tgpLoadTxBtn("jointLoad_tfbg", "selType_rbg", "selGeo_cb")'''
        self.ctrlSel = self.tgpLoadIKCtrl("ctrlIKChestLoad_tf")
        print(self.ctrlSel)

    def loadSrc3Btn(self):
        '''self.src1Sel = self.tgpLoadTxBtn("jointLoad_tfbg", "selType_rbg", "selGeo_cb")'''
        self.grpSel = self.tgpLoadRigBtn("jointJNTSpine_tfbg")
        print(self.grpSel)

    def loadSrc4Btn(self):
        '''self.src1Sel = self.tgpLoadTxBtn("jointLoad_tfbg", "selType_rbg", "selGeo_cb")'''
        self.grpSel2 = self.tgpLoadCOGBtn("cog_tfbg")
        print(self.grpSel2)

    def tgpLoadIKCtrl(self, loadBtn):
        self.selLoad = []
        self.selLoad = mc.ls(sl=True, fl=True, type="transform")

        if (len(self.selLoad) != 1):
            mc.warning("Select only the IK Control")
            return
        else:
            if CRU.checkObjectType(self.selLoad[0]) != "nurbsCurve":
                mc.warning("The IK Chest Control should be a nurbsCurve")
                return
            selName = self.selLoad[0]
            mc.textFieldButtonGrp(loadBtn, e=True, tx=selName)
            print(selName)

    def tgpLoadRigBtn(self, loadBtn):
        self.selLoad = []
        self.selLoad = mc.ls(sl=True, fl=True, type="transform")

        if (len(self.selLoad) != 1):
            mc.warning("Select only the rig Group")
            return
        else:

            if CRU.checkObjectType(self.selLoad[0]) != "transform":
                mc.warning("The Spine Rig Group should only be a transform")
                return
            selName = self.selLoad[0]
            mc.textFieldButtonGrp(loadBtn, e=True, tx=selName)

    def tgpLoadCOGBtn(self, loadBtn):
        self.selLoad = []
        self.selLoad = mc.ls(sl=True, fl=True, type="transform")

        if (len(self.selLoad) != 1):
            mc.warning("Select only the COG Control")
            return
        else:
            if CRU.checkObjectType(self.selLoad[0]) != "nurbsCurve":
                mc.warning("The Control should be a nurbsCurve")
                return
            selName = self.selLoad[0]
            mc.textFieldButtonGrp(loadBtn, e=True, tx=selName)

    def tgpLoadTxBtn(self, loadBtn):
        # hierarchy
        self.selLoad = []
        self.selLoad = mc.ls(sl=True, fl=True, type="joint")
        if (len(self.selLoad) != 1):
            mc.warning("Select only the root joint")
            return
        else:

            selName = ', '.join(self.selLoad)
            mc.textFieldButtonGrp(loadBtn, e=True, tx=selName)

            # get the children joints
            self.parent = self.selLoad[0]
            self.child = mc.listRelatives(self.selLoad, ad=True, type="joint")
            # collect the joints in an array
            self.jointArray = [self.parent]
            # reverse the order of the children joints
            self.child.reverse()

            # add to the current list
            self.jointArray.extend(self.child)

            # removes if the last joint is End
            # checks if the last three letters are "End"
            self.jointEndArray = [x for x in self.jointArray if "End" in x[-3:]]
            # print(self.jointEndArray)
            self.jointArray = [x for x in self.jointArray if "End" not in x[-3:]]
            # print(self.jointArray)

        return self.jointArray

    def createNeckHeadCtrls(self, ctrlIKChest, grpJntSpine, checkboxSpine, *args):
        listCtrls = ["neck", "head", "jaw1"]
        headOffsetCtrls = []
        specVal = 0
        for i in range(len(self.jointArray)):
            val = str(self.jointArray[i])
            colourTU = 17

            if any(x in val for x in listCtrls):
                # print("val = {0}".format(val))
                # if the neck, do the following
                if listCtrls[0] in val:
                    sizeCtrl = 10
                    orntVal = (0, 1, 0)
                    headOffsetCtrls.append(
                        CRU.createCTRLs(val, prnt=False, ornt=True, size=sizeCtrl, orientVal=orntVal, colour=colourTU))

                    child = mc.listRelatives(val, c=True)[0]
                    boneLength = mc.getAttr("{0}.ty".format(child))

                    mc.select(headOffsetCtrls[specVal][1] + ".cv[:]")
                    mc.move(boneLength * .2, z=True, r=True, os=True, wd=True)
                elif listCtrls[1] in val:
                    # if the head, do the following
                    sizeCtrl = 15
                    orntVal = (0, 1, 0)

                    boneLength = mc.getAttr("{0}End.ty".format(val))
                    headOffsetCtrls.append(
                        CRU.createCTRLs(val, prnt=False, ornt=True, size=sizeCtrl, orientVal=orntVal, colour=colourTU))
                    mc.select(headOffsetCtrls[specVal][1] + ".cv[:]")
                    mc.move(boneLength * .65, y=True, r=True)

                elif listCtrls[2] in val:
                    # if the jaw, do the following
                    sizeCtrl = 3
                    orntVal = (0, 1, 0)
                    # get the length of the bone
                    getBoneChild = mc.listRelatives(val, type="joint", ad=True)
                    boneLength = mc.getAttr("{0}.ty".format(getBoneChild[0]))
                    boneLength2 = mc.getAttr("{0}.ty".format(getBoneChild[1]))
                    # print(boneLength)
                    # print(boneLength2)
                    headOffsetCtrls.append(
                        CRU.createCTRLs(val, prnt=False, ornt=True, size=sizeCtrl, orientVal=orntVal, colour=colourTU))
                    # move the CVs into place
                    mc.select(headOffsetCtrls[specVal][1] + ".cv[:]")
                    mc.move(0, -boneLength2 * 2, boneLength * 1.1, r=True)

                specVal += 1

        mc.parent(headOffsetCtrls[1][0], headOffsetCtrls[0][1])
        mc.parent(headOffsetCtrls[2][0], headOffsetCtrls[1][1])
        mc.parent(headOffsetCtrls[3][0], headOffsetCtrls[2][1])

        # CTRL_neck1 point constrains JNT_neck1
        # parent OFFSET_CTRL_neck1 under CTRL_IK_chest
        if checkboxSpine:
            mc.pointConstraint(headOffsetCtrls[0][1], self.jointArray[0])
            noUnicode = str(self.jointArray[0])
            grpHead = mc.group(n="GRP_JNT_head", w=True, em=True)
            mc.parent(noUnicode, grpHead)

            mc.parent(headOffsetCtrls[0][0], ctrlIKChest)

            # was originally GRP_JNT_torso, but changed to GRP_rig_torso
            grpTorso = mc.group(n="GRP_rig_torso", w=True, em=True)
            mc.parent(grpHead, grpJntSpine, grpTorso)

        return headOffsetCtrls

    def createEyeControls(self, eyeArray, headOffsetCtrls, *args):
        # Create eye control
        eyeCtrlArray = []

        eyeOffsetArray = []

        radiusBase = mc.getAttr("{0}.ty".format(self.jointEndArray[-1]))

        for i in range(len(eyeArray)):
            # takes the eye joints, creates a corresponding locator
            eyeName = str(eyeArray[i]).replace("JNT_", "")
            eyeCtrlArray.append(mc.spaceLocator(p=(0, 0, 0), name="CTRL_" + eyeName)[0])
            # print(eyeCtrlArray[i])

            mc.setAttr('{0}.overrideEnabled'.format(eyeCtrlArray[i]), 1)
            if "_l_" in eyeCtrlArray[i]:
                mc.setAttr("{0}.overrideColor".format(eyeCtrlArray[i]), 14)
                # print("Left")
            elif "_r_" in eyeCtrlArray[i]:
                mc.setAttr("{0}.overrideColor".format(eyeCtrlArray[i]), 13)
                # print("Right")

            # groups them at the creation point
            autoGrp = mc.group(eyeCtrlArray[i], name="AUTO_" + eyeName)
            eyeOffsetArray.append(mc.group(autoGrp, name="OFFSET_" + eyeName))

            # moves the eye into posiiton
            todelete = mc.parentConstraint(eyeArray[i], eyeOffsetArray[i], mo=False)
            mc.delete(todelete)

            mc.move(radiusBase * 2, eyeOffsetArray[i], z=True, r=True)

        # print(eyeCtrlArray)
        # Create the eyes control
        eyesCtrlName = "CTRL_eyes"
        eyesCtrl = mc.circle(nr=(0, 1, 0), r=radiusBase * .75, n=eyesCtrlName, degree=1, sections=4)[0]

        mc.setAttr("{0}.ry".format(eyesCtrl), 45)
        mc.makeIdentity(eyesCtrl, a=True)  # freeze transform
        mc.setAttr("{0}.sx".format(eyesCtrl), 1.5)
        mc.makeIdentity(eyesCtrl, a=True)  # freeze transform
        mc.setAttr("{0}.rx".format(eyesCtrl), 90)
        mc.makeIdentity(eyesCtrl, a=True)  # freeze transform

        eyesAuto = mc.group(eyesCtrl, n="AUTO_" + eyesCtrlName)

        eyesOffset = mc.group(eyesAuto, n="OFFSET_" + eyesCtrlName)

        todelete = mc.pointConstraint(eyeCtrlArray, eyesOffset)
        mc.delete(todelete)

        mc.parent(eyeOffsetArray, eyesCtrl)

        aimArray = []
        for i in range(len(eyeArray)):
            aimArray.append(mc.aimConstraint(eyeCtrlArray[i], eyeArray[i], aim=[0, 0, 1]))

        # create the eye follow settings
        eyesFollowLocArray = []

        eyesFollowLocArray.append(mc.spaceLocator(p=(0, 0, 0), name="LOC_eyesHeadFollow")[0])
        eyesFollowLocArray.append(mc.spaceLocator(p=(0, 0, 0), name="LOC_eyesWorldFollow")[0])

        for i in range(len(eyesFollowLocArray)):
            todelete = mc.parentConstraint(eyesCtrl, eyesFollowLocArray[i], mo=False)
            mc.delete(todelete)
        headCtrl = ""
        for i in range(len(headOffsetCtrls)):
            if "head" in headOffsetCtrls[i][1]:
                headCtrl = headOffsetCtrls[i][1]

        mc.parent(eyesFollowLocArray[0], headCtrl)

        eyesCtrlPrntConst = mc.parentConstraint(eyesFollowLocArray[0], eyesFollowLocArray[1], eyesOffset)[0]

        mc.addAttr(eyesCtrl, longName='eyesFollow', at="enum", enumName="Head:World", k=True)

        # The last two attributes would be the relevant head and eye controls
        eyesFollow = mc.listAttr(eyesCtrlPrntConst)[-2:]

        CRU.setDriverDrivenValues(eyesCtrl, "eyesFollow", eyesCtrlPrntConst, eyesFollow[0], 0, 1)
        CRU.setDriverDrivenValues(eyesCtrl, "eyesFollow", eyesCtrlPrntConst, eyesFollow[0], 1, 0)

        CRU.setDriverDrivenValues(eyesCtrl, "eyesFollow", eyesCtrlPrntConst, eyesFollow[1], 0, 0)
        CRU.setDriverDrivenValues(eyesCtrl, "eyesFollow", eyesCtrlPrntConst, eyesFollow[1], 1, 1)

        for i in range(len(eyesFollowLocArray)):
            mc.setAttr("{0}.v".format(eyesFollowLocArray[i]), False)

        grpWorldFollow = mc.group(n="GRP_LOC_follow", w=True, em=True)

        mc.parent(eyesFollowLocArray[1], grpWorldFollow)

        return headCtrl, eyeCtrlArray, eyesCtrl, grpWorldFollow

    def createSpaceSwitching(self, headCtrl, headOffsetCtrls, ctrlIKChest, ctrlCOG, grpWorldFollow, *args):
        # creates the head follow attributes
        eyesHeadLocArray = []
        eyesHeadLocArray.append(mc.spaceLocator(p=(0, 0, 0), name="LOC_headNeckFollow")[0])
        eyesHeadLocArray.append(mc.spaceLocator(p=(0, 0, 0), name="LOC_headTorsoFollow")[0])
        eyesHeadLocArray.append(mc.spaceLocator(p=(0, 0, 0), name="LOC_headCOGFollow")[0])
        eyesHeadLocArray.append(mc.spaceLocator(p=(0, 0, 0), name="LOC_headWorldFollow")[0])

        # moves these to the CTRL_head
        for i in range(len(eyesHeadLocArray)):
            todelete = mc.parentConstraint(headCtrl, eyesHeadLocArray[i], mo=False)
            mc.delete(todelete)

        headFollowOrntConstr = mc.orientConstraint(eyesHeadLocArray, headCtrl)[0]
        mc.addAttr(headCtrl, longName='headFollow', at="enum", enumName="Neck:Torso:COG:World", k=True)
        # print(headFollowOrntConstr)

        # grab the last 4 attributes
        headSpaceFollow = mc.listAttr(headFollowOrntConstr)[-4:]
        # print(headSpaceFollow)
        for i in range(len(headSpaceFollow)):
            # set the driven key to 1 and the undriven keys to 0

            CRU.setDriverDrivenValues(headCtrl, "headFollow", headFollowOrntConstr, headSpaceFollow[i], i, 1)
            print("-------")
            print(headSpaceFollow[i])
            for i2 in range(len(headSpaceFollow)):
                if i2 != i:
                    # need to have the second to last value be i, not i2
                    CRU.setDriverDrivenValues(headCtrl, "headFollow", headFollowOrntConstr, headSpaceFollow[i2], i, 0)
                    print(headSpaceFollow[i2])

        locParents = [headOffsetCtrls[1][1], ctrlIKChest, ctrlCOG, grpWorldFollow]
        # print(locParents)
        # parent LOC_headNeckFollow under CTRL_neck2
        # parent LOC_headTorsoFollow under CTRL_IK_chest
        # parent LOC_headCOGFollow under CTRL_COG
        # parent LOC_headWorldFollow under GRP_LOC_worldFollow
        for i in range(len(eyesHeadLocArray)):
            mc.parent(eyesHeadLocArray[i], locParents[i])
            mc.setAttr("{0}.v".format(eyesHeadLocArray[i]), False)

    def neckCleanUp(self, headOffsetCtrls, eyeCtrlArray, eyesCtrl, *args):

        for i in range(len(headOffsetCtrls)):
            CRU.lockHideCtrls(headOffsetCtrls[i][1], translate=True, scale=True, visible=True)

        for i in range(len(eyeCtrlArray)):
            CRU.lockHideCtrls(eyeCtrlArray[i], scale=True, visible=True)

        CRU.lockHideCtrls(eyesCtrl, scale=True, visible=True)

    def tgpMakeBC(self, *args):
        checkGeo = mc.checkBox("selGeo_cb", q=True, v=True)
        checkboxSpine = mc.checkBox("selSpineEnd_cb", q=True, v=True)
        if checkboxSpine:
            ctrlIKChest = mc.textFieldButtonGrp("ctrlIKChestLoad_tf", q=True, text=True)
            grpJntSpine = mc.textFieldButtonGrp("jointJNTSpine_tfbg", q=True, text=True)
            ctrlCOG = mc.textFieldButtonGrp("cog_tfbg", q=True, text=True)

        self.jntNames = mc.textFieldButtonGrp("jointLoad_tfbg", q=True, text=True)

        # make sure the selections are not empty
        checkList = [self.jntNames]

        eyeArray = [x for x in self.jointArray if "eye" in x]

        # gets us most of the geos
        jntArrayNoEnd = [x for x in self.jointArray if "End" not in x]

        # print(eyeArray)

        if ((checkList[0] == "")):
            mc.warning("You are missing a selection!")
            return
        else:
            if "neck1" not in checkList[0]:
                mc.warning("Make the first selection the root neck joint")
                return

            # CRU.createLocatorToDelete()
            # create the IK base controls
            # Creating the Neck and Head Controls.

            headOffsetCtrls = self.createNeckHeadCtrls(ctrlIKChest, grpJntSpine, checkboxSpine)

            headCtrl, eyeCtrlArray, eyesCtrl, grpWorldFollow = self.createEyeControls(eyeArray, headOffsetCtrls)

            if checkboxSpine:
                self.createSpaceSwitching(headCtrl, headOffsetCtrls, ctrlIKChest, ctrlCOG, grpWorldFollow, )

            self.neckCleanUp(headOffsetCtrls, eyeCtrlArray, eyesCtrl)

            if checkGeo:
                CRU.tgpSetGeo(jntArrayNoEnd)
