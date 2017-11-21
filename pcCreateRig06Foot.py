'''
Created on May 30, 2014
for Tin Girl Book and game project

@author: Eyal Assaf
'''
import maya.cmds as mc
# import tgpUtils as ut
from functools import partial
from tgpBaseUI import BaseUI as UI

'''
import tgpBlendColors as bc
reload(bc)
bc.tgpBlendColors()

'''

import pcCreateRig00AUtilities

reload(pcCreateRig00AUtilities)
from pcCreateRig00AUtilities import pcCreateRigUtilities as CRU


class pcCreateRigFoot(UI):
    def __init__(self):

        self.window = "bcWindow"
        self.title = "pcRigFeet"
        self.winSize = (500, 325)

        self.createUI()

    def createCustom(self, *args):
        # selection type

        mc.rowColumnLayout(nc=2, cw=[(1, 500), (2, 500)], cs=[1, 5], rs=[1, 3])

        mc.text(l="Select The Ankle Root: ")
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
        mc.text(bgc=(0.85, 0.65, 0.25), l="Ankle Locator: ")
        mc.textFieldButtonGrp("locLoad_tfbg", cw=(1, 322), bl="  Load  ")

        mc.text(bgc=(0.85, 0.65, 0.25), l="IK Foot CTRL: ")
        mc.textFieldButtonGrp("ctrlIKLegLoad_tf", cw=(1, 322), bl="  Load  ", tx="CTRL_IK_l_leg")

        mc.text(bgc=(0.85, 0.65, 0.25), l="Upper Leg Joint: ")
        mc.textFieldButtonGrp("jntLegLoad_tf", cw=(1, 322), bl="  Load  ", tx="JNT_l_upperLeg")

        mc.setParent("..")

        mc.separator(st="in", h=20, w=500)

        # load buttons
        #

        mc.textFieldButtonGrp("locLoad_tfbg", e=True, bc=self.loadSrc1Btn)
        mc.textFieldButtonGrp("ctrlIKLegLoad_tf", e=True, bc=self.loadSrc2Btn)
        mc.textFieldButtonGrp("jntLegLoad_tf", e=True, bc=self.loadSrc3Btn)

        self.selLoad = []
        self.locArray = []
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
        self.locSel = self.tgpLoadTxBtn("locLoad_tfbg", "locator")

    def loadSrc2Btn(self):
        self.ctrlSel = self.loadCtrlBtn("ctrlIKLegLoad_tf")

    def loadSrc3Btn(self):
        self.jntSel = self.tgpLoadJntBtn("jntLegLoad_tf", "joint")

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
            return selName


    def tgpLoadJntBtn(self, loadBtn, myType):
        # hierarchy
        self.selLoad = []

        self.selLoad = mc.ls(sl=True, fl=True, type=myType)

        if (len(self.selLoad) != 1):
            mc.warning("Select only the root {0}".format(myType))
            return
        else:
            self.jointLegArray = self.getLegJnts(loadBtn, self.selLoad)

        return self.jointLegArray

    def getLegJnts(self, loadBtn, loadedValue):
        selName = ', '.join(loadedValue)
        mc.textFieldButtonGrp(loadBtn, e=True, tx=selName)

        # get the children joints
        self.parent = loadedValue[0]
        self.child = mc.listRelatives(loadedValue, ad=True, type="joint")
        # collect the joints in an array
        self.jointArray = [self.parent]
        # reverse the order of the children joints
        self.child.reverse()

        # add to the current list
        self.jointArray.extend(self.child)

        # checks if the joints are legs but not if there's a twist in it
        jointLegArray = [x for x in self.jointArray if ("leg" in x.lower()) and "Twist" not in x]
        self.jointRoot = loadedValue[0]

        return jointLegArray

    def tgpLoadTxBtn(self, loadBtn, myType):
        # hierarchy
        self.selLoad = []
        self.selLoad = mc.ls(sl=True, fl=True, type="transform")

        if (len(self.selLoad) != 1):
            mc.warning("Select only the root locator")
            return
        else:
            if CRU.checkObjectType(self.selLoad[0]) != "locator":
                mc.warning("The ankle should be a locator")
                return
            selName = ', '.join(self.selLoad)
            mc.textFieldButtonGrp(loadBtn, e=True, tx=selName)

            # get the children joints
            self.parent = self.selLoad[0]
            self.child = mc.listRelatives(self.selLoad, ad=True, type="transform")
            # collect the joints in an array
            self.locArray = [self.parent]
            # reverse the order of the children joints
            self.child.reverse()

            # add to the current list
            self.locArray.extend(self.child)
            locArraySorted = []
            for i in range(len(self.locArray)):
                sels = mc.listRelatives(self.locArray[i], c=True, s=True)
                if myType in mc.objectType(sels) or myType == mc.objectType(sels):
                    locArraySorted.append(self.locArray[i])

            self.locRoot = self.selLoad[0]
            self.locArray = locArraySorted

        return self.locArray

    def tgpSetDriverEnumWorldFollowLeg(self, driver, driverAttr, driven, *args):

        # sets the leg enum to shift between world follow and knee follow
        w0w1Attr = mc.listAttr(driven)[-1:]
        CRU.setDriverDrivenValues(driver, driverAttr, driven, w0w1Attr[0], 0, 1)
        CRU.setDriverDrivenValues(driver, driverAttr, driven, w0w1Attr[0], 1, 0)

    def createRotateIKFoot(self, ctrlIKLeg, locFootRoot, isLeft, leftRight, *args):
        rotVals = ["rotX", "rotY", "rotZ"]
        for i in range(len(rotVals)):
            mc.addAttr(ctrlIKLeg, longName=rotVals[i], at="float", k=True)

        if isLeft:
            mult = 1;
        else:
            mult = -1;

        # Loc_ankle.rotate is connected to CTRL_IK_Leg.rotate
        footExpr = "{0}.rotateX = {1}.rotX;\n" \
                   "{0}.rotateY= {1}.rotY*({2});\n" \
                   "{0}.rotateZ = {1}.rotZ*({2});".format(locFootRoot, ctrlIKLeg, mult)

        xprName = "expr_" + leftRight + "footTwist"  # changes to account for the left or right

        mc.expression(s=footExpr, n=xprName)

    def createFootRollAll(self, ctrlIKLeg, footRoll, locHeel, locBall, locToeEnd, *args):
        footRollValues = [0, -10, 5, 10]
        footRollValuesHeel = [0, -50, 0, 0]
        footRollValuesBall = [0, 0, 40, 0]
        footRollValuesEnd = [0, 0, 0, 60]

        self.setFootAttributeValues(ctrlIKLeg, footRoll, footRollValues, locHeel, footRollValuesHeel, "rotateX")
        self.setFootAttributeValues(ctrlIKLeg, footRoll, footRollValues, locBall, footRollValuesBall, "rotateX")
        self.setFootAttributeValues(ctrlIKLeg, footRoll, footRollValues, locToeEnd, footRollValuesEnd, "rotateX")

    def createFootRollIndividual(self, ctrlIKLeg, heelOffset, ballOffset, toePivotOffset, locHeel, locBall, locToeEnd,
                                 *args):
        # individual values
        footRollIndiVals = [0, 10]
        footRollIndiValsHeel = [0, -50]
        footRollIndiValsBall = [0, 40]
        footRollIndiValsToeEnd = [0, 60]
        self.setFootAttributeValues(ctrlIKLeg, heelOffset, footRollIndiVals, locHeel, footRollIndiValsHeel, "rotateX")
        self.setFootAttributeValues(ctrlIKLeg, ballOffset, footRollIndiVals, locBall, footRollIndiValsBall, "rotateX")
        self.setFootAttributeValues(ctrlIKLeg, toePivotOffset, footRollIndiVals, locToeEnd, footRollIndiValsToeEnd,
                                    "rotateX")

    def createHeelAndToeTwists(self, ctrlIKLeg, twistValues, heelTwist, locHeel, toeTwist, locToeEnd, isLeft, *args):

        # I can accidentally flip the direction of the locators, so I need to keep these values separate
        heelTwistValues = [0, -50, 50]
        toeTwistValues = [0, 50, -50]

        self.setFootAttributeValues(ctrlIKLeg, heelTwist, twistValues, locHeel, heelTwistValues, "rotateY", isLeft)
        self.setFootAttributeValues(ctrlIKLeg, toeTwist, twistValues, locToeEnd, toeTwistValues, "rotateY", isLeft)

    def createSideToSide(self, ctrlIKLeg, twistValues, sideToSide, locInner, locOuter, isLeft, *args):
        sideToSideInnerValues = [0, 50, 0]
        sideToSideOuterValues = [0, 0, -50]

        self.setFootAttributeValues(ctrlIKLeg, sideToSide, twistValues, locInner, sideToSideInnerValues, "rotateZ",
                                    isLeft)
        self.setFootAttributeValues(ctrlIKLeg, sideToSide, twistValues, locOuter, sideToSideOuterValues, "rotateZ",
                                    isLeft)

    def createToeFlap(self, ctrlIKLeg, toeFlap, twistValues, locToeFlap, *args):

        toeFlapValues = [0, 40, -40]
        self.setFootAttributeValues(ctrlIKLeg, toeFlap, twistValues, locToeFlap, toeFlapValues, "rotateX")

    def createAutoKneeFollow(self, locFootRoot, kneeOffsetCtrl, leftRight, *args):
        autoKneeName = "LOC_" + leftRight + "kneeFollow"

        # Moves the knee follow locator into the proper place
        locAutoKneeFollow = mc.spaceLocator(p=(0, 0, 0), name=autoKneeName)[0]
        toDelete = mc.parentConstraint(locFootRoot, locAutoKneeFollow)
        mc.delete(toDelete)

        # constrains the locator to the foot in point and orient
        kneeFollowPnt = mc.pointConstraint(locFootRoot, locAutoKneeFollow)[0]
        kneeFollowOrntY = mc.orientConstraint(locFootRoot, locAutoKneeFollow, skip=["x", "z"])[0]

        kneeFollowPrnt = mc.parentConstraint(locAutoKneeFollow, kneeOffsetCtrl[0], mo=True)
        kneeFollow = "kneeFollow"
        mc.addAttr(kneeOffsetCtrl[1], longName=kneeFollow, at="enum", k=True, en="foot:world")

        # tgpSetDriverEnumWorldFollow(driver, driverAttr, driven, numNodes)
        # sets the autoKneeControl parent values to on or off
        self.tgpSetDriverEnumWorldFollowLeg(kneeOffsetCtrl[1], kneeFollow, kneeFollowPnt)
        self.tgpSetDriverEnumWorldFollowLeg(kneeOffsetCtrl[1], kneeFollow, kneeFollowOrntY)
        return locAutoKneeFollow

    def makeFoot(self, ctrlIKLeg, offsetFoot, locFootRoot, jntLegs, locArray, leftRight, isLeft, colourTU, *args):

        # gets a bunch of values for later use
        childrenFoot = mc.listRelatives(ctrlIKLeg, ad=True, type="ikHandle")
        ikLeg = [x for x in childrenFoot if "leg" in x][0]
        ikBall = [x for x in childrenFoot if "ball" in x][0]
        ikToe = [x for x in childrenFoot if "toe" in x][0]
        legLength = mc.getAttr("{0}.ty".format(jntLegs[1])) + mc.getAttr("{0}.ty".format(jntLegs[-1]))

        locToeFlap = [x for x in locArray if "toeFlap" in x][0]
        mc.parent(ikBall, ikToe, locToeFlap)
        locBall = [x for x in locArray if "ball" in x][0]
        locToeEnd = [x for x in locArray if "toeEnd" in x][0]
        locHeel = [x for x in locArray if "heel" in x][0]
        locInner = [x for x in locArray if "Inner" in x][0]
        locOuter = [x for x in locArray if "Outer" in x][0]
        mc.parent(ikLeg, locBall)
        mc.parent(offsetFoot, ctrlIKLeg)

        # meaningless break, just for ease of use
        mc.addAttr(ctrlIKLeg, longName="break1", nn="_____", at="enum", k=True, en="_____:_____")

        # Rotating the IK Foot
        self.createRotateIKFoot(ctrlIKLeg, locFootRoot, isLeft, leftRight)

        # gets a bunch of values for later use
        footRoll = "footRoll"
        heelOffset = "heelOffset"
        ballOffset = "ballOffset"
        toePivotOffset = "toePivotOffset"
        heelTwist = "heelTwist"
        toeTwist = "toeTwist"
        sideToSide = "sideToSide"
        toeFlap = "toeFlap"

        footAttributes = [[footRoll, -10, 10], [heelOffset, 0, 10], [ballOffset, 0, 10], [toePivotOffset, 0, 10],
                          [heelTwist, -10, 10], [toeTwist, -10, 10], [sideToSide, -10, 10], [toeFlap, -10, 10], ]

        mc.addAttr(ctrlIKLeg, longName="break2", nn="_____", at="enum", k=True, en="_____:_____")
        for i in range(len(footAttributes)):
            mc.addAttr(ctrlIKLeg, longName=footAttributes[i][0], at="float", k=True, minValue=footAttributes[i][1],
                       maxValue=footAttributes[i][2])

        # Foot Rolling
        self.createFootRollAll(ctrlIKLeg, footRoll, locHeel, locBall, locToeEnd)

        self.createFootRollIndividual(ctrlIKLeg, heelOffset, ballOffset, toePivotOffset, locHeel, locBall, locToeEnd, )

        # common values that are used
        twistValues = [0, -10, 10]

        # Heel and Toe Twist
        self.createHeelAndToeTwists(ctrlIKLeg, twistValues, heelTwist, locHeel, toeTwist, locToeEnd, isLeft)

        # Adding Side To Side
        self.createSideToSide(ctrlIKLeg, twistValues, sideToSide, locInner, locOuter, isLeft)

        # Adding the toeFlap
        self.createToeFlap(ctrlIKLeg, toeFlap, twistValues, locToeFlap)

        # Adding Knee Controls
        # I prefer creating new ones over using elbows
        # createKnee(ikJntsDrive, leftRight, legLength, ikLeg0, isLeft):
        kneeOffsetCtrl = self.createKnee(jntLegs, leftRight, legLength, ikLeg, isLeft)

        # Auto Knee Follow
        locAutoKneeFollow = self.createAutoKneeFollow(locFootRoot, kneeOffsetCtrl, leftRight)

        # Cleaning Up

        self.footCleanUp(locAutoKneeFollow, leftRight, offsetFoot, kneeOffsetCtrl, ctrlIKLeg, colourTU)

    def footCleanUp(self, locAutoKneeFollow, leftRight, offsetFoot, kneeOffsetCtrl, ctrlIKLeg, colourTU, *args):
        # rename the GRP_LOC_worldFollow to GRP_LOC_follow if not already
        try:
            grpFollowWorld = mc.ls("GRP_LOC_worldFollow")[0]
        except:
            try:
                grpFollowWorld = mc.ls("GRP_LOC_follow")[0]
            except:
                mc.warning("Your follow locator is not properly named")
                return
            pass
        # replace "GRP_LOC_worldFollow" with "GRP_LOC_follow"
        grpFollowWorldRename = grpFollowWorld.replace("worldFollow", "follow")
        try:
            # rename if necessary
            mc.rename(grpFollowWorld, grpFollowWorldRename)
        except:
            pass

        # parents the follow control under the world follow group
        mc.parent(locAutoKneeFollow, grpFollowWorldRename)

        # makes invisible the locator for the world follow and the locators under the foot
        mc.setAttr("{0}.visibility".format(locAutoKneeFollow), False)
        mc.setAttr("{0}.visibility".format(offsetFoot), False)

        # groups the knee under the leg rig
        grpRigLeg = "GRP_rig_" + leftRight + "leg"
        mc.parent(kneeOffsetCtrl[0], grpRigLeg)

        # makes our colours the corresponding side values
        mc.setAttr('{0}.overrideEnabled'.format(kneeOffsetCtrl[0]), 1)
        mc.setAttr("{0}.overrideColor".format(kneeOffsetCtrl[0]), colourTU)

        mc.setAttr('{0}.overrideEnabled'.format(offsetFoot), 1)
        mc.setAttr("{0}.overrideColor".format(offsetFoot), colourTU)

        mc.connectAttr("{0}.v".format(ctrlIKLeg), "{0}.v".format(kneeOffsetCtrl[1]))

        # lock and hide stuff at the end
        CRU.lockHideCtrls(kneeOffsetCtrl[1], scale=True, rotate=True, visible=True)

    def tgpCreateMirror(self, offsetFoot, leftRightReplace, leftRightReplaceMirror, jntLegs):
        offsetFootStuffMirrorWork = mc.duplicate(offsetFoot, rc=True)
        offsetFootMirrorWork = offsetFootStuffMirrorWork[0]
        offsetFootMirror = offsetFootMirrorWork.replace(leftRightReplace, leftRightReplaceMirror)[:-1]

        offsetFootStuffMirror = []
        for i in range(len(offsetFootStuffMirrorWork)):
            # switch the l/r,
            toRename = offsetFootStuffMirrorWork[i].replace(leftRightReplace, leftRightReplaceMirror)[:-1]
            mc.rename(offsetFootStuffMirrorWork[i], toRename)
            offsetFootStuffMirror.append(toRename)
        jntLegsMirror = []
        # get the mirror legs for future reference too
        for i in range(len(jntLegs)):
            jntLegsMirror.append(jntLegs[i].replace(leftRightReplace, leftRightReplaceMirror))

        # takes the initial offset value, duplicates it, flips the values around, then freezes the transformation
        # translates everything into place
        mirrorXTrans = mc.getAttr("{0}.tx".format(offsetFootMirror)) * -1
        mirrorYRot = mc.getAttr("{0}.ry".format(offsetFootMirror)) * -1
        mirrorXScal = mc.getAttr("{0}.sx".format(offsetFootMirror)) * -1
        mc.setAttr("{0}.tx".format(offsetFootMirror), mirrorXTrans)
        mc.setAttr("{0}.ry".format(offsetFootMirror), mirrorYRot)
        mc.setAttr("{0}.sx".format(offsetFootMirror), mirrorXScal)
        mc.makeIdentity(offsetFootMirror, apply=True, scale=True)

        return offsetFootStuffMirror, offsetFootMirror, jntLegsMirror

    def setFootAttributeValues(self, ctrlIKLeg, footAttribute, footAttributeValues, loc, footAttributeValuesLoc,
                               setValue, isLeft=True):
        # the values may need to be negative when the foot is switched, but some of the values work fine with both sides so we make it a default
        if isLeft:
            mult = 1
        else:
            mult = -1
        for i in range(len(footAttributeValues)):
            # def setDriverDrivenValues(driver, driverAttribute, driven, drivenAttribute, driverValue, drivenValue):
            CRU.setDriverDrivenValues(ctrlIKLeg, footAttribute, loc, setValue, footAttributeValues[i],
                                      footAttributeValuesLoc[i] * mult)

    def createKnee(self, ikJntsDrive, leftRight, legLength, ikLeg, isLeft, *args):

        kneeName = "CTRL_" + leftRight + "knee"

        kneeOffsetCtrl = []
        kneeOffsetCtrl.append(mc.group(n="OFFSET_" + kneeName, w=True, em=True))
        kneeOffsetCtrl.append(mc.spaceLocator(p=(0, 0, 0), name=kneeName)[0])
        kneeOffsetCtrl.append(mc.group(n="AUTO_" + kneeName, w=True, em=True))

        mc.parent(kneeOffsetCtrl[2], kneeOffsetCtrl[0])
        mc.parent(kneeOffsetCtrl[1], kneeOffsetCtrl[2])

        toDelete = mc.pointConstraint(ikJntsDrive, kneeOffsetCtrl[0])
        toDelete2 = mc.aimConstraint(ikJntsDrive[1], kneeOffsetCtrl[0], aim=(0, 0, 1))

        mc.delete(toDelete, toDelete2)

        if not isLeft:
            legLength = -legLength

        # moves along the Z axis, relative to its pre-move position, along the object space, using worldspace distance units
        mc.move(0, 0, legLength / 2, kneeOffsetCtrl[0], r=True, os=True, wd=True)

        mc.poleVectorConstraint(kneeOffsetCtrl[1], ikLeg)

        return kneeOffsetCtrl

    def tgpMakeBC(self, *args):

        checkSelLeft = mc.radioButtonGrp("selLegType_rbg", q=True, select=True)
        mirrorSel = mc.radioButtonGrp("selLegMirrorType_rbg", q=True, select=True)
        locNames = mc.textFieldButtonGrp("locLoad_tfbg", q=True, text=True)

        ctrlIKLeg = mc.textFieldButtonGrp("ctrlIKLegLoad_tf", q=True, text=True)

        jntRoot = mc.textFieldButtonGrp("jntLegLoad_tf", q=True, text=True)
        if not jntRoot:
            mc.warning("You need to select a root joint for the legs")
            return
        jntLegs = self.getLegJnts("jntLegLoad_tf", [jntRoot])
        if not jntLegs:
            mc.warning("You need to select leg joint")
            return

        try:
            locFootRoot = self.locArray[0]

        except:
            mc.warning("No locator selected!")
            return
        try:
            offsetFoot = mc.listRelatives(locFootRoot, parent=True)[0]
        except:
            # if this doesn't work, tell the user to check if under
            mc.warning("Be sure the locator is under an offset")
            return
        locArray = self.locArray

        if mirrorSel == 1:
            mirrorRig = False
        else:
            mirrorRig = True

        if checkSelLeft == 1:
            isLeft = True
            leftRight = "l_"
            leftRightMirror = "r_"

            colourTU = 14
            colourTUMirror = 13
        else:
            isLeft = False
            leftRight = "r_"
            leftRightMirror = "l_"
            colourTU = 13
            colourTUMirror = 14

        leftRightReplace = "_" + leftRight
        leftRightReplaceMirror = "_" + leftRightMirror

        # make sure the selections are not empty
        checkList = [locNames]
        # note: the isCopy is not applicable due to the differences between the leg and arm joint setup.
        # However, editing them out is too much hassle,  it's easier just to leave them both false
        if ((checkList[0] == "")):
            mc.warning("You are missing a selection!")
            return
        else:
            # CRU.createLocatorToDelete()
            if not (CRU.checkLeftRight(isLeft, locFootRoot)):
                # if the values are not lined up properly, break out
                mc.warning("You are selecting the incorrect side")
                return

            if mirrorRig:
                # we want to get the foot before we add anything to it. When doing this programmatically, it's easier
                offsetFootStuffMirror, offsetFootMirror, jntLegsMirror = self.tgpCreateMirror(offsetFoot,
                                                                                              leftRightReplace,
                                                                                              leftRightReplaceMirror,
                                                                                              jntLegs)

            # makeFoot(ctrlIKLeg, offsetFoot, locFootRoot, jntLegs, locArray, leftRight, isLeft)
            self.makeFoot(ctrlIKLeg, offsetFoot, locFootRoot, jntLegs, locArray, leftRight, isLeft, colourTU)

            if mirrorRig:

                print("Mirroring")

                isLeftMirror = not isLeft

                ctrlIKLegMirror = ctrlIKLeg.replace(leftRightReplace, leftRightReplaceMirror)
                locFootRootMirror = locFootRoot.replace(leftRightReplace, leftRightReplaceMirror)
                locArrayMirror = []
                for i in range(len(locArray)):
                    locArrayMirror.append(locArray[i].replace(leftRightReplace, leftRightReplaceMirror))

                self.makeFoot(ctrlIKLegMirror, offsetFootMirror, locFootRootMirror, jntLegsMirror, locArrayMirror,
                              leftRightMirror, isLeftMirror, colourTUMirror)
