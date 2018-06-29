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


class pcCreateRigAlt04FeetCode(object):
    def __init__(self, mirrorSel=2, lrSel=1,
                 locName="LOC_l_heel", ctrlIKFootCheck="CTRL_l_foot"):

        self.tgpMakeBC(mirrorSel, lrSel, locName, ctrlIKFootCheck)

    def createFootRollAll(self, ctrlIKFoot,
                          locHeel, locBall, locToe,
                          roll, bendLimitAngle, toeStraight,
                          leftRight,
                          *args):
        heelRotClamp = "{0}heel_rotClamp".format(leftRight)
        mc.shadingNode("clamp", n=heelRotClamp, au=True)
        mc.connectAttr("{0}.{1}".format(ctrlIKFoot, roll), "{0}.inputR".format(heelRotClamp))
        mc.setAttr("{0}.minR".format(heelRotClamp), self.heelMax)
        mc.setAttr("{0}.maxR".format(heelRotClamp), 0)
        mc.connectAttr("{0}.outputR".format(heelRotClamp), "{0}.rotateX".format(locHeel))

        # the foot ball clamp
        # Ball Heel Roll
        ballRotClampZero2B = "{0}ball_zeroToBendClamp".format(leftRight)
        mc.shadingNode("clamp", n=ballRotClampZero2B, au=True)
        mc.connectAttr("{0}.{1}".format(ctrlIKFoot, roll), "{0}.inputR".format(ballRotClampZero2B))
        mc.setAttr("{0}.maxR".format(ballRotClampZero2B), 90)
        '''mc.connectAttr("{0}.outputR".format(ballRotClampZero2B),
                       "{0}.rotateX".format(locBall))  # will be undone later, but useful for testing'''

        # Ball Over Rotation
        footBend2SClamp = "{0}foot_bendToStraightClamp".format(leftRight)  # bendToStraight
        mc.shadingNode("clamp", n=footBend2SClamp, au=True)

        mc.connectAttr("{0}.{1}".format(ctrlIKFoot, bendLimitAngle), "{0}.minR".format(footBend2SClamp))
        mc.connectAttr("{0}.{1}".format(ctrlIKFoot, toeStraight), "{0}.maxR".format(footBend2SClamp))
        mc.connectAttr("{0}.{1}".format(ctrlIKFoot, roll), "{0}.inputR".format(footBend2SClamp))

        #####

        # create a set range to allow for a percentage, then set the range from 0 to 1
        footBend2SPercent = "{0}foot_bendToStraightPercent".format(leftRight)  # bendToStraight
        mc.shadingNode("setRange", n=footBend2SPercent, au=True)
        mc.connectAttr("{0}.minR".format(footBend2SClamp), "{0}.oldMinX".format(footBend2SPercent))
        mc.connectAttr("{0}.maxR".format(footBend2SClamp), "{0}.oldMaxX".format(footBend2SPercent))
        mc.setAttr("{0}.minX".format(footBend2SPercent), 0)
        mc.setAttr("{0}.maxX".format(footBend2SPercent), 1)
        mc.connectAttr("{0}.inputR".format(footBend2SClamp), "{0}.valueX".format(footBend2SPercent))

        # we meed a percentage to multiply now
        footRollMult = "{0}foot_roll_MUL".format(leftRight)  # bendToStraight
        mc.shadingNode("multiplyDivide", n=footRollMult, au=True)
        mc.connectAttr("{0}.outValueX".format(footBend2SPercent), "{0}.input1X".format(footRollMult))
        mc.connectAttr("{0}.inputR".format(footBend2SClamp), "{0}.input2X".format(footRollMult))
        mc.connectAttr("{0}.outputX".format(footRollMult), "{0}.rotateX".format(locToe))

        ######
        # fixing over rotation
        mc.connectAttr("{0}.{1}".format(ctrlIKFoot, bendLimitAngle), "{0}.maxR".format(ballRotClampZero2B))
        ballZero2BPercent = "{0}ball_zeroToBendPercent".format(leftRight)  # zeroToBendPercent
        mc.shadingNode("setRange", n=ballZero2BPercent, au=True)
        mc.connectAttr("{0}.minR".format(ballRotClampZero2B), "{0}.oldMinX".format(ballZero2BPercent))
        mc.connectAttr("{0}.maxR".format(ballRotClampZero2B), "{0}.oldMaxX".format(ballZero2BPercent))
        mc.setAttr("{0}.minX".format(ballZero2BPercent), 0)
        mc.setAttr("{0}.maxX".format(ballZero2BPercent), 1)
        mc.connectAttr("{0}.inputR".format(ballRotClampZero2B),
                       "{0}.valueX".format(ballZero2BPercent))  # connects the roll value to value x

        footInvertPercent = "{0}foot_invertPercentage".format(leftRight)
        mc.shadingNode("plusMinusAverage", n=footInvertPercent, au=True)
        mc.setAttr("{0}.operation".format(footInvertPercent), 2)
        mc.setAttr("{0}.input1D[0]".format(footInvertPercent), 1)
        mc.setAttr("{0}.input1D[1]".format(footInvertPercent), 1)
        mc.connectAttr("{0}.outValueX".format(footBend2SPercent), "{0}.input1D[1]".format(footInvertPercent))

        ballPercentMul = "{0}ball_percent_MUL".format(leftRight)
        mc.shadingNode("multiplyDivide", n=ballPercentMul, au=True)
        mc.connectAttr("{0}.outValueX".format(ballZero2BPercent), "{0}.input1X".format(ballPercentMul))
        mc.connectAttr("{0}.output1D".format(footInvertPercent), "{0}.input2X".format(ballPercentMul))

        ballRollMul = "{0}ball_roll_MUL".format(leftRight)
        mc.shadingNode("multiplyDivide", n=ballRollMul, au=True)
        mc.connectAttr("{0}.outputX".format(ballPercentMul), "{0}.input1X".format(ballRollMul))
        mc.connectAttr("{0}.{1}".format(ctrlIKFoot, roll), "{0}.input2X".format(ballRollMul))
        mc.connectAttr("{0}.outputX".format(ballRollMul), "{0}.rotateX".format(locBall))

    def createSideToSide(self, ctrlIKFoot, sideToSide, locInner, locOuter, leftRight, isLeft, *args):

        if isLeft:
            imVal = 1
        else:
            imVal = -1

        # CRU.setDriverDrivenValues(driver, driverAttribute, driven, drivenAttribute, driverValue, drivenValue)
        CRU.setDriverDrivenValues(ctrlIKFoot, sideToSide, locInner, "rotateZ", 0, 0)
        CRU.setDriverDrivenValues(ctrlIKFoot, sideToSide, locOuter, "rotateZ", 0, 0)
        CRU.setDriverDrivenValues(ctrlIKFoot, sideToSide, locInner, "rotateZ", -90, imVal * 90)
        CRU.setDriverDrivenValues(ctrlIKFoot, sideToSide, locOuter, "rotateZ", 90, imVal * -90)

    def createToeWiggle(self, ctrlIKFoot, toeWiggle, ikToe, locBall, locToe, leftRight, *args):
        grpToeWiggle = "GRP_{0}toeWiggle".format(leftRight)
        mc.group(em=True, name=grpToeWiggle, w=True)
        ikToeParent = mc.listRelatives(ikToe, p=True)[0]
        todelete = mc.pointConstraint(locBall, grpToeWiggle)
        mc.delete(todelete)

        mc.parent(grpToeWiggle, ikToeParent)
        mc.parent(ikToe, grpToeWiggle)
        mc.connectAttr("{0}.{1}".format(ctrlIKFoot, toeWiggle), "{0}.rotateX".format(grpToeWiggle))
        mc.parent(grpToeWiggle, locToe)

    def createFootRollExtra(self, ctrlIKFoot, attribute, locObj, toReplace="LOC", toReplaceWith="GRP"):
        grpObj = locObj.replace(toReplace, toReplaceWith)

        CRU.createParentGroup(locObj, grpObj, point=True)
        mc.connectAttr("{0}.{1}".format(ctrlIKFoot, attribute), "{0}.rotateX".format(grpObj))

    def makeFootComplete(self, ctrlIKFoot, locArray, leftRight, isLeft, *args):

        # gets a bunch of values for later use
        ikFootChildren = mc.listRelatives(ctrlIKFoot, ad=True, type="ikHandle")
        ikFootPV = [x for x in ikFootChildren if "pv" in x][0]
        ikFootNoFlip = [x for x in ikFootChildren if "noFlip" in x][0]
        ikBall = [x for x in ikFootChildren if "ball" in x][0]
        ikToe = [x for x in ikFootChildren if "toe" in x][0]

        # get the locators under the CTRL_l_foot
        footChildrenAlt = mc.listRelatives(ctrlIKFoot)
        locFootGrandhildren = mc.listRelatives(footChildrenAlt, type="locator")
        locFootChildren = mc.listRelatives(locFootGrandhildren, p=True)
        grpKnee = [x for x in footChildrenAlt if "knee" in x][0]

        locBall = [x for x in locArray if "ball" in x][0]
        locToe = [x for x in locArray if "toe" in x][0]
        locHeel = [x for x in locArray if "heel" in x][0]
        locInner = [x for x in locArray if "Inner" in x][0]
        locOuter = [x for x in locArray if "Outer" in x][0]

        #####
        '''
        CTRL_l_foot
            (other stuff)
                LOC_l_heel
                    HDL_l_toe
                    LOC_l_toe
                        LOC_l_ball
                            HDL_noFlip_l_foot
                            HDL_pv_l_foot
                            HDL_l_ball
            
                            GRP_noFlip_l_knee
                        
                            LOC_l_knee_to_l_footEnd				
                            LOC_IK_pv_l_leg_lengthEnd
                            LOC_IK_noFlip_l_leg_lengthEnd
        '''
        for i in range(len(locFootChildren)):
            mc.parent(locFootChildren[i], locBall)

        mc.parent(ikFootNoFlip, locBall)
        mc.parent(ikFootPV, locBall)

        mc.parent(ikBall, locBall)
        mc.parent(grpKnee, locBall)

        mc.parent(ikToe, locInner)

        mc.parent(locHeel, ctrlIKFoot)

        # meaningless break, just for ease of use
        mc.addAttr(ctrlIKFoot, longName="break1", nn="-----", at="enum", k=True, en="_____")

        # add values to the ctrlIKFoot

        roll = "roll"
        bendLimitAngle = "bendLimitAngle"
        toeStraight = "toeStraight"
        self.heelMax = -90

        mc.addAttr(ctrlIKFoot, longName=roll, at="float", k=True, min=self.heelMax)
        mc.addAttr(ctrlIKFoot, longName=bendLimitAngle, at="float", k=True, dv=45)
        mc.addAttr(ctrlIKFoot, longName=toeStraight, at="float", k=True, dv=75)

        mc.addAttr(ctrlIKFoot, longName="break2", nn="-----", at="enum", k=True, en="_____")

        tilt = "tilt"
        lean = "lean"
        toeSpin = "toeSpin"
        toeWiggle = "toeWiggle"

        mc.addAttr(ctrlIKFoot, longName=tilt, at="float", k=True, min=-90, max=90)
        mc.addAttr(ctrlIKFoot, longName=lean, at="float", k=True)
        mc.addAttr(ctrlIKFoot, longName=toeSpin, at="float", k=True)
        mc.addAttr(ctrlIKFoot, longName=toeWiggle, at="float", k=True)

        mc.addAttr(ctrlIKFoot, longName="break3", nn="-----", at="enum", k=True, en="_____")

        heelLift = "heelLift"
        ballLift = "ballLift"
        toeLift = "toeLift"

        mc.addAttr(ctrlIKFoot, longName=heelLift, at="float", k=True, min=self.heelMax, max=0)
        mc.addAttr(ctrlIKFoot, longName=ballLift, at="float", k=True, min=0)
        mc.addAttr(ctrlIKFoot, longName=toeLift, at="float", k=True, min=0)
        '''footRoll = "footRoll"
        heelOffset = "heelOffset"
        ballOffset = "ballOffset"
        toePivotOffset = "toePivotOffset"
        heelTwist = "heelTwist"
        toeTwist = "toeTwist"
        sideToSide = "sideToSide"
        toeFlap = "toeFlap"

        footAttributes = [[footRoll, -10, 10], [heelOffset, 0, 10], [ballOffset, 0, 10], [toePivotOffset, 0, 10],
                          [heelTwist, -10, 10], [toeTwist, -10, 10], [sideToSide, -10, 10], [toeFlap, -10, 10], ]'''

        '''mc.addAttr(ctrlIKFoot, longName="break2", nn="_____", at="enum", k=True, en="_____:_____")
        for i in range(len(footAttributes)):
            mc.addAttr(ctrlIKFoot, longName=footAttributes[i][0], at="float", k=True, minValue=footAttributes[i][1],
                       maxValue=footAttributes[i][2])'''

        # Foot Rolling
        self.createFootRollAll(ctrlIKFoot, locHeel, locBall, locToe, roll, bendLimitAngle, toeStraight, leftRight)

        # Adding Side To Side
        self.createSideToSide(ctrlIKFoot, tilt, locInner, locOuter, leftRight, isLeft)

        # Lean and toeSpin
        # lean is useful when your toe is planeted but you are balancing on it
        mc.connectAttr("{0}.{1}".format(ctrlIKFoot, lean), "{0}.rotateZ".format(locBall))
        mc.connectAttr("{0}.{1}".format(ctrlIKFoot, toeSpin), "{0}.rotateY".format(locToe))
        CRU.changeRotateOrder(locToe, "ZXY")

        self.createToeWiggle(ctrlIKFoot, toeWiggle, ikToe, locBall, locToe, leftRight)

        # cleaning up
        for i in range(len(locArray)):
            mc.setAttr('{0}.v'.format(locArray[i]), False)

        self.createFootRollExtra(ctrlIKFoot, heelLift, locHeel)
        self.createFootRollExtra(ctrlIKFoot, toeLift, locToe)
        self.createFootRollExtra(ctrlIKFoot, ballLift, locBall)

        return

    def tgpCreateMirror(self, locHeel, leftRightReplace, leftRightReplaceMirror):
        locHeelMirrorsWork = mc.duplicate(locHeel, rc=True)

        locHeelArrayMirror = []

        for i in range(len(locHeelMirrorsWork)):
            # switch the l/r,
            toRename = locHeelMirrorsWork[i].replace(leftRightReplace, leftRightReplaceMirror)[:-1]
            mc.rename(locHeelMirrorsWork[i], toRename)
            locHeelArrayMirror.append(toRename)
        locHeelMirror = locHeelArrayMirror[0]

        # takes the initial offset value, duplicates it, flips the values around, then freezes the transformation
        # translates everything into place
        mirrorXTrans = mc.getAttr("{0}.tx".format(locHeelMirror)) * -1
        mirrorYRot = mc.getAttr("{0}.ry".format(locHeelMirror)) * -1
        mirrorXScal = mc.getAttr("{0}.sx".format(locHeelMirror)) * -1
        mc.setAttr("{0}.tx".format(locHeelMirror), mirrorXTrans)
        mc.setAttr("{0}.ry".format(locHeelMirror), mirrorYRot)
        mc.setAttr("{0}.sx".format(locHeelMirror), mirrorXScal)
        mc.makeIdentity(locHeelMirror, apply=True, scale=True)

        return locHeelArrayMirror, locHeelMirror

    def tgpMakeBC(self, mirrorSel=None, lrSel=None,
                  locName=None, ctrlIKFootCheck=None, *args):

        # symmetry = CRU.checkSymmetry()  # we want symmetry turned off for this process
        if mirrorSel is None:
            mirrorSel = mc.radioButtonGrp("selLegMirrorType_rbg", q=True, select=True)
        if lrSel is None:
            lrSel = mc.radioButtonGrp("selLegType_rbg", q=True, select=True)

        if mirrorSel == 1:
            mirrorRig = False
        else:
            mirrorRig = True

        if lrSel == 1:
            isLeft = True
            leftRight = CRU.valLeft
            leftRightMirror = CRU.valRight
        else:
            isLeft = False
            leftRight = CRU.valRight
            leftRightMirror = CRU.valLeft

        leftRightReplace = "_" + leftRight
        leftRightReplaceMirror = "_" + leftRightMirror

        if locName is None:
            locName = mc.textFieldButtonGrp("locLoad_tfbg", q=True, text=True)
            passVal = "locLoad_tfbg"
        else:
            passVal = None
        try:
            locFootRoot = locName
        except:
            mc.warning("No locator selected!")
            return

        locNames = CRU.tgpGetLocs(locName, passVal, "locator", "Heel Locator", ["LOC", "heel"])
        if not (CRU.checkLeftRight(isLeft, locFootRoot)):
            # if the values are not lined up properly, break out
            mc.warning("You are selecting the incorrect side for the locator")
            return

        if ctrlIKFootCheck is None:
            ctrlIKFootCheck = mc.textFieldButtonGrp("ctrlIKFootLoad_tf", q=True, text=True)
            passVal = "ctrlIKFootLoad_tf"
        else:
            passVal = None
        ctrlIKFoot = CRU.tgpGetTx(ctrlIKFootCheck, passVal, "nurbsCurve", "IK Foot Control",
                                  ["CTRL", "foot"], "control")
        if not (CRU.checkLeftRight(isLeft, ctrlIKFoot)):
            # if the values are not lined up properly, break out
            mc.warning("You are selecting the incorrect side for the IK leg control")
            return

        locArray = locNames

        # make sure the selections are not empty
        checkList = [locNames]
        if checkList is None:
            checkList = [locNames]
        # note: the isCopy is not applicable due to the differences between the leg and arm joint setup.
        # However, editing them out is too much hassle,  it's easier just to leave them both false
        if ((checkList[0] == "") or (checkList[0] is None)):
            mc.warning("You are missing a selection!")
            return
        else:
            # CRU.createLocatorToDelete()

            if mirrorRig:
                # we want to get the foot before we add anything to it. When doing this programmatically, it's easier
                self.tgpCreateMirror(locFootRoot,
                                     leftRightReplace,
                                     leftRightReplaceMirror,
                                     )

            # makeFootComplete(ctrlIKFoot, locFootRoot, jntLegs, locArray, leftRight, isLeft)
            self.makeFootComplete(ctrlIKFoot, locArray, leftRight, isLeft)

            if mirrorRig:

                print("Mirroring")

                isLeftMirror = not isLeft

                ctrlIKFootMirror = ctrlIKFoot.replace(leftRightReplace, leftRightReplaceMirror)
                locFootRootMirror = locFootRoot.replace(leftRightReplace, leftRightReplaceMirror)
                locArrayMirror = []
                for i in range(len(locArray)):
                    locArrayMirror.append(locArray[i].replace(leftRightReplace, leftRightReplaceMirror))

                self.makeFootComplete(ctrlIKFootMirror, locArrayMirror, leftRightMirror, isLeftMirror)

            # reset the symmetry to the default because otherwise we might get wonky results
            # mc.symmetricModelling(symmetry=symmetry)
