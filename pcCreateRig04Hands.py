'''
Created on May 30, 2014
for Tin Girl Book and game project

@author: Eyal Assaf
'''
import maya.cmds as mc
# import tgpUtils as ut
from functools import partial
from tgpBaseUI import BaseUI as UI

import pcCreateRig00AUtilities

reload(pcCreateRig00AUtilities)
from pcCreateRig00AUtilities import pcCreateRigUtilities as CRU


class pcCreateRig04Hands(UI):
    def __init__(self):

        self.window = "bcWindow"
        self.title = "pcRigHands"
        self.winSize = (500, 350)

        self.createUI()

    def createCustom(self, *args):
        # selection type

        mc.rowColumnLayout(nc=2, cw=[(1, 500), (2, 500)], cs=[1, 5], rs=[1, 3])

        mc.text(l="Select The Palm Root: ")
        mc.text(l="")
        mc.separator(st="in", h=17, w=500)
        mc.setParent("..")
        mc.rowColumnLayout(nc=3, cw=[(1, 125), (2, 150), (3, 150)], cs=[1, 5], rs=[1, 3],
                           cal=([1, "left"], [2, "left"], [3, "left"],))

        mc.text(l="Mirror Arm As Well?")
        # mc.setParent("..")
        mc.radioButtonGrp("selArmMirrorType_rbg", la2=["No", "Yes"], nrb=2, sl=2, cw2=[50, 50], )
        mc.text(l="")
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
        mc.text(bgc=(0.85, 0.65, 0.25), l="Hand Joint: ")
        mc.textFieldButtonGrp("jointLoad_tfbg", cw=(1, 322), bl="  Load  ")

        mc.text(bgc=(0.85, 0.65, 0.25), l="Arm: ")
        mc.textFieldButtonGrp("armLoad_tfbg", cw=(1, 322), bl="  Load  ", tx="JNT_l_armEnd")

        mc.text(bgc=(0.85, 0.65, 0.25), l="FKIK Ctrl: ")
        mc.textFieldButtonGrp("ctrlFKIKSwitch_tfbg", cw=(1, 322), bl="  Load  ", tx="CTRL_fkikSwitch")

        mc.setParent("..")

        mc.separator(st="in", h=17, w=500)

        mc.rowColumnLayout(nc=2, cw=[(1, 100), (2, 370)], cs=[1, 5], rs=[1, 3])
        mc.checkBox("selGeo_cb", l="Affect Geometry", en=True, v=True)
        mc.setParent("..")

        # load buttons
        #
        mc.textFieldButtonGrp("jointLoad_tfbg", e=True, bc=self.loadSrc1Btn)
        mc.textFieldButtonGrp("armLoad_tfbg", e=True, bc=self.loadSrc2Btn)
        mc.textFieldButtonGrp("ctrlFKIKSwitch_tfbg", e=True, bc=self.loadSrc3Btn)

        self.selLoad = []
        self.jointArray = []
        mc.showWindow(self.window)

    def createButtonCmd(self, *args):
        self.tgpMakeBC()

    def loadSrc1Btn(self):
        self.jntHandSel = self.tgpLoadJntsBtn("jointLoad_tfbg", "joint", "Palm Joint", ["JNT", "palm"])
        self.selSrc1 = self.jntHandSel
        print(self.selSrc1)

    def loadSrc2Btn(self):
        self.selSrc2a, self.selSrc2b = self.tgpLoadJntsArmBtn("armLoad_tfbg", "joint", "Arm Joint", ["JNT", "Arm"])
        print(self.selSrc2a)
        print(self.selSrc2b)

    def loadSrc3Btn(self):
        self.selSrc3 = self.tgpLoadTxBtn("ctrlFKIKSwitch_tfbg", "nurbsCurve", "FK/IK Switch Control",
                                         ["CTRL", "fk", "ik", "Switch"], "control")
        print(self.selSrc3)

    def tgpLoadTxBtn(self, loadBtn, objectType, objectDesc, keywords, objectNickname=None):
        if objectNickname is None:
            objectNickname = objectType

        self.selLoad = []
        self.selLoad = mc.ls(sl=True, fl=True, type="transform")

        if (len(self.selLoad) != 1):
            mc.warning("Select only the {0}".format(objectDesc))
            return
        else:
            if CRU.checkObjectType(self.selLoad[0]) != objectType:
                mc.warning("{0} should be a {1}".format(objectDesc, objectNickname))
                return
            selName = self.selLoad[0]

            if not all(word.lower() in selName.lower() for word in keywords):
                mc.warning("That is the wrong {0}. Select the {1}".format(objectNickname, objectDesc))
                return
            mc.textFieldButtonGrp(loadBtn, e=True, tx=selName)
            return selName

    def tgpLoadJntsArmBtn(self, loadBtn, objectType, objectDesc, keywords, objectNickname=None):
        if objectNickname is None:
            objectNickname = objectType

        self.selLoad = []
        self.selLoad = mc.ls(sl=True, fl=True, type=objectType)

        if (len(self.selLoad) != 1):
            mc.warning("Select only the {0}".format(objectType))
            return
        else:
            selName = self.selLoad[0]
            exclusions = ["Twist", "_FK_", "_IK_"]

            if (not all(word.lower() in selName.lower() for word in keywords)) or any(
                            exclsn.lower() in selName.lower() for exclsn in exclusions):
                mc.warning("That is the wrong {0}. Select the {1}".format(objectNickname, objectDesc))
                return None, None
            print(exclusions)

            if any(exclsn.lower() in selName.lower() for exclsn in exclusions):
                mc.warning("That is the wrong {0} to delete. Select the {1}".format(objectNickname, objectDesc))
                return None, None

            # get the children joints
            self.parent = self.selLoad[0]
            self.child = mc.listRelatives(self.selLoad, ad=True, type=objectType)
            # collect the joints in an array
            self.jointArray = [self.parent]
            # reverse the order of the children joints
            if self.child:
                self.child.reverse()
                # add to the current list
                self.jointArray.extend(self.child)

            self.jointArmEndArray = [x for x in self.jointArray if "End" in x[-3:]]

            mc.textFieldButtonGrp(loadBtn, e=True, tx=self.jointArmEndArray[0])
            return self.jointArray, self.jointArmEndArray

    def tgpLoadJntsBtn(self, loadBtn, objectType, objectDesc, keywords, objectNickname=None):
        if objectNickname is None:
            objectNickname = objectType
        # hierarchy
        self.selLoad = []
        self.selLoad = mc.ls(sl=True, fl=True, type=objectType)

        if (len(self.selLoad) != 1):
            mc.warning("Select only the {0}".format(objectDesc))
            return
        else:

            selName = self.selLoad[0]

            if not all(word.lower() in selName.lower() for word in keywords):
                mc.warning("That is the wrong {0}. Select the {1}".format(objectNickname, objectDesc))
                return

            self.child = mc.listRelatives(self.selLoad, ad=True, type="joint")

            if self.child is None:
                mc.warning("You have the wrong joint selected")
                return

            mc.textFieldButtonGrp(loadBtn, e=True, tx=selName)

            # get the children joints
            self.parent = self.selLoad[0]
            # collect the joints in an array
            self.jointArrayHand = [self.parent]
            # reverse the order of the children joints, skip if not properly selected
            #
            self.child.reverse()

            # add to the current list
            self.jointArrayHand.extend(self.child)

            # removes if the last joint is End

        return self.jointArrayHand

    def tgpSetDriverArmFKIKSwitch(self, driver, driverAttr, driven, *args):
        w0w1Attr = mc.listAttr(driven)[-2:]
        CRU.setDriverDrivenValues(driver, driverAttr, driven, w0w1Attr[0], drivenValue=0, driverValue=1,
                                  modifyBoth="linear")
        CRU.setDriverDrivenValues(driver, driverAttr, driven, w0w1Attr[0], drivenValue=1, driverValue=0,
                                  modifyBoth="linear")
        CRU.setDriverDrivenValues(driver, driverAttr, driven, w0w1Attr[1], drivenValue=0, driverValue=0,
                                  modifyBoth="linear")
        CRU.setDriverDrivenValues(driver, driverAttr, driven, w0w1Attr[1], drivenValue=1, driverValue=1,
                                  modifyBoth="linear")

    def createPalmCtrls(self, jntPalmBase, leftRight, colourTU, jntPalm, isLeft, *args):

        # create the CTRL, then move it
        handOffsetCtrl = CRU.createCTRLs(jntPalmBase, 5, ornt=True, pnt=True, colour=colourTU, orientVal=(1, 0, 0))
        handLength = mc.getAttr("{0}.ty".format(jntPalm[1]))
        mc.select(handOffsetCtrl[1] + ".cv[:]")
        moveX = - handLength / 2
        mc.move(moveX, handLength * 0.5, 0, r=True, ls=True)

        # add the twist limits for the wrists:
        lowerTwistVal = "lowerArmTwist"
        upperTwistVal = "upperArmTwist"
        mc.addAttr(handOffsetCtrl[1], longName=lowerTwistVal, at="float", k=True, min=0, max=1, dv=1)
        mc.addAttr(handOffsetCtrl[1], longName=upperTwistVal, at="float", k=True, min=0, max=1, dv=1)

        # get the expression (this is a bit unique to me) then edit it
        armExprName = "expr" + leftRight + "armTwist"
        armExpr = mc.expression(armExprName, q=True, s=True)

        ctrlPalmName = "CTRL" + leftRight + "palm"
        armExpr = armExpr.replace("armEnd", "palm")
        armExpr = armExpr.replace("JNT" + leftRight + "palm", ctrlPalmName)
        editExpr = armExpr.splitlines()
        for i in range(len(editExpr)):
            if "lowerArm.rotate" in editExpr[i]:
                # if we're rotating the upper arm twists with the lower arm
                replaceTwistVal = upperTwistVal
            elif "palm.rotate" in editExpr[i]:
                # if we're rotating the lower arm twists with the palm
                replaceTwistVal = lowerTwistVal

            editExpr[i] = editExpr[i].replace(";", " * {0}.{1};\n".format(ctrlPalmName, replaceTwistVal))
            print(editExpr[i])

        armExprReplace = "".join(editExpr)
        print(armExprReplace)
        mc.delete(armExprName)

        mc.expression(s=armExprReplace, n=armExprName)

        # change the rotation order
        toRotateChange = [handOffsetCtrl[1], jntPalmBase]
        CRU.changeRotateOrder(toRotateChange, "YZX")

        return handOffsetCtrl

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
                fkFingerOffsetCtrls.append(
                    CRU.createCTRLs(temp, size=theSize, ornt=True, colour=colourTU, orientVal=(0, 1, 0)))
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
        for i in range(len(fkJntOffsetCtrls)):
            for j in range(len(fkJntOffsetCtrls[i]) - 1):
                mc.parent(fkJntOffsetCtrls[i][j + 1][0], fkJntOffsetCtrls[i][j][1])

        return fkJntOffsetCtrls

    def attachHandToArm(self, leftRight, fkColour, ikColour, handOffsetCtrl, jntArmEnd, ctrlFKIK, ctrlFKIKAttr, *args):
        # create locators, groups that contain said locators, then position them at the hand controls
        conFKName = "CON_FK{0}palm".format(leftRight)
        conLocFKOffsetCtrl = []
        conLocFKOffsetCtrl.append(mc.group(n="OFFSET_{0}".format(conFKName), em=True))
        conLocFKOffsetCtrl.append(mc.spaceLocator(p=(0, 0, 0), name=conFKName)[0])
        mc.parent(conLocFKOffsetCtrl[1], conLocFKOffsetCtrl[0])

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
        # setDriverDrivenValues(driver, driverAttribute, driven, drivenAttribute, driverValue, drivenValue, modifyInOut=None, modifyBoth=None)
        self.tgpSetDriverArmFKIKSwitch(ctrlFKIK, ctrlFKIKAttr, handOffsetCtrlParentConstraint)

        # at this point, the cleanup for CON_IK/FK_l_arms would take place in my notes, but why not just name it to begin with? So I did

        grpConPalm = mc.group(n="GRP_CON{0}palm".format(leftRight), w=True, em=True)
        mc.parent(conLocFKOffsetCtrl[0], conLocIKOffsetCtrl[0], grpConPalm)

        return grpConPalm, conLocFKOffsetCtrl, conLocIKOffsetCtrl

    def makeHand(self, leftRight, jntsHand, jntArmEnd, jntPalm, colourTU, fkColour, ikColour, ctrlFKIK, ctrlFKIKAttr,
                 isLeft, checkGeo, geoJntArray, *args):
        # Creating the Palm Control
        jntPalmBase = jntPalm[0]
        jntFingers, jntFingersUnsorted = self.getFingers(jntsHand)

        handOffsetCtrl = self.createPalmCtrls(jntPalmBase, leftRight, colourTU, jntPalm, isLeft)

        # Attaching the hand to the arm
        grpConPalm, conLocFKOffsetCtrl, conLocIKOffsetCtrl = self.attachHandToArm(leftRight, fkColour, ikColour,
                                                                                  handOffsetCtrl, jntArmEnd, ctrlFKIK,
                                                                                  ctrlFKIKAttr, )

        # Create the finger controls.
        # parent the finger offsets under the hands controls. We don't need to do so for the joints since we already assume it to be the case.
        fkFingerOffsetCtrls = self.createFingerFKs(jntFingers, colourTU, isLeft)
        for i in range(len(fkFingerOffsetCtrls)):
            mc.parent(fkFingerOffsetCtrls[i][0][0], handOffsetCtrl[1])
        # clean up the outliner
        self.handCleanUp(handOffsetCtrl, fkFingerOffsetCtrls, leftRight, jntPalmBase, jntPalm, jntFingersUnsorted,
                         grpConPalm, conLocFKOffsetCtrl, conLocIKOffsetCtrl)

        if checkGeo:
            CRU.tgpSetGeo(geoJntArray, setLayer=True)

    def handCleanUp(self, handOffsetCtrl, fkFingerOffsetCtrls, leftRight, jntPalmBase, jntPalm, jntFingersUnsorted,
                    grpConPalm, conLocFKOffsetCtrl, conLocIKOffsetCtrl, *args):

        grpRigArm = mc.group(n="GRP_rig{0}arm".format(leftRight), w=True, em=True)
        # For the sake of not having a bazillion entries for the input text, I'm hardcoding things here
        mc.parent("GRP_CTRL_IK{0}arm".format(leftRight), "GRP_jnt{0}arm".format(leftRight),
                  "OFFSET_CTRL{0}shoulder".format(leftRight), jntPalmBase, handOffsetCtrl[0], grpConPalm, grpRigArm)
        CRU.lockHideCtrls(handOffsetCtrl[1], translate=True, scale=True, visible=True)
        for i in range(len(fkFingerOffsetCtrls)):
            for j in range(len(fkFingerOffsetCtrls[i])):
                CRU.lockHideCtrls(fkFingerOffsetCtrls[i][j][1], scale=True, translate=True, visible=True)

        mc.setAttr("{0}.visibility".format(conLocFKOffsetCtrl[1]), False)
        mc.setAttr("{0}.visibility".format(conLocIKOffsetCtrl[1]), False)

        CRU.layerEdit(jntPalm, bndLayer=True, noRecurse=True)
        CRU.layerEdit(jntFingersUnsorted, bndLayer=True, noRecurse=True)

    def getPalm(self, jntsHand, *args):
        return ([x for x in jntsHand if "palm" in x])

    def getFingers(self, jntsHand, *args):
        allFingers = []
        allFingersUnsorted = [x for x in jntsHand if "palm" not in x]

        indexOfFingers = ["index", "middle", "ring", "pinky", "thumb"]

        for finger in indexOfFingers:
            allFingers.append([x for x in allFingersUnsorted if finger in x])

        return allFingers, allFingersUnsorted

    def tgpMakeBC(self, *args):

        checkSelLeft = mc.radioButtonGrp("selArmType_rbg", q=True, select=True)

        mirrorSel = mc.radioButtonGrp("selArmMirrorType_rbg", q=True, select=True)

        checkGeo = mc.checkBox("selGeo_cb", q=True, v=True)
        ctrlFKIK = mc.textFieldButtonGrp("ctrlFKIKSwitch_tfbg", q=True, text=True)

        self.jntNames = mc.textFieldButtonGrp("jointLoad_tfbg", q=True, text=True)

        try:
            jntHandRoot = self.jointArrayHand[0]
        except:
            mc.warning("No joint selected!")
            return

        try:
            jntArmEnd = mc.textFieldButtonGrp("armLoad_tfbg", q=True, text=True)
        except:
            mc.warning("No joint selected!")
            return

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
            # CRU.createLocatorToDelete()

            # get the fingers and palm
            jntsHand = self.jntHandSel

            if not (CRU.checkLeftRight(isLeft, jntHandRoot)):
                # if the values are not lined up properly, break out
                mc.warning("You are selecting the incorrect side for the hand")
                return

            if not (CRU.checkLeftRight(isLeft, jntArmEnd)):
                # if the values are not lined up properly, break out
                mc.warning("You are selecting the incorrect side for the arm")
                return
            # gets the hand joints
            geoJntArray = [x for x in jntsHand if "End" not in x[-3:]]

            # create the palm controls
            jntPalm = self.getPalm(jntsHand)
            jntPalmBase = jntPalm[0]

            if mirrorRig:
                print("Mirroring")

                # create a mirror rig for the hand
                geoJntArrayMirror = geoJntArray[:]
                for i in range(len(geoJntArrayMirror)):
                    geoJntArrayMirror[i] = geoJntArrayMirror[i].replace(leftRight, leftRightMirror)

                mc.mirrorJoint(jntPalmBase, mirrorYZ=True, mirrorBehavior=True,
                               searchReplace=[leftRight, leftRightMirror])
                # adds the joints that interact with geometry
                jntsHandMirror = []
                for i in range(len(jntsHand)):
                    jntsHandMirror.append(jntsHand[i].replace(leftRight, leftRightMirror))

                jntPalmMirror = self.getPalm(jntsHandMirror)

                jntArmEndMirror = jntArmEnd.replace(leftRight, leftRightMirror)
                isLeftMirror = not isLeft

            # makeHand(self, leftRight, jntsHand, jntPalm, colourTU, fkColour, ikColour, ctrlFKIK, ctrlFKIKAttr, *args):
            self.makeHand(leftRight, jntsHand, jntArmEnd, jntPalm, colourTU, fkColour, ikColour, ctrlFKIK, ctrlFKIKAttr,
                          isLeft, checkGeo, geoJntArray)

            if mirrorRig:
                self.makeHand(leftRightMirror, jntsHandMirror, jntArmEndMirror, jntPalmMirror, colourTUMirror,
                              fkColourMirror, ikColourMirror, ctrlFKIK, ctrlFKIKAttrMirror, isLeftMirror, checkGeo,
                              geoJntArrayMirror)
