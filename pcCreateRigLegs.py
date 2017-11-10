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


class pcCreateRigLegs(UI):
    def __init__(self):

        self.window = "bcWindow"
        self.title = "pcRigLegs"
        self.winSize = (500, 325)

        self.createUI()

    def createCustom(self, *args):
        # selection type
        mc.rowColumnLayout(nc=3, cw=[(1, 125), (2, 150), (3, 150)], cs=[1, 5], rs=[1, 3],
                           cal=([1, "left"], [2, "left"], [3, "left"],))

        mc.text(l="Mirror Leg As Well?")
        # mc.setParent("..")
        mc.radioButtonGrp("selLegMirrorType_rbg", la2=["No", "Yes"], nrb=2, sl=2, cw2=[50, 50], )
        mc.text(l="")
        mc.checkBox("selCreateTwists_cb", l="Create Twists", en=True, v=True)
        mc.checkBox("selSpineEnd_cb", l="Connect To Hip", en=True, v=True)
        mc.setParent("..")
        mc.separator(st="in", h=20, w=500)

        mc.rowColumnLayout(nc=3, cw=[(1, 100), (2, 200), (3, 150)], cs=[1, 5], rs=[1, 3],
                           cal=([1, "left"], [2, "left"], [3, "left"],))
        mc.text(l="Initial Limb: ")
        mc.radioButtonGrp("selLegType_rbg", la2=["Left", "Right"], nrb=2, sl=1, cw2=[50, 50], )
        mc.setParent("..")
        mc.separator(st="in", h=20, w=500)

        # sources
        mc.rowColumnLayout(nc=2, cw=[(1, 100), (2, 370)], cs=[1, 5], rs=[1, 3])
        mc.text(bgc=(0.85, 0.65, 0.25), l="Leg: ")
        mc.textFieldButtonGrp("jointLoad_tfbg", cw=(1, 322), bl="  Load  ")

        mc.text(bgc=(0.85, 0.65, 0.25), l="FKIK Ctrl: ")
        mc.textFieldButtonGrp("ctrlLoad_tfbg", cw=(1, 322), bl="  Load  ", tx="CTRL_fkikSwitch")

        mc.text(bgc=(0.85, 0.65, 0.25), l="FK Hip CTRL: ")
        mc.textFieldButtonGrp("ctrlFKHipLoad_tf", cw=(1, 322), bl="  Load  ", tx="CTRL_FK_hip")

        mc.setParent("..")

        mc.separator(st="in", h=20, w=500)

        mc.rowColumnLayout(nc=2, cw=[(1, 100), (2, 370)], cs=[1, 5], rs=[1, 3])
        mc.checkBox("selGeo_cb", l="Affect Geometry", en=True, v=True)
        mc.setParent("..")

        mc.separator(st="in", h=20, w=500)

        # load buttons
        #

        mc.textFieldButtonGrp("jointLoad_tfbg", e=True, bc=self.loadSrc1Btn)
        mc.textFieldButtonGrp("ctrlFKHipLoad_tf", e=True, bc=self.loadSrc2Btn)
        mc.textFieldButtonGrp("ctrlLoad_tfbg", e=True, bc=self.loadSrc3Btn)

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
        self.jntSel = self.tgpLoadTxBtn("jointLoad_tfbg", "joint")
        print(self.jntSel)

    def loadSrc2Btn(self):
        self.ctrlSel = self.loadCtrlBtn("ctrlFKHipLoad_tf")
        print(self.ctrlSel)

    def loadSrc3Btn(self):
        self.grpSel = self.loadCtrlBtn("ctrlLoad_tfbg")
        print(self.ctrlSel)

    def loadCtrlBtn(self, loadBtn):
        self.selLoad = []
        # self.selLoad = mc.ls(sl=True, fl=True, type="nurbsCurve")
        self.selLoad = mc.ls(sl=True, fl=True, type="transform")

        if (len(self.selLoad) != 1):
            mc.warning("Select only the Control")
            return
        else:

            if CRU.checkObjectType(self.selLoad[0]) != "nurbsCurve":
                mc.warning("The Control should be a nurbsCurve")
                return
            selName = self.selLoad[0]
            mc.textFieldButtonGrp(loadBtn, e=True, tx=selName)
            print(selName)
            return selName

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
            self.jointArray = [self.parent]
            # reverse the order of the children joints
            self.child.reverse()

            # add to the current list
            self.jointArray.extend(self.child)

            # removes if the last joint is End
            # checks if the last three letters are "End"
            self.jointEndArray = [x for x in self.jointArray if "End" in x[-3:]]
            self.jntLegArray = [x for x in self.jointArray if "Leg" in x[-3:]]
            self.jointRoot = self.selLoad[0]

        return self.jointArray

    def makeTwists(self, numTwists, leftRight, jntLegArray, geoJntArray, footOffsetCtrl, *args):
        # colourTU and isLeft is for a special part of the code which lets us create a foot control
        numTwistsPlus1 = numTwists + 1
        twists = numTwists
        twistJnts = []
        twistExpression = ""

        for i in range(len(jntLegArray)):
            twistJntsSubgroup = []
            val = str(jntLegArray[i])
            # we want to affect the ankle twist
            if i == 0:
                nextJnt = mc.listRelatives(val, c=True, type="joint")[0]
                nextJntVal = nextJnt
            else:
                # print("I AM THE FISH!!")
                nextJnts = mc.listRelatives(val, c=True, type="joint", ad=True)
                nextJnt = nextJnts[-2]
                nextJntVal = nextJnts[-1]
                print("=-=-=-=-=-=")
                print(nextJnts)
                print(nextJnt)
                print("=+=+=+=+=+=")
                # with the ankle, we can create the control

            nextJntYVal = mc.getAttr("{0}.ty".format(nextJntVal))
            nextJntIncrement = nextJntYVal / (numTwistsPlus1)
            twistJnt = mc.duplicate(val, po=True, n="ToDelete")

            # create the joint twists at the proper location

            # upper leg is positive, lower leg is negative
            '''JNT_l_upperLegTwist1.rotateY = JNT_l_lowerLeg.rotateY * .25;
            JNT_l_upperLegTwist2.rotateY = JNT_l_lowerLeg.rotateY * .5;
            JNT_l_upperLegTwist3.rotateY = JNT_l_lowerLeg.rotateY * .75;

            JNT_l_lowerLegTwist1.rotateY = JNT_l_ankleTwist.rotateY * .25 * -1;
            JNT_l_lowerLegTwist2.rotateY = JNT_l_ankleTwist.rotateY * .5 * -1;
            JNT_l_lowerLegTwist3.rotateY = JNT_l_ankleTwist.rotateY * .75 * -1;'''
            for x in range(twists):

                valx = x + 1
                twistTempName = "{0}Twist{1}".format(val, valx)

                twistTemp = mc.duplicate(twistJnt, n=twistTempName)

                mc.parent(twistTemp, jntLegArray[i])
                mc.setAttr("{0}.ty".format(twistTempName), nextJntIncrement * valx)
                twistJntsSubgroup.append(twistTemp[0])

                if i == 0:
                    twistInverse = 1.0 / (numTwistsPlus1)
                else:
                    twistInverse = -1.0 / (numTwistsPlus1)

                if "upper" in nextJnt:
                    legType = self.upperTwistVal
                elif "lower" in nextJnt:
                    legType = self.lowerTwistVal

                twistExpression += "{0}.rotateY = {1}.rotateY * {2}*{3}.{4};\n".format(twistTempName, nextJnt,
                                                                                       valx * twistInverse,
                                                                                       footOffsetCtrl[1], legType)
                geoJntArray.append(twistTempName)

            mc.delete(twistJnt)

            twistJnts.append(twistJntsSubgroup)

            twistExpression += "\n"

            # change to account for the limb
        xprNameTwist = "expr_" + leftRight + "legTwist"  # changes to account for the left or right

        mc.expression(s=twistExpression, n=xprNameTwist)
        return xprNameTwist, twistExpression, geoJntArray

    def tgpCreateLimbFKIFList(self, jntsTemp, textToReplace="", textReplacement="", stripLastVal=0, deleteThis=True,
                              renameThis=True, addToEnd="", *args):
        jntsReturn = []
        # creates a set of values. Normally, we want this deleted, but we can also create a list from the values that simply don't include problematic node
        stripLastVal1 = stripLastVal * (-1)
        for i in range(len(jntsTemp)):
            toTest = jntsTemp[i]
            if mc.objectType(toTest) == "joint":
                if "Twist" in toTest and "ankleTwist" not in toTest:
                    if deleteThis:
                        mc.delete(toTest)
                else:
                    if stripLastVal1 == 0:
                        temp = toTest
                    else:
                        temp = toTest[:stripLastVal1]
                    toRename = temp.replace(textToReplace, textReplacement) + addToEnd  # strip off the last character
                    if renameThis:
                        mc.rename(toTest, toRename)
                    jntsReturn.append(toRename)
            else:
                if deleteThis:
                    mc.delete(toTest)
        return jntsReturn

    def tgpSetDriverLegFKIKSwitch(self, driver, driverAttr, driven, *args):
        w0w1Attr = mc.listAttr(driven)[-2:]
        CRU.setDriverDrivenValues(driver, driverAttr, driven, w0w1Attr[0], drivenValue=0, driverValue=1,
                                  modifyBoth="linear")
        CRU.setDriverDrivenValues(driver, driverAttr, driven, w0w1Attr[0], drivenValue=1, driverValue=0,
                                  modifyBoth="linear")
        CRU.setDriverDrivenValues(driver, driverAttr, driven, w0w1Attr[1], drivenValue=0, driverValue=0,
                                  modifyBoth="linear")
        CRU.setDriverDrivenValues(driver, driverAttr, driven, w0w1Attr[1], drivenValue=1, driverValue=1,
                                  modifyBoth="linear")

    def attachLegToHip(self, fkJnts, ikJnts, bndJnts, ctrlFKIK, ctrlFKIKAttr, ikJntsDrive, fkJntOffsetCtrls, leftRight,
                       *args):
        # Constraining the bind joints to the fk and ik
        bndPntConstraint = mc.pointConstraint(fkJnts[0], ikJnts[0], bndJnts[0])[0]
        self.tgpSetDriverLegFKIKSwitch(ctrlFKIK, ctrlFKIKAttr, bndPntConstraint)

        # Constraining the ik joints to the ik drive
        ikPntConstraint = mc.pointConstraint(ikJntsDrive[0], ikJnts[0])[0]

        # creating the hip attachment and attaching the IK and IKdrive
        hipIKOffsetCtrl = self.createHip(leftRight, ikJnts, ikJntsDrive)

        # Constraining the upperLeg FK control to the upperLeg JNT
        print("{0} constraining {1}".format(fkJntOffsetCtrls[0][1], bndJnts[0]))
        mc.pointConstraint(fkJntOffsetCtrls[0][1], fkJnts[0])

        return hipIKOffsetCtrl

    def addFootCtrl(self, geoJntArray, isLeft, leftRight, colourTU, *args):

        ankleTwist = [x for x in geoJntArray if "ankleTwist" in x][0]

        self.lowerTwistVal = "lowerLegTwist"
        self.upperTwistVal = "upperLegTwist"

        # creates the control next to ankleTwist
        footCtrlsOffsetCtrl = CRU.createNail(ankleTwist, isLeft, leftRight + "footCtrls", bodySize=12, headSize=2,
                                             colour=colourTU)
        mc.addAttr(footCtrlsOffsetCtrl[1], longName=self.lowerTwistVal, at="float", k=True, min=0, max=1, dv=1)
        mc.addAttr(footCtrlsOffsetCtrl[1], longName=self.upperTwistVal, at="float", k=True, min=0, max=1, dv=1)

        return footCtrlsOffsetCtrl

    def addIKFKCreateFKCtrl(self, jntLegArray, colourTU, isLeft, *args):
        bndJnts, fkJnts, ikJnts = self.getBndFkIkJnts(jntLegArray)

        fkLen = len(fkJnts)
        ikLen = len(ikJnts)
        bndLen = len(bndJnts)

        if bndLen != fkLen or bndLen != ikLen:
            mc.warning("Your leg joints are somehow not equal")
            return
        else:
            ikFkJntConstraints = []
            # we want to constrain upperLeg, lowerLeg, ankleTwist, ball
            specVals = [0, 1, -4, -2]
            for sv in specVals:
                temp = mc.orientConstraint(fkJnts[sv], ikJnts[sv], bndJnts[sv])[0]
                ikFkJntConstraints.append(temp)

        fkJntsToUse = [fkJnts[0], fkJnts[1], fkJnts[-4], fkJnts[-2]]

        # we want to create FK controls for the limbs except the end
        sizeVals = [12.5, 12.5, 11, 7.5]
        fkJntOffsetCtrls = self.createLegFKs(fkJntsToUse, colourTU, isLeft, sizeVals)

        return bndJnts, fkJnts, ikJnts, ikFkJntConstraints, fkJntOffsetCtrls

    def createIKCtrlsAndDrive(self, ikJnts, leftRight, colourTU, *args):
        # create the IKs
        # we make the JNT IK Drive earlier than in the notes
        ikJntsDrive = self.createLegIKDrive(ikJnts)

        ikJntsToUse = [ikJnts[0], ikJnts[2]]
        ikJntsDriveToUse = [ikJntsDrive[0], ikJntsDrive[2]]
        # The first is a Rotate Plane solver, the rest are Single Chain solvers
        # createLegOrFootIK(self, ikJntsToUse, ikJntsDriveToUse, leftRight, colourTU, ikSuffix, createCtrl):
        ikLegs, ikLegSide, ikOffsetCtrl = self.createLegOrFootIK(ikJntsToUse, ikJntsDriveToUse, leftRight, colourTU,
                                                                 "leg",
                                                                 True, "ikRPsolver")

        ikJntsToUse = [ikJnts[-4], ikJnts[-2]]
        ikJntsDriveToUse = [ikJntsDrive[-4], ikJntsDrive[-2]]
        ikBall, ikBallSide = self.createLegOrFootIK(ikJntsToUse, ikJntsDriveToUse, leftRight, colourTU, "ball", False,
                                                    "ikSCsolver")

        ikJntsToUse = [ikJnts[-2], ikJnts[-1]]
        ikJntsDriveToUse = [ikJntsDrive[-2], ikJntsDrive[-1]]
        ikToe, ikToeSide = self.createLegOrFootIK(ikJntsToUse, ikJntsDriveToUse, leftRight, colourTU, "toe", False,
                                                  "ikSCsolver")

        mc.parent(ikLegs[0], ikBall[0], ikToe[0], ikOffsetCtrl[1])
        # [0, 1, -4, -2]

        return ikJntsDrive, ikOffsetCtrl, ikLegs

    def orientConstrainThenRotateOrder(self, ikJnts, ikJntsDrive, bndJnts, fkJnts, fkJntOffsetCtrls, *args):
        listVals = [0, 1, -4, -2]
        skipYVals = [1]
        self.orientConstrainSkipY(ikJnts, ikJntsDrive, listVals, skipYVals)

        # change the rotation order
        rotationChange = [bndJnts[1], fkJnts[1], ikJnts[1], ikJntsDrive[1], fkJntOffsetCtrls[1][1]]

        CRU.changeRotateOrder(rotationChange, "YZX")

    def createHip(self, leftRight, ikJnts, ikJntsDrive, *args):
        # create a locator
        hipName = "CTRL_IK_" + leftRight + "hip"
        hipIKOffsetCtrl = []
        hipIKOffsetCtrl.append(mc.group(n="OFFSET_" + hipName, w=True, em=True))
        hipIKOffsetCtrl.append(mc.spaceLocator(p=(0, 0, 0), name=hipName)[0])
        hipIKOffsetCtrl.append(mc.group(n="AUTO_" + hipName, w=True, em=True))
        setSize = 20
        mc.setAttr("{0}.localScaleX".format(hipIKOffsetCtrl[1]), setSize)
        mc.setAttr("{0}.localScaleY".format(hipIKOffsetCtrl[1]), setSize)
        mc.setAttr("{0}.localScaleZ".format(hipIKOffsetCtrl[1]), setSize)

        mc.parent(hipIKOffsetCtrl[2], hipIKOffsetCtrl[0])
        mc.parent(hipIKOffsetCtrl[1], hipIKOffsetCtrl[2])
        # position and orient the offset
        toDelete = mc.parentConstraint(ikJnts[0], hipIKOffsetCtrl[0])
        mc.delete(toDelete)
        # hip control point constrains the ikDrive joint
        mc.pointConstraint(hipIKOffsetCtrl[1], ikJntsDrive[0])
        mc.setAttr("{0}.visibility".format(hipIKOffsetCtrl[1]), False)
        # we parent the hip locators in our clean up

        return hipIKOffsetCtrl

    def getBndFkIkJnts(self, jntLegArray, *args):
        bndJntsTemp = mc.listRelatives(jntLegArray[0], type="joint", ad=True)
        bndJnts = self.tgpCreateLimbFKIFList(bndJntsTemp, deleteThis=False, renameThis=False)
        bndJnts.append(jntLegArray[0])
        bndJnts.reverse()

        ikJntsTemp = mc.duplicate(jntLegArray[0], rc=True)
        ikJntRoot = ikJntsTemp[0]

        # We already made unique
        ikJntsTempDesc = mc.listRelatives(ikJntRoot, ad=True)
        ikJntsTempDesc.append(ikJntRoot)

        # remove non-IK related joints
        ikJnts = self.tgpCreateLimbFKIFList(ikJntsTempDesc, "JNT_", "JNT_IK_", 1)

        ikJnts.reverse()

        # create the FK Joints

        fkJntsTemp = mc.duplicate(ikJnts[0], rc=True)

        fkJnts = self.tgpCreateLimbFKIFList(fkJntsTemp, "JNT_IK_", "JNT_FK_", 1)

        return bndJnts, fkJnts, ikJnts

    def setupIkKneeLegTwist(self, ikOffsetCtrl, ikJnts, ikLegs, isLeft, *args):
        kneeTwistAttr = "kneeTwist"
        mc.addAttr(ikOffsetCtrl[1], longName=kneeTwistAttr, at="float", k=True)

        mc.connectAttr("{0}.{1}".format(ikOffsetCtrl[1], kneeTwistAttr), ikJnts[1] + ".rotateY")
        # We don't work with the leg twist yet

        legTwistAttr = "legTwist"
        mc.addAttr(ikOffsetCtrl[1], longName=legTwistAttr, at="float", k=True)

        # Finishing the Leg, Leg IK Twist
        # we are connecting the leg twist in the IK. We want the leg twist to aim inward in negative.
        ikCtrlLegTwistNode = "{0}_LegTwist_MD".format(ikOffsetCtrl[1])
        mc.shadingNode("multiplyDivide", n=ikCtrlLegTwistNode, au=True)
        # We want the
        if isLeft:
            mult = -1
        else:
            mult = 1
        mc.setAttr("{0}.operation".format(ikCtrlLegTwistNode), 2)
        mc.setAttr("{0}.i2x".format(ikCtrlLegTwistNode), mult)
        mc.connectAttr("{0}.{1}".format(ikOffsetCtrl[1], "legTwist"), ikCtrlLegTwistNode + ".i1x")

        mc.connectAttr("{0}.ox".format(ikCtrlLegTwistNode), ikLegs[0] + ".twist")

    def createLegFKs(self, fkJnts, colourTU, isLeft, sizeVals=None, *args):
        # we want to create FK controls for the limbs except the end
        if sizeVals == None:
            sizeToUse = 10
        fkJntOffsetCtrls = []
        for i in range(len(fkJnts)):
            temp = fkJnts[i]
            try:
                sizeToUse = sizeVals[i]
            except:
                sizeToUse = 10
            # createCTRLs(self, s, size=3, prnt=False, ornt=False, pnt=False, orientVal=(1, 0, 0), colour=5, sections=None):
            fkJntOffsetCtrls.append(
                CRU.createCTRLs(temp, size=sizeToUse, ornt=True, colour=colourTU, orientVal=(0, 1, 0)))
            # checks if the object is the ball or the lowerleg. The ball because it has no value in front of it in the fkJnts, and lowerleg because the value in front of it in fkJnts
            checkers = ["ball", "lower", "ankle"]
            # checks if ball or lower leg
            if any(checker in fkJnts[i] for checker in checkers[:-1]):
                legLength = mc.getAttr("{0}.ty".format(mc.listRelatives(fkJnts[i], c=True, typ="joint")[0]))
            else:
                legLength = mc.getAttr("{0}.ty".format(fkJnts[i + 1]))
            # check if the lowerleg or ankle

            # only change the thigh location
            if not any(checker in fkJnts[i] for checker in checkers):
                mc.select(fkJntOffsetCtrls[i][1] + ".cv[:]")
                mc.move(0, legLength * 0.5, 0, r=True, ls=True)

            # if the ball, modify to prettify
            if checkers[0] in fkJnts[i]:
                if isLeft:
                    mc.select(fkJntOffsetCtrls[i][1] + ".cv[4:6]")
                    # mc.move(0, 0, -sizeToUse, r=True, ls=True)
                else:
                    mc.select(fkJntOffsetCtrls[i][1] + ".cv[0:2]")
                # scale to the center
                mc.scale(1, 1, 0, p=(0, 0, 0))

                mc.move(0, 0, legLength * 0.15, r=True, ls=True)

        # parent the fk lower leg controls under the fk upper leg controls
        for i in range(len(fkJntOffsetCtrls[:-1])):
            mc.parent(fkJntOffsetCtrls[i + 1][0], fkJntOffsetCtrls[i][1])

        return fkJntOffsetCtrls

    def createLegIKDrive(self, ikJnts, *args):

        ikJntsTDriveTemp = mc.duplicate(ikJnts[0], rc=True)
        ikJntsDrive = self.tgpCreateLimbFKIFList(ikJntsTDriveTemp, addToEnd="Drive", stripLastVal=1)

        return ikJntsDrive

    def createLegOrFootIK(self, ikJntsToUse, ikJntsDriveToUse, leftRight, colourTU, ikSuffix, createCtrl, ikSolver,
                          *args):
        ikSide = leftRight + ikSuffix

        ikLegName = "IK_" + ikSide
        effLegName = "EFF_" + ikSide
        ikLegs = mc.ikHandle(n=ikLegName, sj=ikJntsDriveToUse[0], ee=ikJntsDriveToUse[-1], sol=ikSolver)
        mc.rename(ikLegs[1], effLegName)

        # fkJntOffsetCtrls.append(self.createCTRLs(temp, size=9, ornt=True, colour=colourTU, orientVal=(0, 1, 0)))
        ikOffsetCtrl = None
        if createCtrl:
            # We just want to create a control at the location, we'll be parenting it.
            ikOffsetCtrl = CRU.createCTRLs(ikLegs[0], 9, pnt=False, ornt=False, prnt=False, colour=colourTU,
                                           addPrefix=True, orientVal=(0, 1, 0), boxDimensionsLWH=[6, 6, 6])
            return ikLegs, ikSide, ikOffsetCtrl

        return ikLegs, ikSide

    def orientConstrainSkipY(self, ikJnts, ikJntsDrive, listVals, skipYVals, *args):
        for i in listVals:
            if i in skipYVals:
                mc.orientConstraint(ikJntsDrive[i], ikJnts[i], skip="y")
            else:
                mc.orientConstraint(ikJntsDrive[i], ikJnts[i])

    def legCleanUp(self, fkJnts, ikJnts, ikJntsDrive, bndJnts,
                   ikOffsetCtrl, fkJntOffsetCtrls, hipIKOffsetCtrl, ctrlFKHip,
                   leftRight, ctrlFKIK, ctrlFKIKAttr, checkboxHip, footCtrlsOffsetCtrl, *args):

        # group the root leg joints and the IK control
        grpLegRigName = "GRP_rig_" + leftRight + "leg"
        grpLegJntName = "GRP_JNT_" + leftRight + "leg"

        grpLegRig = mc.group(n=grpLegRigName, w=True, em=True)
        grpLegJnt = mc.group(n=grpLegJntName, w=True, em=True)

        mc.parent(fkJnts[0], ikJnts[0], ikJntsDrive[0], bndJnts[0], grpLegJnt)
        mc.parent(grpLegJnt, ikOffsetCtrl[0], footCtrlsOffsetCtrl[0], grpLegRig)

        # attach objects to the hip
        if checkboxHip:
            # mc.parentConstrain(shoulderOffsetCtrl[0], JNT_IK_spine_6,  mo=True)
            # print(fkJntOffsetCtrls[0][1])
            mc.parent(fkJntOffsetCtrls[0][0], hipIKOffsetCtrl[0], ctrlFKHip)

        # Hiding the visibility of the joints
        mc.setAttr("{0}.visibility".format(ikJnts[0]), False)
        mc.setAttr("{0}.visibility".format(ikJntsDrive[0]), False)
        mc.setAttr("{0}.visibility".format(fkJnts[0]), False)
        mc.setAttr("{0}.visibility".format(hipIKOffsetCtrl[1]), False)

        # locking and hiding the IK controls
        CRU.lockHideCtrls(ikOffsetCtrl[1], rotate=True, scale=True, visible=True)
        for fkOC in fkJntOffsetCtrls:
            CRU.lockHideCtrls(fkOC[1], translate=True, scale=True, visible=True)

        # my custom control shouldn't be moved by the animator
        CRU.lockHideCtrls(footCtrlsOffsetCtrl[1], translate=True, rotate=True, scale=True, visible=True)

        # locking and hiding the CTRL_IK_l_hip
        CRU.lockHideCtrls(hipIKOffsetCtrl[1], scale=True, visible=True)

        # set the FK to visible when not ctrlFKIK not 1 for leg attribute

        tangentToUse = ["linear", "step"]
        visMin = 0.001

        CRU.setDriverDrivenValues(ctrlFKIK, ctrlFKIKAttr, fkJntOffsetCtrls[0][1], "visibility", drivenValue=True,
                                  driverValue=0, modifyInOut=tangentToUse)
        CRU.setDriverDrivenValues(ctrlFKIK, ctrlFKIKAttr, fkJntOffsetCtrls[0][1], "visibility", drivenValue=True,
                                  driverValue=1 - visMin, modifyInOut=tangentToUse)
        CRU.setDriverDrivenValues(ctrlFKIK, ctrlFKIKAttr, fkJntOffsetCtrls[0][1], "visibility", drivenValue=False,
                                  driverValue=1, modifyInOut=tangentToUse)

        tangentToUse = ["linear", "step"]
        # set the IK to visible when not ctrlFKIK not 0 for leg attribute
        CRU.setDriverDrivenValues(ctrlFKIK, ctrlFKIKAttr, ikOffsetCtrl[1], "visibility", drivenValue=False,
                                  driverValue=0, modifyInOut=tangentToUse)
        CRU.setDriverDrivenValues(ctrlFKIK, ctrlFKIKAttr, ikOffsetCtrl[1], "visibility", drivenValue=True,
                                  driverValue=visMin, modifyInOut=tangentToUse)
        CRU.setDriverDrivenValues(ctrlFKIK, ctrlFKIKAttr, ikOffsetCtrl[1], "visibility", drivenValue=True,
                                  driverValue=1, modifyInOut=tangentToUse)

        CRU.layerEdit(fkJnts, fkLayer=True, layerVis=False, noRecurse=True)
        CRU.layerEdit(ikJnts, ikLayer=True, layerVis=False, noRecurse=True)
        CRU.layerEdit(ikJntsDrive, ikdriveLayer=True, layerVis=False, noRecurse=True)

    def makeLeg(self, isLeft, leftRight,
                jntLegArray,
                checkGeo, geoJntArray, colourTU, jntLegRoot,
                ctrlFKIK, ctrlFKIKAttr, ctrlFKHip, checkboxTwists,
                checkboxHip, *args):

        # create a special control for my own preferences
        footCtrlsOffsetCtrl = self.addFootCtrl(geoJntArray, isLeft, leftRight, colourTU)

        # Create the joint twists
        # Adding the twist joint (does this at the same time)
        # Twist Joints and low-res Mesh
        if checkboxTwists:
            xprNameTwist, twistExpression, geoJntArray = self.makeTwists(3, leftRight, jntLegArray, geoJntArray,
                                                                         footCtrlsOffsetCtrl)

        # for testing purposes only, setting the IK to active:
        mc.setAttr("{0}.{1}".format(ctrlFKIK, ctrlFKIKAttr), 0.5)

        # Adding the IK and FK and creating the FK Controls
        bndJnts, fkJnts, ikJnts, ikFkJntConstraints, fkJntOffsetCtrls = self.addIKFKCreateFKCtrl(jntLegArray, colourTU,
                                                                                                 isLeft)

        # IK Leg Control Part 1
        ikJntsDrive, ikOffsetCtrl, ikLegs = self.createIKCtrlsAndDrive(ikJnts, leftRight, colourTU)

        # IK Leg Control Part 2
        self.orientConstrainThenRotateOrder(ikJnts, ikJntsDrive, bndJnts, fkJnts, fkJntOffsetCtrls)

        # FK IK Switching
        # Adding the IK and FK and creating the FK Controls
        for i in range(len(ikFkJntConstraints)):
            self.tgpSetDriverLegFKIKSwitch(ctrlFKIK, ctrlFKIKAttr, ikFkJntConstraints[i])

        # Attaching the Leg to the Hip
        hipIKOffsetCtrl = self.attachLegToHip(fkJnts, ikJnts, bndJnts, ctrlFKIK, ctrlFKIKAttr, ikJntsDrive,
                                              fkJntOffsetCtrls, leftRight)

        # create the ik twist
        self.setupIkKneeLegTwist(ikOffsetCtrl, ikJnts, ikLegs, isLeft)

        # Organize the rig
        self.legCleanUp(fkJnts, ikJnts, ikJntsDrive, bndJnts,
                        ikOffsetCtrl, fkJntOffsetCtrls, hipIKOffsetCtrl, ctrlFKHip,
                        leftRight, ctrlFKIK, ctrlFKIKAttr, checkboxHip, footCtrlsOffsetCtrl)

        if checkGeo:
            CRU.tgpSetGeo(geoJntArray)

    def tgpMakeBC(self, *args):

        checkSelLeft = mc.radioButtonGrp("selLegType_rbg", q=True, select=True)
        mirrorSel = mc.radioButtonGrp("selLegMirrorType_rbg", q=True, select=True)

        checkboxTwists = mc.checkBox("selCreateTwists_cb", q=True, v=True)

        checkGeo = mc.checkBox("selGeo_cb", q=True, v=True)

        self.jntNames = mc.textFieldButtonGrp("jointLoad_tfbg", q=True, text=True)
        ctrlFKIK = mc.textFieldButtonGrp("ctrlLoad_tfbg", q=True, text=True)

        geoJntArray = self.jointArray
        checkboxHip = mc.checkBox("selSpineEnd_cb", q=True, v=True)

        if checkboxHip:
            ctrlFKHip = mc.textFieldButtonGrp("ctrlFKHipLoad_tf", q=True, text=True)
        else:
            ctrlFKHip = None

        # print(ctrlFKHip)

        try:
            jntLegRoot = self.jointArray[0]
        except:
            mc.warning("No joint selected!")
            return

        # print(mirrorSel)
        if mirrorSel == 1:
            mirrorRig = False
        else:
            mirrorRig = True

        listCtrlFKIKAttr = ["l_leg", "r_leg", "l_leg", "r_leg"]
        if checkSelLeft == 1:
            isLeft = True
            leftRight = "l_"
            leftRightMirror = "r_"
            colourTU = 14
            colourTUMirror = 13
            ctrlFKIKAttr = listCtrlFKIKAttr[2]
            ctrlFKIKAttrMirror = listCtrlFKIKAttr[3]
        else:
            isLeft = False
            leftRight = "r_"
            leftRightMirror = "l_"
            colourTU = 13
            colourTUMirror = 14
            ctrlFKIKAttr = listCtrlFKIKAttr[3]
            ctrlFKIKAttrMirror = listCtrlFKIKAttr[2]

        jntLegArray = self.jntLegArray

        # make sure the selections are not empty
        checkList = [self.jntNames]
        # However, editing them out is too much hassle,  it's easier just to leave them both false
        if ((checkList[0] == "")):
            mc.warning("You are missing a selection!")
            return
        else:
            #CRU.createLocatorToDelete()
            if not (CRU.checkLeftRight(isLeft, jntLegRoot)):
                # if the values are not lined up properly, break out
                mc.warning("You are selecting the incorrect side")
                return

            if mirrorRig:
                toReplace = "_" + leftRight
                toReplaceWith = "_" + leftRightMirror
                geoJntArrayMirror = []
                mirrorBase = mc.mirrorJoint(jntLegRoot, mirrorYZ=True, mirrorBehavior=True,
                                            searchReplace=[toReplace, toReplaceWith])
                jntLegRootMirror = mirrorBase[0]
                try:
                    mc.parent(jntLegRootMirror, w=True)
                except:
                    pass
                for mb in mirrorBase:
                    if mc.objectType(mb) == "joint":
                        geoJntArrayMirror.append(mb)
                isLeftMirror = not isLeft
                # we need to create mirror names for the legs
                jntLegArrayMirror = []
                for jntAA in jntLegArray:
                    jntLegArrayMirror.append(jntAA.replace(toReplace, toReplaceWith))

            self.makeLeg(isLeft, leftRight,
                         jntLegArray,
                         checkGeo, geoJntArray, colourTU, jntLegRoot,
                         ctrlFKIK, ctrlFKIKAttr, ctrlFKHip, checkboxTwists,
                         checkboxHip=checkboxHip)

            # print(mirrorRig)
            if mirrorRig:
                print("Mirroring")

                self.makeLeg(isLeftMirror, leftRightMirror,
                             jntLegArrayMirror,
                             checkGeo, geoJntArrayMirror, colourTUMirror, jntLegRootMirror,
                             ctrlFKIK, ctrlFKIKAttrMirror, ctrlFKHip, checkboxTwists,
                             checkboxHip=checkboxHip)
