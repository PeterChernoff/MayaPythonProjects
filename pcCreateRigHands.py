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

reload(pcCreateRigUtilities)
from pcCreateRigUtilities import pcCreateRigUtilities as CRU

class pcCreateRigHands(UI):
    def __init__(self):

        self.window = "bcWindow"
        self.title = "pcRigHand"
        self.winSize = (500, 325)

        self.createUI()

    def createCustom(self, *args):
        # selection type
        mc.rowColumnLayout(nc=3, cw=[(1, 125), (2, 150), (3, 150)], cs=[1, 5], rs=[1, 3],
                           cal=([1, "left"], [2, "left"], [3, "left"],))

        mc.text(l="Mirror Arm As Well?")
        # mc.setParent("..")
        mc.radioButtonGrp("selArmMirrorType_rbg", la2=["No", "Yes"], nrb=2, sl=2, cw2=[50, 50], )
        mc.text(l="")
        mc.setParent("..")
        mc.separator(st="in", h=20, w=500)

        mc.rowColumnLayout(nc=3, cw=[(1, 100), (2, 200), (3, 150)], cs=[1, 5], rs=[1, 3],
                           cal=([1, "left"], [2, "left"], [3, "left"],))
        mc.text(l="Initial Limb: ")
        mc.radioButtonGrp("selArmType_rbg", la2=["Left", "Right"], nrb=2, sl=1, cw2=[50, 50], )
        mc.setParent("..")
        mc.separator(st="in", h=20, w=500)

        # sources
        mc.rowColumnLayout(nc=2, cw=[(1, 100), (2, 370)], cs=[1, 5], rs=[1, 3])
        mc.text(bgc=(0.85, 0.65, 0.25), l="Hand: ")
        mc.textFieldButtonGrp("jointLoad_tfbg", cw=(1, 322), bl="  Load  ")

        mc.text(bgc=(0.85, 0.65, 0.25), l="Arm: ")
        mc.textFieldButtonGrp("armLoad_tfbg", cw=(1, 322), bl="  Load  ", tx="")

        mc.text(bgc=(0.85, 0.65, 0.25), l="FKIK Ctrl: ")
        mc.textFieldButtonGrp("ctrlLoad_tfbg", cw=(1, 322), bl="  Load  ", tx="CTRL_fkikSwitch")

        mc.setParent("..")

        mc.separator(st="in", h=20, w=500)

        mc.rowColumnLayout(nc=2, cw=[(1, 100), (2, 370)], cs=[1, 5], rs=[1, 3])
        mc.checkBox("selGeo_cb", l="Affect Geometry", en=True, v=True)
        mc.setParent("..")

        mc.separator(st="in", h=20, w=500)

        # load buttons
        #
        # TO DELETE: May need to edit so the buttons load things properly
        mc.textFieldButtonGrp("jointLoad_tfbg", e=True, bc=self.loadSrc1Btn)
        mc.textFieldButtonGrp("armLoad_tfbg", e=True, bc=self.loadSrc2Btn)
        mc.textFieldButtonGrp("ctrlLoad_tfbg", e=True, bc=self.loadSrc3Btn)
        # mc.textFieldButtonGrp("ctrlIKChestLoad_tf", e=True, bc=self.loadSrc2Btn)
        # mc.textFieldButtonGrp("jointRigSpine_tfbg", e=True, bc=self.loadSrc3Btn)
        # mc.textFieldButtonGrp("cog_tfbg", e=True, bc=self.loadSrc4Btn)

        self.selLoad = []
        self.jointArray = []
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
        self.jntHandSel = self.tgpLoadTxBtn("jointLoad_tfbg", "joint")
        # print(self.jntHandSel)

    def loadSrc2Btn(self):
        self.jntArmSel = self.tgpLoadArm("armLoad_tfbg")
        # print(self.jntArmSel)

    def loadSrc3Btn(self):
        self.jntCtrl = self.tgpLoadCtrl("ctrlLoad_tfbg")
        # print(self.jntCtrl)

    def tgpLoadCtrl(self, loadBtn):
        self.selLoad = []
        # self.selLoad = mc.ls(sl=True, fl=True, type="nurbsCurve")
        self.selLoad = mc.ls(sl=True, fl=True, type="transform")

        if (len(self.selLoad) != 1):
            mc.warning("Select only the FKIK Control")
            return
        else:
            selName = self.selLoad[0]
            mc.textFieldButtonGrp(loadBtn, e=True, tx=selName)

            return selName

    def tgpLoadArm(self, loadBtn):
        self.selLoad = []
        self.selLoad = mc.ls(sl=True, fl=True, type="joint")

        if (len(self.selLoad) != 1):
            mc.warning("Select only the arm joint")
            return
        else:
            selName = ', '.join(self.selLoad)

            # get the children joints
            self.parent = self.selLoad[0]
            self.child = mc.listRelatives(self.selLoad, ad=True, type="joint")
            # collect the joints in an array
            self.jointArray = [self.parent]
            # reverse the order of the children joints
            if self.child:
                self.child.reverse()
                # add to the current list
                self.jointArray.extend(self.child)

            self.jointArmEndArray = [x for x in self.jointArray if "End" in x[-3:]]

            mc.textFieldButtonGrp(loadBtn, e=True, tx=self.jointArmEndArray[0])

            return self.jointArray

    def tgpLoadTxBtn(self, loadBtn, myType):
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
            self.jointArrayHand = [self.parent]
            # reverse the order of the children joints
            self.child.reverse()

            # add to the current list
            self.jointArrayHand.extend(self.child)

            # removes if the last joint is End

        return self.jointArrayHand

    def createCTRLs(self, s, size=3, prnt=False, ornt=False, pnt=False, orientVal=(1, 0, 0), colour=5, sectionsTU=None,
                    addPrefix=False):
        selname = str(s)
        '''
        0 gray, 1 black, 2 dark grey, 3 light gray, 4 red
        5 dark blue, 6 blue, 7 dark green, 8 dark purple, 9 pink
        10 brown, 11 dark brown, 12 brownish red, 13 light red, 14 green
        15 darkish blue, 16 white, 17 yellow, 18 cyan, 19 greenish blue
        20 light pink, 21 peach, 22 other yellow, 23 turquoise, 24 light brown
        puke yellow
        puke green
        lightish green
        light blue
        darkish blue
        purple
        magenta
        '''

        if addPrefix:
            ctrlName = "CTRL_" + selname
        else:
            ctrlName = selname.replace("JNT_", "CTRL_")

        if sectionsTU:
            ctrl = mc.circle(nr=orientVal, r=size, n=ctrlName, degree=1, sections=sectionsTU)[0]
        else:
            ctrl = mc.circle(nr=orientVal, r=size, n=ctrlName)[0]

        mc.setAttr('{0}.overrideEnabled'.format(ctrlName), 1)
        mc.setAttr("{0}.overrideColor".format(ctrlName), colour)
        auto = mc.group(ctrl, n="AUTO_" + ctrl)
        offset = mc.group(auto, n="OFFSET_" + ctrl)

        mc.parentConstraint(s, offset, mo=0)
        mc.delete(mc.parentConstraint(s, offset))
        # parent and orient/point are not inclusive
        if prnt:
            mc.parentConstraint(ctrl, s, mo=0)
        else:
            if ornt:
                mc.orientConstraint(ctrl, s, mo=0)
            if pnt:
                mc.pointConstraint(ctrl, s, mo=0)
        # we normally don't include auto
        offsetCtrl = [offset, ctrl, auto]
        return offsetCtrl

    def lockHideCtrls(self, s, translate=False, rotate=False, scale=False):
        if translate:
            mc.setAttr("{0}.tx".format(s), k=False, l=True)
            mc.setAttr("{0}.ty".format(s), k=False, l=True)
            mc.setAttr("{0}.tz".format(s), k=False, l=True)
        if rotate:
            mc.setAttr("{0}.rx".format(s), k=False, l=True)
            mc.setAttr("{0}.ry".format(s), k=False, l=True)
            mc.setAttr("{0}.rz".format(s), k=False, l=True)
        if scale:
            mc.setAttr("{0}.sx".format(s), k=False, l=True)
            mc.setAttr("{0}.sy".format(s), k=False, l=True)
            mc.setAttr("{0}.sz".format(s), k=False, l=True)

    def setDriverDrivenValues(self, driver, driverAttribute, driven, drivenAttribute, driverValue, drivenValue,
                              modifyInOut=None, modifyBoth=None):
        # the way it's written, the setDrivenKeyframe is driven-> driver, not the other way around. My custom value does the more intuitive manner
        # modify tanget is determining if the tanget goes in or out
        if modifyInOut or modifyBoth:

            if modifyBoth:
                modifyIn = modifyBoth
                modifyOut = modifyBoth
            else:
                modifyIn = modifyInOut[0]
                modifyOut = modifyInOut[1]
            mc.setDrivenKeyframe('{0}.{1}'.format(driven, drivenAttribute),
                                 cd='{0}.{1}'.format(driver, driverAttribute),
                                 dv=driverValue, v=drivenValue, itt=modifyIn, ott=modifyOut)
        else:
            mc.setDrivenKeyframe('{0}.{1}'.format(driven, drivenAttribute),
                                 cd='{0}.{1}'.format(driver, driverAttribute),
                                 dv=driverValue, v=drivenValue)

    def tgpSetGeo(self, geoJntArray, *args):
        for i in range(len(geoJntArray)):
            try:
                print("------")
                theParent = geoJntArray[i]
                print(theParent)
                geoName = theParent.replace("JNT_", "GEO_")
                print(geoName)
                mc.parent(geoName, theParent)
                print("parent successful")
                pivotTranslate = mc.xform(theParent, q=True, ws=True, rotatePivot=True)
                print("pivotTranslate Successful")
                mc.makeIdentity(geoName, a=True, t=True, r=True, s=True)
                print("make identity Successful")
                mc.xform(geoName, ws=True, pivots=pivotTranslate)
                print("xform Successful")

            except:
                mc.warning("Geo not properly named or available")
                mc.warning("===========")

    def tgpSetDriverArmFKIKSwitch(self, driver, driverAttr, driven, *args):
        w0w1Attr = mc.listAttr(driven)[-2:]
        #print(w0w1Attr)
        self.setDriverDrivenValues(driver, driverAttr, driven, w0w1Attr[0], drivenValue=0, driverValue=1, modifyBoth="linear")
        self.setDriverDrivenValues(driver, driverAttr, driven, w0w1Attr[0], drivenValue=1, driverValue=0, modifyBoth="linear")
        self.setDriverDrivenValues(driver, driverAttr, driven, w0w1Attr[1], drivenValue=0, driverValue=0, modifyBoth="linear")
        self.setDriverDrivenValues(driver, driverAttr, driven, w0w1Attr[1], drivenValue=1, driverValue=1, modifyBoth="linear")

    def createFingerFKs(self, fkJnts, colourTU, isLeft, *args):

        fkJntOffsetCtrls = []
        for fkJnt in fkJnts:
            fkFingerOffsetCtrls = []
            # we want to create FK controls for the fingers except the end
            for i in range(len(fkJnt[:-1])):
                temp = fkJnt[i]
                if i == 0:
                    theSize = 1
                elif "thumb" in temp:
                    theSize = 2
                else:
                    theSize = 1.5
                fkFingerOffsetCtrls.append(self.createCTRLs(temp, size=theSize, ornt=True, colour=colourTU, orientVal=(0, 1, 0)))
                fingerLength = mc.getAttr("{0}.ty".format(fkJnt[i + 1]))
                mc.select(fkFingerOffsetCtrls[i][1] + ".cv[:]")
                if isLeft:
                    moveZ = -3
                else:
                    moveZ = 3
                if i == 0:
                    mc.move(0, fingerLength * 0.9, moveZ, r=True, ls=True)
                else:
                    mc.move(0, fingerLength * 0.5, 0, r=True, ls=True)
            fkJntOffsetCtrls.append(fkFingerOffsetCtrls)

        # parents the fingers fks under each other
        # print(fkJntOffsetCtrls)
        for i in range(len(fkJntOffsetCtrls)):
            for j in range(len(fkJntOffsetCtrls[i]) - 1):
                mc.parent(fkJntOffsetCtrls[i][j + 1][0], fkJntOffsetCtrls[i][j][1])

        return fkJntOffsetCtrls

    def makeHand(self, leftRight, jntsHand, jntArmEnd, jntPalm, colourTU, fkColour, ikColour, ctrlFKIK, ctrlFKIKAttr,
                 isLeft, checkGeo, geoJntArray, *args):
        jntPalmBase = jntPalm[0]

        jntFingers = self.getFingers(jntsHand)
        # create the CTRL, then move it
        handOffsetCtrl = CRU.createCTRLs(jntPalmBase, 5, ornt=True, pnt=True, colour=colourTU, orientVal=(1, 0, 0))
        handLength = mc.getAttr("{0}.ty".format(jntPalm[1]))
        mc.select(handOffsetCtrl[1] + ".cv[:]")
        if isLeft:
            moveX = -5
        else:
            moveX = 5
        mc.move(moveX, handLength * 0.5, 0, r=True, ls=True)

        # get the expression (this is a bit unique to me) then edit it
        armExprName = "expr" + leftRight + "armTwist"
        armExpr = mc.expression(armExprName, q=True, s=True)
        # to delete: may need to replace JNT_armEnd with CTRL_palm
        armExpr = armExpr.replace("armEnd", "palm")
        # print(armExprName)
        # print(armExpr)

        mc.delete(armExprName)

        mc.expression(s=armExpr, n=armExprName)

        # change the rotation order
        toRotateChange = [handOffsetCtrl[1], jntPalmBase]
        # print(toRotateChange)
        self.changeRotateOrder(toRotateChange, "YZX")

        # create locators, groups that contain said locators, then position them at the hand controls
        conFKName = "CON_FK{0}palm".format(leftRight)
        conLocFKOffsetCtrl = []
        conLocFKOffsetCtrl.append(mc.group(n="OFFSET_{0}".format(conFKName), em=True))
        conLocFKOffsetCtrl.append(mc.spaceLocator(p=(0, 0, 0), name=conFKName)[0])
        mc.parent(conLocFKOffsetCtrl[1], conLocFKOffsetCtrl[0])
        # print(conLocFKOffsetCtrl)

        mc.setAttr('{0}.overrideEnabled'.format(conLocFKOffsetCtrl[0]), 1)
        mc.setAttr("{0}.overrideColor".format(conLocFKOffsetCtrl[0]), fkColour)
        mc.setAttr("{0}.localScaleX".format(conLocFKOffsetCtrl[1]), 15)

        conIKName = "CON_IK{0}palm".format(leftRight)
        conLocIKOffsetCtrl = []
        conLocIKOffsetCtrl.append(mc.group(n="OFFSET_{0}".format(conIKName), em=True))
        conLocIKOffsetCtrl.append(mc.spaceLocator(p=(0, 0, 0), name=conIKName)[0])
        mc.parent(conLocIKOffsetCtrl[1], conLocIKOffsetCtrl[0])

        mc.setAttr('{0}.overrideEnabled'.format(conLocIKOffsetCtrl[0]), 1)
        mc.setAttr("{0}.overrideColor".format(conLocIKOffsetCtrl[0]), ikColour)
        mc.setAttr("{0}.localScaleZ".format(conLocIKOffsetCtrl[1]), 15)

        attributes = ["tx", "ty", "tz", "rx", "ry", "rz", ]
        mc.parent(conLocFKOffsetCtrl[0], conLocIKOffsetCtrl[0], handOffsetCtrl[1])
        for attribute in attributes:
            mc.setAttr("{0}.{1}".format(conLocIKOffsetCtrl[0], attribute), 0)
            mc.setAttr("{0}.{1}".format(conLocFKOffsetCtrl[0], attribute), 0)

        mc.parent(conLocFKOffsetCtrl[0], w=True)
        mc.parent(conLocIKOffsetCtrl[0], w=True)

        # attach to the hands
        handOffsetCtrlParentConstraint = \
            mc.parentConstraint(conLocFKOffsetCtrl[1], conLocIKOffsetCtrl[1], handOffsetCtrl[0])[0]
        mc.pointConstraint(jntArmEnd, conLocFKOffsetCtrl[1])
        mc.orientConstraint(jntArmEnd, conLocFKOffsetCtrl[1])

        mc.pointConstraint(jntArmEnd, conLocIKOffsetCtrl[1])

        # set the driven keys
        # def setDriverDrivenValues(self, driver, driverAttribute, driven, drivenAttribute, driverValue, drivenValue, modifyInOut=None, modifyBoth=None):
        self.tgpSetDriverArmFKIKSwitch(ctrlFKIK, ctrlFKIKAttr, handOffsetCtrlParentConstraint)

        # at this point, the cleanup for CON_IK/FK_l_arms would take place in my notes, but why not just name it to begin with? So I did

        grpConPalm = mc.group(n="GRP_CON{0}palm".format(leftRight), w=True, em=True)
        mc.parent(conLocFKOffsetCtrl[0], conLocIKOffsetCtrl[0], grpConPalm)

        # parent the finger offsets under the hands controls. We don't need to do so for the joints since we already assume it to be the case.
        fkFingerOffsetCtrls = self.createFingerFKs(jntFingers, colourTU, isLeft)
        for i in range(len(fkFingerOffsetCtrls)):
            mc.parent(fkFingerOffsetCtrls[i][0][0], handOffsetCtrl[1])



        self.handCleanUp(handOffsetCtrl, fkFingerOffsetCtrls, leftRight, jntPalmBase, grpConPalm)


    def handCleanUp(self, handOffsetCtrl, fkFingerOffsetCtrls, leftRight, jntPalmBase, grpConPalm, *args):

        # I opted to name this armTop because I didn't want the hassle of competing with the old GRP_rig_l_arm
        grpRigArm = mc.group(n="GRP_rig{0}armTop".format(leftRight), w=True, em=True)
        # For the sake of not having a bazillion entries for the input text, I'm just doing this here.
        mc.parent("GRP_CTRL_IK{0}arm".format(leftRight), "GRP_rig{0}arm".format(leftRight),
                  "OFFSET_CTRL{0}shoulder".format(leftRight), jntPalmBase, handOffsetCtrl[0], grpConPalm, grpRigArm)
        self.lockHideCtrls(handOffsetCtrl[1], translate=True, scale=True)
        for i in range(len(fkFingerOffsetCtrls)):
            for j in range(len(fkFingerOffsetCtrls[i])):
                self.lockHideCtrls(fkFingerOffsetCtrls[i][j][1])


    def changeRotateOrder(self, rotateChangeList, getRotOrder, *args):


        for rotateChange in rotateChangeList:
            if (getRotOrder == "XYZ"):
                mc.setAttr(rotateChange + ".rotateOrder", 0)
            elif (getRotOrder == "YZX"):
                mc.setAttr(rotateChange + ".rotateOrder", 1)
            elif (getRotOrder == "ZXY"):
                mc.setAttr(rotateChange + ".rotateOrder", 2)
            elif (getRotOrder == "XZY"):
                mc.setAttr(rotateChange + ".rotateOrder", 3)
            elif (getRotOrder == "YXZ"):
                mc.setAttr(rotateChange + ".rotateOrder", 4)
            elif (getRotOrder == "ZYX"):
                mc.setAttr(rotateChange + ".rotateOrder", 5)

            # print ("Changed Rotate Order for {0} to {1}".format(rotateChange, getRotOrder))
    def getPalm(self, jntsHand, *args):
        return ([x for x in jntsHand if "palm" in x])

    def getFingers(self, jntsHand, *args):
        allFingers = []
        palmLess = [x for x in jntsHand if "palm" not in x]

        indexOfFingers = ["index", "middle", "ring", "pinky", "thumb"]

        for finger in indexOfFingers:
            allFingers.append([x for x in palmLess if finger in x])

        return allFingers

    def tgpMakeBC(self, *args):

        checkSelLeft = mc.radioButtonGrp("selArmType_rbg", q=True, select=True)

        mirrorSel = mc.radioButtonGrp("selArmMirrorType_rbg", q=True, select=True)

        checkGeo = mc.checkBox("selGeo_cb", q=True, v=True)
        ctrlFKIK = mc.textFieldButtonGrp("ctrlLoad_tfbg", q=True, text=True)

        self.jntNames = mc.textFieldButtonGrp("jointLoad_tfbg", q=True, text=True)

        try:
            jntHandRoot = self.jointArrayHand[0]
        except:
            mc.warning("No joint selected!")
            return

        try:
            jntArmEnd = self.jointArmEndArray[0]
        except:
            mc.warning("No joint selected!")
            return

        # print(mirrorSel)
        if mirrorSel == 1:
            mirrorRig = False
        else:
            mirrorRig = True

        listCtrlFKIKAttr = ["l_arm", "r_arm", "l_leg", "r_leg"]
        strRight = "_r_"
        strLeft = "_l_"

        if checkSelLeft == 1:
            isLeft = True
            leftRight = strLeft
            leftRightMirror = strRight
            colourTU = 14
            ikColour = 19
            fkColour = 23
            colourTUMirror = 13
            ikColourMirror = 9
            fkColourMirror = 21
            ctrlFKIKAttr = listCtrlFKIKAttr[0]
            ctrlFKIKAttrMirror = listCtrlFKIKAttr[1]
        else:
            isLeft = False
            leftRight = strRight
            leftRightMirror = strLeft
            colourTU = 13
            ikColour = 9
            fkColour = 21
            colourTUMirror = 14
            ikColourMirror = 19
            fkColourMirror = 23
            ctrlFKIKAttr = listCtrlFKIKAttr[1]
            ctrlFKIKAttrMirror = listCtrlFKIKAttr[0]

        # make sure the selections are not empty
        checkList = [self.jntNames]

        if ((checkList[0] == "")):
            mc.warning("You are missing a selection!")
            return
        else:

            # get the fingers and palm
            jntsHand = self.jntHandSel
            # gets the hand joints
            geoJntArray = [x for x in jntsHand if "End" not in x[-3:]]

            # create the palm controls
            jntPalm = self.getPalm(jntsHand)
            jntPalmBase = jntPalm[0]

            # makeHand(self, leftRight, jntsHand, jntPalm, colourTU, fkColour, ikColour, ctrlFKIK, ctrlFKIKAttr, *args):
            self.makeHand(leftRight, jntsHand, jntArmEnd, jntPalm, colourTU, fkColour, ikColour, ctrlFKIK, ctrlFKIKAttr, isLeft)








            if mirrorRig:
                # create a mirror rig for the hand
                mirrorBase = mc.mirrorJoint(jntPalmBase, mirrorYZ=True, mirrorBehavior=True, searchReplace=[leftRight, leftRightMirror])
                # adds the joints that interact with geometry
                jntsHandMirror = []
                for mb in mirrorBase:
                    if mc.objectType(mb) != "joint":
                        mc.delete(mb)
                    else:
                        if "End" not in mb[-3:]:
                            geoJntArray.append(mb)
                        jntsHandMirror.append(mb)

                #print(geoJntArray)

                jntPalmMirror = self.getPalm(jntsHandMirror)
                jntPalmBasMirror = jntPalmMirror[0]


                jntArmEndMirror = jntArmEnd.replace(leftRight, leftRightMirror)
                isLeftMirror = not isLeft


                self.makeHand(leftRightMirror, jntsHandMirror, jntArmEndMirror, jntPalmMirror, colourTUMirror, fkColourMirror, ikColourMirror, ctrlFKIK, ctrlFKIKAttrMirror,isLeftMirror)

            if checkGeo:
                print(geoJntArray)
                self.tgpSetGeo(geoJntArray)
























