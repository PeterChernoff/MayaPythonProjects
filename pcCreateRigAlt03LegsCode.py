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

reload(pcCreateRigAlt00AUtilities)

from pcCreateRigAlt00AUtilities import pcCreateRigUtilities as CRU


class pcCreateRigAlt03LegsCode(object):
    def __init__(self, mirrorSel=2, lrSel=1,
                 cbTwists=True, cbAnkleTwist=True, cbSwitchSetup=True, cbGeo=True, cbHip=True,
                 bndJnt="JNT_BND_l_upperLeg", jntIKHipCheck="JNT_IK_hip", grpDNTTorsoCheck="GRP_DO_NOT_TOUCH_torso",
                 ctrlBodyCheck="CTRL_body", ctrlRootTransCheck="CTRL_rootTransform"):

        self.tgpMakeBC(mirrorSel, lrSel,
                       cbTwists, cbAnkleTwist, cbSwitchSetup, cbGeo, cbHip,
                       bndJnt, jntIKHipCheck, grpDNTTorsoCheck,
                       ctrlBodyCheck, ctrlRootTransCheck)

    def makeTwists(self, mkTwists, bndTwistee, bndTwister, ctrlFootSettings, ctrlIKFoot,
                   leftRight, fkikBlendName=None, *args):
        '''if leftRight == CRU.valLeft:
            setVal = 0
        else:
            setVal = 1
        # this was more for testing purposes
        mc.setAttr("{0}.fkik_blend".format(ctrlFootSettings), setVal)'''
        # colourTU and isLeft is for a special part of the code which lets us create a foot control
        numTwistsP1 = mkTwists + 1
        twists = mkTwists
        twistJnts = []
        twistExpression = ""
        breakVal = "_{0}".format(leftRight)

        ctrlTwistValAttr = bndTwistee.split("{0}".format(breakVal))[1]
        ctrlTwistValAttrName = "{0}Twist".format(ctrlTwistValAttr)
        mc.addAttr(ctrlFootSettings, longName=ctrlTwistValAttrName, at="float", k=True, min=0, max=1, dv=1)

        twistJntsSubgroup = []
        nextJnt = mc.listRelatives(bndTwistee, c=True, type="joint")[0]  # this is for the length

        # with the ankle, we can create the control

        nextJntXVal = mc.getAttr("{0}.tx".format(nextJnt))
        nextJntIncrement = nextJntXVal / (mkTwists)
        twistJntToDel = mc.duplicate(bndTwistee, po=True, n="ToDelete")  # duplicate the joint only

        # create the joint twists at the proper location

        # upper leg is positive, lower leg is negative
        '''
        # The calculation should look like this. The negative values may not be needed
        JNT_l_upperLegSeg1.rotateY = CTRL_l_lowerLeg.rotateX * 0.0* CTRL_l_foot.upperLegTwist;
        JNT_l_upperLegSeg2.rotateY = CTRL_l_lowerLeg.rotateX * 0.25* CTRL_l_foot.upperLegTwist;
        JNT_l_upperLegSeg3.rotateY = CTRL_l_lowerLeg.rotateX * 0.5* CTRL_l_foot.upperLegTwist;
        JNT_l_upperLegSeg4.rotateY = CTRL_l_lowerLeg.rotateX * 0.75* CTRL_l_foot.upperLegTwist;
        JNT_l_upperLegSeg5.rotateY = CTRL_l_lowerLeg.rotateX * 1* CTRL_l_foot.upperLegTwist;

        JNT_l_lowerLegSeg1.rotateY = JNT_l_ankleTwist.rotateY * -0.0* CTRL_l_foot.lowerLegTwist;
        JNT_l_lowerLegSeg2.rotateY = JNT_l_ankleTwist.rotateY * -0.25* CTRL_l_foot.lowerLegTwist;
        JNT_l_lowerLegSeg3.rotateY = JNT_l_ankleTwist.rotateY * -0.5* CTRL_l_foot.lowerLegTwist;
        JNT_l_lowerLegSeg4.rotateY = JNT_l_ankleTwist.rotateY * -0.75* CTRL_l_foot.lowerLegTwist;
        JNT_l_lowerLegSeg5.rotateY = JNT_l_ankleTwist.rotateY * -1* CTRL_l_foot.lowerLegTwist;
        '''

        twistInverse = 1.0 / (mkTwists)

        # names the multiplication node
        # we want it to divide it by the
        # gives us the lengths
        # creates scaling node setup
        multNodeSX = "{0}{1}{2}".format(leftRight, ctrlTwistValAttr, "ScaleTwists_MUL")
        mc.shadingNode("multiplyDivide", n=multNodeSX, au=True)
        mc.setAttr("{0}.operation".format(multNodeSX), 2)
        mc.connectAttr("{0}.translateX".format(nextJnt), "{0}.input1X".format(multNodeSX))
        mc.setAttr("{0}.input2X".format(multNodeSX), nextJntXVal)

        # gives us the rotations
        multNodeRX = "{0}{1}{2}".format(leftRight, ctrlTwistValAttr, "RotTwists_MUL")
        mc.shadingNode("multiplyDivide", n=multNodeRX, au=True)
        mc.setAttr("{0}.operation".format(multNodeRX), 1)
        # mc.connectAttr("{0}.tx".format(nextJnt), "{0}.input1X".format(multNodeRX))
        mc.setAttr("{0}.input2X".format(multNodeRX), twistInverse)

        # gives us the percent by which we twist
        multNodePercent = "{0}{1}{2}".format(leftRight, ctrlTwistValAttr,
                                             "PercentTwists_MUL")  # note: this is a test name
        mc.shadingNode("multiplyDivide", n=multNodePercent, au=True)
        mc.setAttr("{0}.operation".format(multNodePercent), 1)
        mc.connectAttr("{0}.{1}".format(ctrlFootSettings, ctrlTwistValAttrName), "{0}.input1X".format(multNodePercent))
        mc.connectAttr("{0}.outputX".format(multNodeRX), "{0}.input2X".format(multNodePercent))

        rotVal = "X"
        mv = 1

        useAnkleTwist = False
        if "ankleTwist" in bndTwister:
            useAnkleTwist = True

        if useAnkleTwist:
            mnRXinput1X = "{0}.rotate{1}".format(bndTwister, rotVal)
        else:
            mnRXinput1X = "{0}.rotate{1}".format(nextJnt, rotVal)

        mc.setAttr("{0}.input2X".format(multNodeRX), twistInverse * mv)
        mc.connectAttr(mnRXinput1X, "{0}.input1X".format(multNodeRX))

        twistJnts = []
        for x in range(numTwistsP1):
            valx = x + 1
            twistTemp = "{0}Seg{1}".format(bndTwistee, valx)

            # creates twists
            mc.duplicate(twistJntToDel, n=twistTemp)
            twistJnts.append(twistTemp)
            # we want to parent these under the leg or to the new bones
            if x == 0:
                mc.parent(twistTemp, bndTwistee)
            else:
                mc.parent(twistTemp, twistJnts[x - 1])
                # connect the values to the length of the leg. We can skip the first one since it's at the leg base
                mc.setAttr("{0}.translateX".format(twistTemp), nextJntIncrement)

                mc.connectAttr("{0}.outputX".format(multNodePercent), "{0}.rotateX".format(twistTemp))
            mc.connectAttr("{0}.outputX".format(multNodeSX), "{0}.scaleX".format(twistTemp))

        ####
        # if we're using ankleTwist, we want an average of the ctrlIKFoot and the ankleTwist
        # otherwise, we use the default

        mc.delete(twistJntToDel)
        return twistJnts

    def tgpCreateLimbFKIFList(self, jntsTemp, textToReplace="", textReplacement="", stripLastVal=0, deleteThis=True,
                              renameThis=True, addToEnd="", *args):
        jntsReturn = []
        # creates a set of values. Normally, we want this deleted, but we can also create a list from the values that simply don't include problematic node
        stripLastVal1 = stripLastVal * (-1)
        for i in range(len(jntsTemp)):
            toTest = jntsTemp[i]
            if mc.objectType(toTest) == "joint":
                if "Seg" in toTest:
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

    def makeBlendBasic(self, jntsSrc1, jntsSrc2, jntsTgt, ctrl, ctrlAttr, rotate, translate, override=False, *args):
        blndNodeTrans = []
        blndNodeRot = []
        # colour2 is at 0, colour1 is at 1

        for i in range(len(jntsSrc1)):
            name = jntsTgt[i]
            if translate:
                val = ".translate"
                blndNodeTrans.append(mc.shadingNode("blendColors", au=True, name="{0}_trans_BCN###".format(name)))
                mc.connectAttr(jntsSrc1[i] + val + "X", blndNodeTrans[i] + ".color2R")
                mc.connectAttr(jntsSrc1[i] + val + "Y", blndNodeTrans[i] + ".color2G")
                mc.connectAttr(jntsSrc1[i] + val + "Z", blndNodeTrans[i] + ".color2B")

                mc.connectAttr(jntsSrc2[i] + val + "X", blndNodeTrans[i] + ".color1R")
                mc.connectAttr(jntsSrc2[i] + val + "Y", blndNodeTrans[i] + ".color1G")
                mc.connectAttr(jntsSrc2[i] + val + "Z", blndNodeTrans[i] + ".color1B")

                mc.connectAttr(blndNodeTrans[i] + ".outputR", jntsTgt[i] + "{0}".format(val + "X"))
                mc.connectAttr(blndNodeTrans[i] + ".outputG", jntsTgt[i] + "{0}".format(val + "Y"))
                mc.connectAttr(blndNodeTrans[i] + ".outputB", jntsTgt[i] + "{0}".format(val + "Z"))
                blndName = "{0}.{1}".format(ctrl, ctrlAttr)
                mc.connectAttr(blndName, blndNodeTrans[i] + ".blender", f=True)

            if rotate:
                val = ".rotate"
                blndNodeRot.append(mc.shadingNode("blendColors", au=True, name="{0}_rot_BCN###".format(name)))

                mc.connectAttr(jntsSrc1[i] + val + "X", blndNodeRot[i] + ".color2R")
                mc.connectAttr(jntsSrc1[i] + val + "Y", blndNodeRot[i] + ".color2G")
                mc.connectAttr(jntsSrc1[i] + val + "Z", blndNodeRot[i] + ".color2B")

                mc.connectAttr(jntsSrc2[i] + val + "X", blndNodeRot[i] + ".color1R")
                mc.connectAttr(jntsSrc2[i] + val + "Y", blndNodeRot[i] + ".color1G")
                mc.connectAttr(jntsSrc2[i] + val + "Z", blndNodeRot[i] + ".color1B")

                '''mc.connectAttr(jntsSrc1[i] + val, blndNodeRot[i] + ".color2")
                mc.connectAttr(jntsSrc2[i] + val, blndNodeRot[i] + ".color1")'''

                mc.connectAttr(blndNodeRot[i] + ".outputR", jntsTgt[i] + "{0}".format(val + "X"))
                mc.connectAttr(blndNodeRot[i] + ".outputG", jntsTgt[i] + "{0}".format(val + "Y"))
                mc.connectAttr(blndNodeRot[i] + ".outputB", jntsTgt[i] + "{0}".format(val + "Z"))
                blndName = "{0}.{1}".format(ctrl, ctrlAttr)
                mc.connectAttr(blndName, blndNodeRot[i] + ".blender", f=True)

        return

    def renameIKFKLimbs(self, jntsTemp, textToReplace="", textReplacement="", stripLastVal=0, renameThis=True,
                        addToEnd="", *args):
        jntsReturn = []
        # creates a set of values. Normally, we want this deleted, but we can also create a list from the values that simply don't include problematic node
        stripLastVal1 = stripLastVal * (-1)
        for i in range(len(jntsTemp)):
            toTest = jntsTemp[i]
            if mc.objectType(toTest) == "joint":
                if stripLastVal1 == 0:
                    temp = toTest
                else:
                    temp = toTest[:stripLastVal1]
                toRename = temp.replace(textToReplace, textReplacement) + addToEnd  # strip off the last character
                if renameThis:
                    mc.rename(toTest, toRename)
                jntsReturn.append(toRename)
        return jntsReturn

    def createFKCtrls(self, fkJnts, colourTU, leftRight, *args):
        if leftRight == CRU.valLeft:
            imVal = 1
        else:
            imVal = -1
        set = False
        for i in range(len(fkJnts[:-1])):
            fkJnt = fkJnts[i]

            if "Leg" in fkJnt:
                if "End" in fkJnt:
                    pass
                else:

                    legChild = mc.listRelatives(fkJnt, typ="joint")[0]
                    legLen = mc.getAttr("{0}.translateX".format(legChild))
                    if i == 0:
                        sizeTU = 13
                    else:
                        sizeTU = 11
                    ctrl, ctrlShape = CRU.createCTRLsFKDirect(fkJnt, size=sizeTU, orientVal=(1, 0, 0),
                                                              colourTU=colourTU,
                                                              override=False)
                    fkJnts[i] = ctrl

                    mc.select(ctrlShape + ".cv[:]")

                    mc.move(legLen * 0.5, 0, -legLen * 0.05, r=True, os=True)
                    set = True
            else:
                if self.cbAnkleTwist:
                    footJnt = "ankleTwist"
                    orientVal = (0, 1, 0)
                    turn = True


                else:
                    footJnt = "foot"
                    orientVal = (0, 1, 0)
                    turn = False
                if footJnt in fkJnt:
                    ctrl, ctrlShape = CRU.createCTRLsFKDirect(fkJnt, size=sizeTU, orientVal=orientVal,
                                                              colourTU=colourTU, override=False)

                    mc.select(ctrlShape + ".cv[:]")
                    if turn:
                        mc.rotate(90, z=True, r=True, os=True)
                    else:
                        mc.rotate(90, z=True, r=True, ws=True)
                    set = True
                elif "ball" in fkJnt:

                    sizeTU = 7
                    ctrl, ctrlShape = CRU.createCTRLsFKDirect(fkJnt, size=sizeTU, orientVal=(imVal * 1, 0, 0),
                                                              colourTU=colourTU, override=False)

                    mc.select(ctrlShape + ".cv[5:7]")
                    mc.select(ctrlShape + ".cv[0:1]", add=True)
                    mc.scale(0, cp=True, z=True)
                    set = True
            if set:
                fkJnts[i] = ctrl
                set = False

        return fkJnts

    def makeFKStretch(self, fkJnts, *args):
        ctrlFKLengthKeyArray = []
        for i in range(len(fkJnts)):
            fkJnt = fkJnts[i]
            if "Leg" in fkJnt[-3:]:
                drivenAttr = "translateX"
                legChild = mc.listRelatives(fkJnt, typ="joint")[0]
                legLen = mc.getAttr("{0}.{1}".format(legChild, drivenAttr))
                length = "length"
                driverValue = 1
                mc.addAttr(fkJnt, longName=length, at="float", k=True, min=0, dv=1)
                CRU.setDriverDrivenValues(fkJnt, length, legChild, drivenAttr, drivenValue=legLen,
                                          driverValue=driverValue,
                                          modifyBoth="spline")
                CRU.setDriverDrivenValues(fkJnt, length, legChild, drivenAttr, drivenValue=0, driverValue=0,
                                          modifyBoth="spline")
                fkKey = "{0}_{1}".format(legChild, drivenAttr)
                ctrlFKLengthKeyArray.append(fkKey)
                mc.selectKey(cl=True)
                mc.selectKey(legChild, add=True, k=driverValue, attribute=drivenAttr)
                mc.setInfinity(poi='cycleRelative')

        return ctrlFKLengthKeyArray

    def createIKLegs(self, ikJnts, newLayerNameIK, leftRight, *args):
        if self.cbAnkleTwist:
            ikJntAnkle = [x for x in ikJnts if "ankleTwist" in x[-10:]][0]
            ikJntEnd = [x for x in ikJnts if "legEnd" in x[-6:]][0]
        ikJntFoot = [x for x in ikJnts if "foot" in x[-4:]][0]
        ikJntBall = [x for x in ikJnts if "ball" in x[-4:]][0]
        ikJntToe = [x for x in ikJnts if "toe" in x][0]

        if leftRight == CRU.valLeft:
            imVal = 1
        else:
            imVal = -1

        size = mc.getAttr("{0}.tx".format(ikJnts[-1]))
        ctrlName = "CTRL_{0}foot".format(leftRight)
        orientVal = (0, imVal * 1, 0)
        ctrlIKFoot = mc.circle(r=size, n=ctrlName, nr=orientVal, sections=10)[0]
        mc.matchTransform(ctrlIKFoot, ikJntAnkle, pos=True)

        # adjust size for foot
        mc.select("{0}.cv[:]".format(ctrlIKFoot))
        mc.move(0, moveY=True, ws=True)
        mc.move(2.6, moveZ=True, r=True)

        mc.scale(.9, xz=True)
        mc.scale(1.2, z=True)

        mc.select("{0}.cv[3:8]".format(ctrlIKFoot))
        mc.move(imVal * size * 1.4, moveZ=True, r=True)

        mc.select("{0}.cv[3]".format(ctrlIKFoot))
        mc.move(size * .1, moveX=True, r=True)

        mc.select("{0}.cv[:]".format(ctrlIKFoot))
        mc.move(-size * .1, moveX=True,
                r=True)  # this may be a point you need to personalize for the rig more than usual

        mc.makeIdentity(ctrlIKFoot, apply=True)
        mc.select(cl=True)

        CRU.layerEdit(ctrlIKFoot, newLayerName=newLayerNameIK)
        CRU.changeRotateOrder(ctrlIKFoot, "ZXY")

        if self.cbAnkleTwist:
            ikJntFootUse = ikJntEnd
            ikJntFootUseForBall = ikJntAnkle
        else:
            ikJntFootUse = ikJntFoot
            ikJntFootUseForBall = ikJntFoot
        jntsToUseFoot = [ikJnts[0], ikJntFootUse]
        ikSolver = "ikRPsolver"

        ikLegs = self.createIKVal(jntsToUseFoot, leftRight, "foot", ikSolver, )
        mc.parent(ikLegs[0], ctrlIKFoot)

        jntsToUseBall = [ikJntFootUseForBall, ikJntBall]
        ikBall = self.createIKVal(jntsToUseBall, leftRight, "ball", ikSolver, )
        mc.parent(ikBall[0], ctrlIKFoot)

        jntsToUseToe = [ikJntBall, ikJntToe]
        ikToe = self.createIKVal(jntsToUseToe, leftRight, "toe", ikSolver, )
        mc.parent(ikToe[0], ctrlIKFoot)

        return ctrlIKFoot, ikLegs, ikBall, ikToe

    def createIKVal(self, ikJntsToUse, leftRight, ikSuffix, ikSolver, *args):
        ikSide = leftRight + ikSuffix

        ikLegName = "HDL_" + ikSide
        effLegName = "EFF_" + ikSide
        ikLegs = mc.ikHandle(n=ikLegName, sj=ikJntsToUse[0], ee=ikJntsToUse[-1], sol=ikSolver)
        mc.rename(ikLegs[1], effLegName)

        # we are going to hide this eventually anyways
        mc.setAttr("{0}.v".format(ikLegName), False)
        mc.setAttr("{0}.v".format(effLegName), False)

        return ikLegs

    def makeIKStretch(self, ikJnts, leftRight, ctrlIKFoot, *args):
        if leftRight == CRU.valLeft:
            # need to make adjustments for the values making a mirror
            imVal = 1
        else:
            imVal = -1
        # creates locators that measure distance for the leg
        if self.cbAnkleTwist:
            ikJntFoot = [x for x in ikJnts if "legEnd" in x[-6:]][0]
        else:
            ikJntFoot = [x for x in ikJnts if "foot" in x[-4:]][0]

        # create the starting space locator for the distance node
        locIKLegLenStart = "LOC_IK_{0}leg_lengthStart".format(leftRight)
        mc.spaceLocator(p=(0, 0, 0), name=locIKLegLenStart)

        mc.matchTransform(locIKLegLenStart, ikJnts[0], pos=True)
        locIKLegLenEnd = "LOC_IK_{0}leg_lengthEnd".format(leftRight)
        mc.spaceLocator(p=(0, 0, 0), name=locIKLegLenEnd)

        mc.matchTransform(locIKLegLenEnd, ikJntFoot, pos=True)

        driverAttr = "distance"
        disIKLeg = "DIST_IK_{0}leg_length".format(leftRight)
        disIKLegShape = CRU.createDistanceDimensionNode(locIKLegLenStart, locIKLegLenEnd, disIKLeg, toHide=True)

        mc.parent(locIKLegLenEnd, ctrlIKFoot)

        driverLen = mc.getAttr("{0}.{1}".format(disIKLegShape, driverAttr)) * imVal

        upperLegLen = mc.getAttr("{0}.translateX".format(ikJnts[1]))
        lowerLegLen = mc.getAttr("{0}.translateX".format(ikJntFoot))
        sumLegLen = (upperLegLen + lowerLegLen) * imVal

        drivenAttr = "translateX"

        ctrlIKLengthKeyArray = []

        # uses the total length to drive the length of the upper leg and  extrapolates it to infinity
        CRU.setDriverDrivenValues(disIKLegShape, driverAttr, ikJnts[1], drivenAttr, sumLegLen, upperLegLen,
                                  modifyBoth="spline")
        CRU.setDriverDrivenValues(disIKLegShape, driverAttr, ikJnts[1], drivenAttr, sumLegLen * 2, upperLegLen * 2,
                                  modifyBoth="spline")
        mc.selectKey(cl=True)
        mc.selectKey(ikJnts[1], add=True, k=sumLegLen * 2, attribute=drivenAttr)
        mc.setInfinity(poi='cycleRelative')
        ctrlIKLengthKeyArray.append("{0}_{1}".format(ikJnts[1], drivenAttr))

        # uses the total length to drive the length of the lower leg and  extrapolates it to infinity
        CRU.setDriverDrivenValues(disIKLegShape, driverAttr, ikJntFoot, drivenAttr, sumLegLen, lowerLegLen,
                                  modifyBoth="spline")
        CRU.setDriverDrivenValues(disIKLegShape, driverAttr, ikJntFoot, drivenAttr, sumLegLen * 2, lowerLegLen * 2,
                                  modifyBoth="spline")

        mc.selectKey(cl=True)
        mc.selectKey(ikJntFoot, add=True, k=sumLegLen * 2, attribute=drivenAttr)
        mc.setInfinity(poi='cycleRelative')
        ctrlIKLengthKeyArray.append("{0}_{1}".format(ikJntFoot, drivenAttr))

        return locIKLegLenStart, locIKLegLenEnd, disIKLeg, disIKLegShape, ctrlIKLengthKeyArray

    def createDistanceDimensionNode(self, startLoc, endLoc, lenNodeName, toHide=False):
        distDimShape = mc.distanceDimension(sp=(0, 0, 0), ep=(0, 0, 0))
        mc.connectAttr("{0}.worldPosition".format(startLoc), "{0}.startPoint".format(distDimShape), f=True)
        mc.connectAttr("{0}.worldPosition".format(endLoc), "{0}.endPoint".format(distDimShape), f=True)
        distDimParent = mc.listRelatives(distDimShape, p=True)
        mc.rename(distDimParent, lenNodeName)
        lenNodeNameShape = mc.listRelatives(lenNodeName, s=True)[0]
        if toHide:
            mc.setAttr("{0}.visibility".format(startLoc), False)
            mc.setAttr("{0}.visibility".format(endLoc), False)
            mc.setAttr("{0}.visibility".format(lenNodeName), False)
        return lenNodeNameShape

    def createNoFlipIKLeg(self, ikJnts, ctrlIKFoot, ikLegs, leftRight, *args):
        if leftRight == CRU.valLeft:
            imVal = 1
        else:
            imVal = -1

        locKnee = "LOC_{0}knee".format(leftRight)
        mc.spaceLocator(p=(0, 0, 0), name=locKnee)
        todelete = mc.pointConstraint(ikJnts[1], locKnee)
        mc.delete(todelete)
        legLen = mc.getAttr("{0}.translateX".format(ikJnts[1])) * imVal
        mc.move(legLen, locKnee, r=True, moveZ=True)
        mc.makeIdentity(locKnee, apply=True)

        mc.poleVectorConstraint(locKnee, ikLegs[0])

        # now we make it so that we don't flip the knee
        # point snap the loc_knee to the JNT_IK_foot (or CTRL_foot since they're the same location)
        todelete = mc.pointConstraint(ctrlIKFoot, locKnee)
        mc.move(legLen, locKnee, r=True, moveX=True)
        # the leftRight mirroring affect the twist value determines
        mc.setAttr("{0}.twist".format(ikLegs[0]), 90)
        mc.delete(todelete)

        mc.parent(locKnee, ctrlIKFoot)

        grpNoFlipKnee = "GRP_noFlip_{0}knee".format(leftRight)

        mc.group(em=True, name=grpNoFlipKnee, w=True)
        todelete = mc.pointConstraint(ctrlIKFoot, grpNoFlipKnee)
        mc.delete(todelete)

        mc.parent(grpNoFlipKnee, ctrlIKFoot)
        mc.makeIdentity(grpNoFlipKnee, apply=True)
        mc.parent(locKnee, grpNoFlipKnee)
        mc.addAttr(ctrlIKFoot, longName="blank", niceName="-----", at="enum", en="____", k=True)

        kneeTwist = "kneeTwist"
        mc.addAttr(ctrlIKFoot, longName=kneeTwist, at="float", k=True)
        mc.connectAttr("{0}.{1}".format(ctrlIKFoot, kneeTwist), "{0}.rotateY".format(grpNoFlipKnee))
        mc.setAttr("{0}.v".format(locKnee), False)
        return grpNoFlipKnee, locKnee

    def createDualKnee(self, ikJnts, ctrlIKFoot, ikLegs, grpNoFlipKnee, locIKLegLenEnd, locIKLegLenStart,
                       ctrlFootSettings, leftRight, newLayerNameIK, *args):
        if leftRight == CRU.valLeft:
            imVal = 1
        else:
            imVal = -1

        # get the noFlip values
        dupsNoFlip = mc.duplicate(ctrlIKFoot, ic=True, un=True, rc=True)
        leftRightVal = "_{0}".format(leftRight)

        mc.delete(ikLegs[0], locIKLegLenStart, locIKLegLenEnd, grpNoFlipKnee)

        dupsTrackNoFlip, dupsMoveNoFlip, returnLegNoFlip, animCrvNoFlip, locStartArrayNoFlip, lenArrayNoFlip = self.duplicateNoFlipOrPV(
            locIKLegLenEnd, grpNoFlipKnee,
            ikLegs, ctrlIKFoot,
            dupsNoFlip, leftRightVal,
            prefix="noFlip")
        lenNoFlip = lenArrayNoFlip[0]
        locStartNoFlip = locStartArrayNoFlip[0]

        # the duplicated noFlip group should have the same name as before
        kneeTwist = "kneeTwist"
        mc.connectAttr("{0}.{1}".format(ctrlIKFoot, kneeTwist), "{0}.rotateY".format(grpNoFlipKnee))

        # get the pole vector values
        # This is a little more complicated, so we want to delete the extra IK joints produced
        dupsPV = mc.duplicate(ctrlIKFoot, ic=True, un=True, rc=True)

        dupsPVToDelete = [x for x in dupsPV if x[:-1] in ikJnts[0]]

        # Prune the base IK duplicate
        dupsPV = [x for x in dupsPV if x[:-1] not in ikJnts]
        # get the nodes we will move
        dupsPVHDL = [x for x in dupsMoveNoFlip if "HDL" in x]
        dupsPVLocEnd = [x for x in dupsMoveNoFlip if "lengthEnd" in x][0]
        dupsTrackPV, dupsMovePV, returnLegPV, animCrvPV, locStartArrayPV, lenArrayPV = self.duplicateNoFlipOrPV(
            dupsPVLocEnd, grpNoFlipKnee,
            dupsPVHDL,
            ctrlIKFoot,
            dupsPV, leftRightVal,
            prefix="pv",
            altPrefixReplace="noFlip", )

        lenPV = lenArrayPV[0]
        locStartPV = locStartArrayPV[0]

        mc.delete(dupsPVToDelete)
        dupsPVgrpLoc = [x for x in dupsMovePV if "GRP" in x]
        locPVKnee = mc.listRelatives(dupsPVgrpLoc)[0]
        mc.parent(locPVKnee, w=True)
        mc.delete(dupsPVgrpLoc)
        dupsPVHDL = [x for x in dupsMovePV if "HDL" in x][0]
        mc.setAttr("{0}.twist".format(dupsPVHDL), 0)
        mc.move(0, 0, 0, locPVKnee, os=True)

        # blend the auto/manual leg control
        autoManualLN = "autoManualKneeBlend"
        autoManualNiceName = "Auto (noFlip) / Manual (PV) Knee Blend"
        # note: we set DV to 0.5 for testing purposes
        mc.addAttr(ctrlIKFoot, longName=autoManualLN, niceName=autoManualNiceName, at="float", k=True,
                   min=0, max=1, dv=1)

        ikJntsPV = mc.listRelatives(returnLegPV, type="joint", ad=True)
        ikJntsPV.append(returnLegPV)
        ikJntsPV.reverse()

        ikJntsNoFlip = mc.listRelatives(returnLegNoFlip, type="joint", ad=True)
        ikJntsNoFlip.append(returnLegNoFlip)
        ikJntsNoFlip.reverse()

        self.makeBlendBasic(ikJntsNoFlip, ikJntsPV, ikJnts, ctrlIKFoot, autoManualLN, rotate=True,
                            translate=True)

        # hide values
        mc.setAttr("{0}.v".format(ikJntsPV[0]), False)
        mc.setAttr("{0}.v".format(ikJntsNoFlip[0]), False)
        # note: I am keeping this visible for testing purposes. If it is not visible, I am not testing it.
        mc.setAttr("{0}.v".format(ikJnts[0]), False)

        # create a pyramid
        boxDimensionsLWH = [2, 2, 8]
        x = boxDimensionsLWH[0]
        y = boxDimensionsLWH[1]
        z = boxDimensionsLWH[2]

        toPass = [(0, 0, z),
                  (-x, y, 0), (-x, -y, 0), (0, 0, z),
                  (x, y, 0), (x, -y, 0), (0, 0, z),
                  (x, y, 0), (x, -y, 0), (-x, -y, 0), (-x, y, 0), (x, y, 0), ]
        ctrlKnee = "CTRL_{0}knee".format(leftRight)
        try:
            ctrl = mc.curve(ctrlKnee, r=True, d=1, p=toPass, )
        except:
            ctrl = mc.curve(name=ctrlKnee, d=1, p=toPass, )
            # ctrl = mc.curve(name=ctrlName, p=toPass, d=1)
        todelete = mc.pointConstraint(locPVKnee, ctrlKnee)
        mc.delete(todelete)
        mc.makeIdentity(ctrlKnee, a=True)
        mc.parent(locPVKnee, ctrlKnee)
        CRU.layerEdit(ctrlKnee, newLayerName=newLayerNameIK)

        return ikJntsPV, ikJntsNoFlip, ctrlKnee, animCrvPV, animCrvNoFlip, autoManualLN, locStartNoFlip, lenNoFlip, locStartPV, lenPV

    def duplicateNoFlipOrPV(self, locIKLegLenEnd, grpNoFlipKnee, ikLegs, ctrlIKFoot, dups, leftRightVal, prefix,
                            altPrefixReplace=None, *args):
        dupsTrack = []
        dupsMove = []
        checkToMove = [locIKLegLenEnd, grpNoFlipKnee, ikLegs[0]]
        toDelete = []
        animationCurves = []
        locStartArray = []
        lenArray = []
        for i in range(len(dups)):

            if leftRightVal in dups[i]:
                # create a name to replace the renamed value, with the last character removed
                if "_{0}_".format(prefix) in dups[i]:
                    dupReplace = dups[i][:-1]
                else:
                    dupReplace = dups[i][:-1].replace(leftRightVal, "_{0}{1}".format(prefix, leftRightVal))
                # when we do this, we might do this a second time, so we want to eliminate the other duplicates
                if altPrefixReplace is not None:
                    dupReplace = dupReplace.replace("_{0}".format(altPrefixReplace), "")
                mc.rename(dups[i], dupReplace)
                if dups[i][:-1] in checkToMove:
                    # save the values to move to ctrlFoot
                    dupsMove.append(dupReplace)
                dups[i] = dupReplace
                dupsTrack.append(dupReplace)

                if "CTRL" in dupReplace:
                    toDelete.append(dupReplace)
                if self.cbAnkleTwist:
                    if "ankleTwist" in dupReplace:
                        toDelete.append(dupReplace)
                else:
                    if "ball" in dupReplace:
                        toDelete.append(dupReplace)

                if "upperLeg" in dupReplace:
                    returnLeg = dupReplace
                if "_translate" in dupReplace:
                    animationCurves.append(dupReplace)
                if "lengthStart" in dupReplace:
                    locStartArray.append(dupReplace)
                if "DIST_" in dupReplace[:5]:
                    lenArray.append(dupReplace)

        mc.parent(dupsMove, ctrlIKFoot)
        mc.delete(toDelete)
        return dupsTrack, dupsMove, returnLeg, animationCurves, locStartArray, lenArray

    def createSnappableKnee(self, ikJntsPV, ctrlKnee, leftRight, ctrlIKFoot, animCrvPV, *args):
        if leftRight == CRU.valLeft:
            imVal = 1
        else:
            imVal = -1

        toHide = []
        # create a thigh to knee distance locator
        locSnapUpperToKneeStart = "LOC_{0}upperLeg_to_kneeStart".format(leftRight)
        mc.spaceLocator(p=(0, 0, 0), name=locSnapUpperToKneeStart)
        todelete = mc.pointConstraint(ikJntsPV[0], locSnapUpperToKneeStart)
        mc.delete(todelete)

        locSnapUpperToKneeEnd = "LOC_{0}upperLeg_to_kneeEnd".format(leftRight)
        mc.spaceLocator(p=(0, 0, 0), name=locSnapUpperToKneeEnd)
        todelete = mc.pointConstraint(ctrlKnee, locSnapUpperToKneeEnd)
        mc.delete(todelete)

        disSnapUpper = "DIST_{0}upperLeg_to_knee_length".format(leftRight)
        disSnapUpperShape = CRU.createDistanceDimensionNode(locSnapUpperToKneeStart, locSnapUpperToKneeEnd,
                                                            disSnapUpper)
        toHide.append(locSnapUpperToKneeEnd)
        toHide.append(locSnapUpperToKneeStart)
        toHide.append(disSnapUpper)

        ##################################
        # create a knee to foot distance locator
        locSnapKneeToFootStart = "LOC_{0}knee_to_footStart".format(leftRight)
        mc.spaceLocator(p=(0, 0, 0), name=locSnapKneeToFootStart)
        todelete = mc.pointConstraint(ctrlKnee, locSnapKneeToFootStart)
        mc.delete(todelete)

        locSnapKneeToFootEnd = "LOC_{0}knee_to_footEnd".format(leftRight)
        mc.spaceLocator(p=(0, 0, 0), name=locSnapKneeToFootEnd)
        todelete = mc.pointConstraint(ikJntsPV[-1], locSnapKneeToFootEnd)
        mc.delete(todelete)

        disSnapLower = "DIST_{0}knee_to_foot_length".format(leftRight)
        disSnapLowerShape = CRU.createDistanceDimensionNode(locSnapKneeToFootStart, locSnapKneeToFootEnd, disSnapLower)
        toHide.append(locSnapKneeToFootStart)
        toHide.append(locSnapKneeToFootEnd)
        toHide.append(disSnapLower)
        ##################################
        mc.parent(locSnapKneeToFootStart, locSnapUpperToKneeEnd, ctrlKnee)
        mc.parent(locSnapKneeToFootEnd, ctrlIKFoot)

        # snappable knee
        # create custom control on knee
        longName = "kneeSnap"
        # note: set dv to 0.5 for testing purposes
        mc.addAttr(ctrlKnee, longName=longName, at="float", k=True, min=0, max=1, dv=0)
        blndNdUpperStretchChoice = "{0}upperLeg_pv_stretchChoice".format(leftRight)
        src1Upper = "{0}.distance".format(disSnapUpperShape)
        src2Upper = "{0}.output".format(animCrvPV[0])
        tgtUpper = "{0}.translateX".format(ikJntsPV[1])

        blndNdLowerStretchChoice = "{0}lowerLeg_pv_stretchChoice".format(leftRight)
        src1Lower = "{0}.distance".format(disSnapLowerShape)
        src2Lower = "{0}.output".format(animCrvPV[-1])
        tgtLower = "{0}.translateX".format(ikJntsPV[-1])

        self.makeBlendStretch(src1Upper, src2Upper, tgtUpper, ctrlKnee, longName, blndNdUpperStretchChoice, imVal,
                              leftRight)

        self.makeBlendStretch(src1Lower, src2Lower, tgtLower, ctrlKnee, longName, blndNdLowerStretchChoice, imVal)

        for i in range(len(toHide)):
            mc.setAttr("{0}.v".format(toHide[i]), False)
        return locSnapUpperToKneeStart, disSnapUpper, disSnapLower, blndNdUpperStretchChoice, blndNdLowerStretchChoice

    def makeBlendStretch(self, src1, src2, tgt, ctrl, ctrlAttr, blendNodeName, mult, *args):
        multValName = "{0}_MUL".format(blendNodeName)
        mc.shadingNode("multiplyDivide", n=multValName, au=True)
        mc.setAttr("{0}.operation".format(multValName), 1)
        mc.setAttr("{0}.input2X".format(multValName), mult)

        # this lets us invert the numbers when we need to, like when we are working with the right side vs the left side
        mc.connectAttr(src1, multValName + ".input1X")

        mc.shadingNode("blendColors", au=True, name=blendNodeName)
        mc.connectAttr("{0}.outputX".format(multValName), blendNodeName + ".color1R")
        mc.connectAttr(src2, blendNodeName + ".color2R")
        mc.connectAttr(blendNodeName + ".outputR", tgt, f=True)
        blndName = "{0}.{1}".format(ctrl, ctrlAttr)
        mc.connectAttr(blndName, blendNodeName + ".blender", f=True)

        return

    def createNonUniformStretchNoFlip(self, ctrlIKFoot, leftRight, animCrvNoFlip, ikJntsNoFlip, *args):
        akUpperLegLen = "autoKneeUpperLegLength"
        mc.addAttr(ctrlIKFoot, longName=akUpperLegLen, at="float", k=True, min=0, dv=1)
        akLowerLegLen = "autoKneeLowerLegLength"
        mc.addAttr(ctrlIKFoot, longName=akLowerLegLen, at="float", k=True, min=0, dv=1)
        multNoFlipScaleUpperLeg = "{0}upperLeg_noFlipScale_MULT".format(leftRight)
        multNoFlipScaleLowerLeg = "{0}lowerLeg_noFlipScale_MULT".format(leftRight)

        mc.shadingNode("multiplyDivide", n=multNoFlipScaleUpperLeg, au=True)
        mc.shadingNode("multiplyDivide", n=multNoFlipScaleLowerLeg, au=True)

        # Connect the CTRL_l_foot.autoKneeThighLength to l_upperLeg_noFlipScale_MULT.input1X
        # Connect the translateXanimation.output to l_upperLeg_noFlipScale_MULT.input2X
        # Connect the l_upperLeg_noFlipScale_MULT.outputX into the JNT_IK_noFlip_l_lowerLeg.TranslateX
        mc.connectAttr("{0}.{1}".format(ctrlIKFoot, akUpperLegLen), "{0}.input1X".format(multNoFlipScaleUpperLeg))
        mc.connectAttr("{0}.output".format(animCrvNoFlip[0]), "{0}.input2X".format(multNoFlipScaleUpperLeg))
        mc.connectAttr("{0}.outputX".format(multNoFlipScaleUpperLeg),
                       "{0}.translateX".format(ikJntsNoFlip[1]), f=True)

        # repeat for the lower leg
        mc.connectAttr("{0}.{1}".format(ctrlIKFoot, akLowerLegLen), "{0}.input1X".format(multNoFlipScaleLowerLeg))
        mc.connectAttr("{0}.output".format(animCrvNoFlip[-1]), "{0}.input2X".format(multNoFlipScaleLowerLeg))
        mc.connectAttr("{0}.outputX".format(multNoFlipScaleLowerLeg),
                       "{0}.translateX".format(ikJntsNoFlip[-1]), f=True)

    def toggleFKIKVisibility(self, ctrlFootSettings, ctrlIKFoot, ctrlKnee, fkJnts, fkikBlendName, autoManualLN,
                             leftRight, *args):
        # connect the visibility of the controllers
        fkVis = "FK_visibility"
        ikVis = "IK_visibility"
        kneeVis = "knee_visibility"

        mc.addAttr(ctrlFootSettings, longName=fkVis, at="bool", k=True)
        mc.addAttr(ctrlFootSettings, longName=ikVis, at="bool", k=True)
        mc.addAttr(ctrlFootSettings, longName=kneeVis, at="bool", k=True)
        mc.connectAttr("{0}.{1}".format(ctrlFootSettings, fkVis), "{0}.visibility".format(fkJnts[0]))
        mc.connectAttr("{0}.{1}".format(ctrlFootSettings, ikVis), "{0}.visibility".format(ctrlIKFoot))
        mc.connectAttr("{0}.{1}".format(ctrlFootSettings, kneeVis), "{0}.visibility".format(ctrlKnee))

        visMin = 0.001
        tangentToUse = ["linear", "step"]
        # set the FK
        CRU.setDriverDrivenValues(ctrlFootSettings, fkikBlendName, ctrlFootSettings, fkVis, drivenValue=True,
                                  driverValue=0, modifyInOut=tangentToUse)
        CRU.setDriverDrivenValues(ctrlFootSettings, fkikBlendName, ctrlFootSettings, fkVis, drivenValue=True,
                                  driverValue=1 - visMin, modifyInOut=tangentToUse)
        CRU.setDriverDrivenValues(ctrlFootSettings, fkikBlendName, ctrlFootSettings, fkVis, drivenValue=False,
                                  driverValue=1, modifyInOut=tangentToUse)

        # set the IK
        CRU.setDriverDrivenValues(ctrlFootSettings, fkikBlendName, ctrlFootSettings, ikVis, drivenValue=False,
                                  driverValue=0, modifyInOut=tangentToUse)
        CRU.setDriverDrivenValues(ctrlFootSettings, fkikBlendName, ctrlFootSettings, ikVis, drivenValue=True,
                                  driverValue=visMin, modifyInOut=tangentToUse)
        CRU.setDriverDrivenValues(ctrlFootSettings, fkikBlendName, ctrlFootSettings, ikVis, drivenValue=True,
                                  driverValue=1, modifyInOut=tangentToUse)

        # set the knee
        CRU.setDriverDrivenValues(ctrlIKFoot, autoManualLN, ctrlFootSettings, kneeVis, drivenValue=False,
                                  driverValue=0, modifyInOut=tangentToUse)
        CRU.setDriverDrivenValues(ctrlIKFoot, autoManualLN, ctrlFootSettings, kneeVis, drivenValue=True,
                                  driverValue=visMin, modifyInOut=tangentToUse)
        CRU.setDriverDrivenValues(ctrlIKFoot, autoManualLN, ctrlFootSettings, kneeVis, drivenValue=True,
                                  driverValue=1, modifyInOut=tangentToUse)

        grpKnee = "GRP_{0}knee".format(leftRight)
        mc.group(n=grpKnee, w=True, em=True)
        mc.parent(ctrlKnee, grpKnee)
        # knee shouldn't appear when FK is only on
        vis = "visibility"
        CRU.setDriverDrivenValues(ctrlFootSettings, fkikBlendName, grpKnee, vis, drivenValue=False,
                                  driverValue=0, modifyInOut=tangentToUse)
        CRU.setDriverDrivenValues(ctrlFootSettings, fkikBlendName, grpKnee, vis, drivenValue=True,
                                  driverValue=visMin, modifyInOut=tangentToUse)
        CRU.setDriverDrivenValues(ctrlFootSettings, fkikBlendName, grpKnee, vis, drivenValue=True,
                                  driverValue=1, modifyInOut=tangentToUse)

        return grpKnee

    def organizeLeg(self, grpKnee,
                    bndJnts, ikJnts, ikJntsPV, ikJntsNoFlip,
                    fkJnts, ctrlIKFoot,
                    locStartNoFlip, lenNoFlip, locStartPV, lenPV, locSnapUpperToKneeStart,
                    disSnapUpper, disSnapLower,
                    leftRight,
                    ctrlRootTrans, *args):
        # move the objects into a grp_leg
        grpLeg = "GRP_{0}leg".format(leftRight)
        mc.group(n=grpLeg, w=True, em=True)
        mc.parent(grpLeg, ctrlRootTrans)

        # create an BND Const group
        grpBNDConst = "GRP_BNDConst_{0}leg".format(leftRight)
        mc.group(n=grpBNDConst, w=True, em=True)
        todelete = mc.pointConstraint(bndJnts[0], grpBNDConst)
        mc.delete(todelete)
        mc.makeIdentity(grpBNDConst, a=True)
        mc.parent(bndJnts[0], grpBNDConst)

        # create an IK Const group
        grpIKConst = "GRP_IKConst_{0}leg".format(leftRight)
        mc.group(n=grpIKConst, w=True, em=True)
        todelete = mc.pointConstraint(bndJnts[0], grpIKConst)
        mc.delete(todelete)
        mc.makeIdentity(grpIKConst, a=True)
        mc.parent(locStartPV, locStartNoFlip, ikJnts[0], ikJntsNoFlip[0], ikJntsPV[0], locSnapUpperToKneeStart,
                  grpIKConst)

        # I create this earlier than my notes for simplicity's sake
        grpFKConst = "GRP_FKConst_{0}leg".format(leftRight)
        mc.group(n=grpFKConst, w=True, em=True)
        todelete = mc.pointConstraint(bndJnts[0], grpFKConst)
        mc.delete(todelete)
        mc.makeIdentity(grpFKConst, a=True)
        mc.parent(fkJnts[0], grpFKConst)

        # create a DO_NOT_TOUCH group
        grpDNTLeg = "GRP_DO_NOT_TOUCH_{0}leg".format(leftRight)
        mc.group(n=grpDNTLeg, w=True, em=True)

        mc.parent(lenNoFlip, lenPV, grpBNDConst, grpIKConst,
                  disSnapUpper, disSnapLower, grpDNTLeg)

        # parent the knee, fkConstr group and DNT under the grpLeg
        mc.parent(grpKnee, ctrlIKFoot, grpFKConst, grpDNTLeg, grpLeg)

        return grpIKConst, grpBNDConst, grpFKConst

    def hipSetup(self, grpBNDConst, grpIKConst, grpFKConst,
                 jntIKHip,
                 grpDNTTorso, ctrlRootTrans,
                 ctrlFootSettings,
                 leftRight, *args):
        locHipSpace = "LOC_hipSpace_{0}leg".format(leftRight)
        mc.spaceLocator(p=(0, 0, 0), name=locHipSpace)
        todelete = mc.pointConstraint(grpBNDConst, locHipSpace)
        mc.delete(todelete)

        mc.pointConstraint(locHipSpace, grpBNDConst)
        mc.pointConstraint(locHipSpace, grpIKConst)
        mc.pointConstraint(locHipSpace, grpFKConst)

        if self.cbHip:
            locArray = []

            # Set up the hip space stuff
            locBodySpace = "LOC_bodySpace_{0}leg".format(leftRight)
            locRootSpace = "LOC_rootSpace_{0}leg".format(leftRight)

            locArray = [locHipSpace, locBodySpace, locRootSpace]
            mc.duplicate(locHipSpace, n=locBodySpace)
            mc.duplicate(locHipSpace, n=locRootSpace)

            mc.parent(locHipSpace, jntIKHip)
            mc.parent(locBodySpace, grpDNTTorso)
            mc.parent(locRootSpace, ctrlRootTrans)

            orntCnstrFK = mc.orientConstraint(locHipSpace, locBodySpace, locRootSpace, grpFKConst)[0]
            orntCnstrBND = mc.orientConstraint(locHipSpace, locBodySpace, locRootSpace, grpBNDConst)[0]

            fkRotSpace = "FK_rotationSpace"
            enumVals = "hip:upperBody:root"
            mc.addAttr(ctrlFootSettings, longName=fkRotSpace, at="enum", k=True, en=enumVals)

            self.setOrientLegDriver(ctrlFootSettings, fkRotSpace, orntCnstrFK, locArray)
            self.setOrientLegDriver(ctrlFootSettings, fkRotSpace, orntCnstrBND, locArray)

        return

    def setOrientLegDriver(self, ctrlLimb, enumName, driven, locArray, *args):
        rangeVal = len(locArray)
        rangeValNeg = rangeVal * -1
        w0w1Attr = mc.listAttr(driven)[rangeValNeg:]

        for i in range(len(w0w1Attr)):
            # set the driven key to 1 and the undriven keys to 0

            CRU.setDriverDrivenValues(ctrlLimb, enumName, driven, w0w1Attr[i], i,
                                      1)
            for i2 in range(len(locArray)):
                if i2 != i:
                    # need to have the second to last value be i, not i2
                    CRU.setDriverDrivenValues(ctrlLimb, enumName, driven,
                                              w0w1Attr[i2], i, 0)

        for i in range(len(locArray)):
            # unlocks then locks
            check = mc.getAttr("{0}.visibility".format(locArray[i]), l=True)
            if not check:
                mc.setAttr("{0}.visibility".format(locArray[i]), False)
                CRU.lockHideCtrls(locArray[i], scale=True, visibility=True)

    def fkHipTwistFix(self, grpBNDConst, ctrlFootSettings, fkikBlendName, leftRight, *args):
        blndOrntChoice = "{0}leg_BNDOrientChoice".format(leftRight)
        mc.shadingNode("blendColors", au=True, name=blndOrntChoice)
        orntConst = mc.listRelatives(grpBNDConst, type="orientConstraint")[0]
        mc.connectAttr("{0}.constraintRotateX".format(orntConst), "{0}.color2R".format(blndOrntChoice))
        mc.connectAttr("{0}.constraintRotateY".format(orntConst), "{0}.color2G".format(blndOrntChoice))
        mc.connectAttr("{0}.constraintRotateZ".format(orntConst), "{0}.color2B".format(blndOrntChoice))
        mc.setAttr("{0}.color1R".format(blndOrntChoice), 0)
        mc.setAttr("{0}.color1G".format(blndOrntChoice), 0)
        mc.setAttr("{0}.color1B".format(blndOrntChoice), 0)

        mc.connectAttr("{0}.{1}".format(ctrlFootSettings, fkikBlendName), "{0}.blender".format(blndOrntChoice))

        mc.connectAttr("{0}.outputR".format(blndOrntChoice), "{0}.rotateX".format(grpBNDConst), f=True)
        mc.connectAttr("{0}.outputG".format(blndOrntChoice), "{0}.rotateY".format(grpBNDConst), f=True)
        mc.connectAttr("{0}.outputB".format(blndOrntChoice), "{0}.rotateZ".format(grpBNDConst), f=True)

        return

    def legIKScaleFix(self, lenPV, lenNoFlip,
                      animCrvPV, animCrvNoFlip,
                      ctrlRootTrans,
                      disSnapUpper, disSnapLower,
                      blndNdUpperStretchChoice, blndNdLowerStretchChoice,
                      leftRight, *args):
        if leftRight == CRU.valLeft:
            imVal = 1
        else:
            imVal = -1

        gsLegNoFlipNormalizeDiv = "globalScale_{0}leg_noFlipNormalize_DIV".format(leftRight)
        gsLegPVNormalizeDiv = "globalScale_{0}leg_pvNormalize_DIV".format(leftRight)
        lenNoFlipShape = mc.listRelatives(lenNoFlip, s=True)[0]
        lenPVShape = mc.listRelatives(lenPV, s=True)[0]

        mc.shadingNode("multiplyDivide", n=gsLegNoFlipNormalizeDiv, au=True)
        mc.shadingNode("multiplyDivide", n=gsLegPVNormalizeDiv, au=True)

        mc.setAttr("{0}.operation".format(gsLegNoFlipNormalizeDiv), 2)
        mc.setAttr("{0}.operation".format(gsLegPVNormalizeDiv), 2)

        mc.connectAttr("{0}.distance".format(lenNoFlipShape), "{0}.input1X".format(gsLegNoFlipNormalizeDiv))
        mc.connectAttr("{0}.distance".format(lenPVShape), "{0}.input1X".format(gsLegPVNormalizeDiv))

        mc.connectAttr("{0}.scaleY".format(ctrlRootTrans), "{0}.input2X".format(gsLegNoFlipNormalizeDiv))
        mc.connectAttr("{0}.scaleY".format(ctrlRootTrans), "{0}.input2X".format(gsLegPVNormalizeDiv))

        # connect the normalized distance into the leg, forcing if necessary
        for i in range(len(animCrvPV)):
            mc.connectAttr("{0}.outputX".format(gsLegPVNormalizeDiv), "{0}.input".format(animCrvPV[i]), f=True)

        for i in range(len(animCrvPV)):
            mc.connectAttr("{0}.outputX".format(gsLegNoFlipNormalizeDiv), "{0}.input".format(animCrvNoFlip[i]), f=True)

        # fixing the knee control
        gScaleUpLegToKneeDiv = "globalScale_{0}upperLeg_to_kneeNormalize_DIV".format(leftRight)
        gScaleKneeToFootDiv = "globalScale_{0}knee_to_footNormalize_DIV".format(leftRight)

        mc.shadingNode("multiplyDivide", n=gScaleUpLegToKneeDiv, au=True)
        mc.shadingNode("multiplyDivide", n=gScaleKneeToFootDiv, au=True)

        mc.setAttr("{0}.operation".format(gScaleUpLegToKneeDiv), 2)
        mc.setAttr("{0}.operation".format(gScaleKneeToFootDiv), 2)

        # create inversions for left right (or rather, multiply by -1 if right, 1 if normal)
        gScaleUpLegToKneeINV = "globalScale_{0}upperLeg_to_kneeInvert_MUL".format(leftRight)
        gScaleKneeToFootINV = "globalScale_{0}knee_to_footInvert_MUL".format(leftRight)

        mc.shadingNode("multiplyDivide", n=gScaleUpLegToKneeINV, au=True)
        mc.setAttr("{0}.operation".format(gScaleUpLegToKneeINV), 1)
        mc.setAttr("{0}.input2X".format(gScaleUpLegToKneeINV), imVal)

        mc.shadingNode("multiplyDivide", n=gScaleKneeToFootINV, au=True)
        mc.setAttr("{0}.operation".format(gScaleKneeToFootINV), 1)
        mc.setAttr("{0}.input2X".format(gScaleKneeToFootINV), imVal)
        ########

        disSnapUpperShape = mc.listRelatives(disSnapUpper, s=True)[0]
        disSnapLowerShape = mc.listRelatives(disSnapLower, s=True)[0]

        mc.connectAttr("{0}.distance".format(disSnapUpperShape), "{0}.input1X".format(gScaleUpLegToKneeINV))
        mc.connectAttr("{0}.distance".format(disSnapLowerShape), "{0}.input1X".format(gScaleKneeToFootINV))

        mc.connectAttr("{0}.outputX".format(gScaleUpLegToKneeINV), "{0}.input1X".format(gScaleUpLegToKneeDiv))
        mc.connectAttr("{0}.outputX".format(gScaleKneeToFootINV), "{0}.input1X".format(gScaleKneeToFootDiv))

        mc.connectAttr("{0}.scaleY".format(ctrlRootTrans), "{0}.input2X".format(gScaleUpLegToKneeDiv))
        mc.connectAttr("{0}.scaleY".format(ctrlRootTrans), "{0}.input2X".format(gScaleKneeToFootDiv))

        mc.connectAttr("{0}.outputX".format(gScaleUpLegToKneeDiv), "{0}.color1R".format(blndNdUpperStretchChoice),
                       f=True)
        mc.connectAttr("{0}.outputX".format(gScaleKneeToFootDiv), "{0}.color1R".format(blndNdLowerStretchChoice),
                       f=True)

        return

    def cleanLeg(self, ctrlFootSettings, ctrlIKFoot, ctrlKnee, grpKnee, fkJnts, *args):
        CRU.lockHideCtrls(ctrlFootSettings, translate=True, rotate=True, scale=True, visibility=True)
        CRU.lockHideCtrls(ctrlIKFoot, visibility=True, scale=True)
        CRU.lockHideCtrls(ctrlKnee, rotate=True, scale=True, visibility=True)
        CRU.lockHideCtrls(grpKnee, rotate=True, scale=True, translate=True, visibility=True)

        for i in range(len(fkJnts)):
            CRU.lockHideCtrls(fkJnts[i], scale=True, translate=True, visibility=True)
            CRU.lockHideCtrls(fkJnts[i], theVals=["radi"], channelBox=False)

        return

    def setIKStretchOption(self, ctrlFootSettings, ikJntsPV, ikJntsNoFlip, legLens,
                           leftRight, *args):
        # this is a test for personal expansion ideas
        # this needs to be later on, so we put this at the end
        ikStretchAttr = "IK_stretch"
        enumVals = "on:off"
        mc.addAttr(ctrlFootSettings, longName=ikStretchAttr, at="enum", k=True, en=enumVals)

        self.createStretchIKCond(ikJntsPV, legLens, ctrlFootSettings, ikStretchAttr, leftRight, "pv_")
        self.createStretchIKCond(ikJntsNoFlip, legLens, ctrlFootSettings, ikStretchAttr, leftRight, "noFlip_")

        return

    def createStretchIKCond(self, ikJnts, legLens, ctrlFootSettings, ikStretchAttr, leftRight, type, *args):
        # stretches the upper leg
        lowerLegStretchCond = "{0}lowerLeg_{1}stretch_COND".format(leftRight, type)

        mc.shadingNode("condition", n=lowerLegStretchCond, au=True)
        mc.setAttr("{0}.colorIfFalse".format(lowerLegStretchCond), legLens[0], 0, 0)
        mc.connectAttr("{0}.{1}".format(ctrlFootSettings, ikStretchAttr), "{0}.firstTerm".format(lowerLegStretchCond))
        mc.setAttr("{0}.secondTerm".format(lowerLegStretchCond), 0)
        mc.setAttr("{0}.operation".format(lowerLegStretchCond), 0)

        lowerLegStretchBlnd = []
        myNode = "blendColors"
        # we are doing this because for some reason, using Source=false doesn't work
        test = mc.listConnections('{0}.tx'.format(ikJnts[1]), d=True, s=False, p=True, type=myNode)

        lowerLegStretchBlnd.append(
            mc.listConnections('{0}.tx'.format(ikJnts[1]), d=True, s=False, p=True, type=myNode)[0])
        lowerLegStretchBlnd.append(
            mc.listConnections('{0}.ty'.format(ikJnts[1]), d=True, s=False, p=True, type=myNode)[0])
        lowerLegStretchBlnd.append(
            mc.listConnections('{0}.tz'.format(ikJnts[1]), d=True, s=False, p=True, type=myNode)[0])

        mc.connectAttr("{0}.translateX".format(ikJnts[1]), "{0}.colorIfTrueR".format(lowerLegStretchCond))
        mc.connectAttr("{0}.translateY".format(ikJnts[1]), "{0}.colorIfTrueG".format(lowerLegStretchCond))
        mc.connectAttr("{0}.translateZ".format(ikJnts[1]), "{0}.colorIfTrueB".format(lowerLegStretchCond))

        mc.connectAttr("{0}.outColorR".format(lowerLegStretchCond), "{0}".format(lowerLegStretchBlnd[0]), f=True)
        mc.connectAttr("{0}.outColorG".format(lowerLegStretchCond), "{0}".format(lowerLegStretchBlnd[1]), f=True)
        mc.connectAttr("{0}.outColorB".format(lowerLegStretchCond), "{0}".format(lowerLegStretchBlnd[2]), f=True)

        #####
        # stretches the lower leg
        footStretchCond = "{0}foot_{1}stretch_COND".format(leftRight, type)
        mc.shadingNode("condition", n=footStretchCond, au=True)
        mc.setAttr("{0}.colorIfFalse".format(footStretchCond), legLens[1], 0, 0)
        mc.connectAttr("{0}.{1}".format(ctrlFootSettings, ikStretchAttr), "{0}.firstTerm".format(footStretchCond))
        mc.setAttr("{0}.secondTerm".format(footStretchCond), 0)
        mc.setAttr("{0}.operation".format(footStretchCond), 0)

        footStretchBlnd = []
        footStretchBlnd.append(mc.listConnections('{0}.tx'.format(ikJnts[2]), d=True, s=False, p=True, type=myNode)[0])
        footStretchBlnd.append(mc.listConnections('{0}.ty'.format(ikJnts[2]), d=True, s=False, p=True, type=myNode)[0])
        footStretchBlnd.append(mc.listConnections('{0}.tz'.format(ikJnts[2]), d=True, s=False, p=True, type=myNode)[0])

        mc.connectAttr("{0}.translateX".format(ikJnts[2]), "{0}.colorIfTrueR".format(footStretchCond))
        mc.connectAttr("{0}.translateY".format(ikJnts[2]), "{0}.colorIfTrueG".format(footStretchCond))
        mc.connectAttr("{0}.translateZ".format(ikJnts[2]), "{0}.colorIfTrueB".format(footStretchCond))

        mc.connectAttr("{0}.outColorR".format(footStretchCond), "{0}".format(footStretchBlnd[0]), f=True)
        mc.connectAttr("{0}.outColorG".format(footStretchCond), "{0}".format(footStretchBlnd[1]), f=True)
        mc.connectAttr("{0}.outColorB".format(footStretchCond), "{0}".format(footStretchBlnd[2]), f=True)

    def makeLegFKIKComplete(self, bndJnts, fkJnts, ctrlIK, ):
        fkSwitchJnts = self.makeFKSnapJnts(fkJnts, bndJnts)

        ctrlIKSwitch = self.makeIKSnap(ctrlIK, bndJnts)

        return

    def makeFKSnapJnts(self, fkJnts, bndJnts):
        fkSwitchJnts = []
        for i in range(len(fkJnts[:-1])):
            # create duplicates of everything except the last joint
            if "CTRL_FK_" in fkJnts[i]:
                rename = fkJnts[i].replace("CTRL_FK_", "JNT_FKsnap_")
            elif "JNT_FK_" in fkJnts[i]:
                rename = fkJnts[i].replace("JNT_FK_", "JNT_FKsnap_")
            mc.duplicate(fkJnts[i], n=rename, po=True)
            # we want to save the foot joint
            if "foot" in fkJnts[i]:
                bndFoot = bndJnts[i]
            # we don't want to do the ankleTwist here
            if "ankleTwist" in fkJnts[i]:
                jntAnkleTwistSwitch = rename
            else:
                CRU.lockHideCtrls(rename, translate=True, visibility=True, attrVisible=True, toLock=False)
                mc.parent(rename, bndJnts[i])
                mc.setAttr("{0}.visibility".format(rename), False)
                CRU.lockHideCtrls(rename, visibility=True)
            fkSwitchJnts.append(rename)

        # put the ankleTwist under foot
        if self.cbAnkleTwist:
            CRU.lockHideCtrls(jntAnkleTwistSwitch, translate=True, visibility=True, attrVisible=True, toLock=False)
            mc.parent(jntAnkleTwistSwitch, bndFoot)
            mc.setAttr("{0}.visibility".format(jntAnkleTwistSwitch), False)
            CRU.lockHideCtrls(jntAnkleTwistSwitch, visibility=True)

        return fkSwitchJnts

    def makeIKSnap(self, ctrlIK, bndJnts):
        # create the foot IK and parent it under the foot
        ctrlIKSwitch = ctrlIK.replace("CTRL_", "GRP_IKsnap_")
        mc.duplicate(ctrlIK, n=ctrlIKSwitch, po=True)
        mc.parent(ctrlIKSwitch, bndJnts[-3])

        CRU.lockHideCtrls(ctrlIKSwitch, translate=True, visibility=True, attrVisible=True, toLock=False)
        mc.setAttr("{0}.visibility".format(ctrlIKSwitch), False)
        CRU.lockHideCtrls(ctrlIKSwitch, visibility=True)

        return ctrlIKSwitch

    def makeLegComplete(self, bndJnts,
                        colourTU,
                        leftRight, isLeft,
                        ctrlRootTrans,
                        jntIKHip,
                        grpDNTTorso,
                        geoJntArray,

                        *args):
        # create the FK and IK joints
        jntsTemp = mc.duplicate(bndJnts[0], rc=True)
        fkJnts = self.renameIKFKLimbs(jntsTemp, textToReplace="_BND_", textReplacement="_FK_", stripLastVal=1,
                                      renameThis=True, addToEnd="", )
        newLayerNameFK = "{0}leg_FK_LYR".format(leftRight)
        CRU.layerEdit(fkJnts, newLayerName=newLayerNameFK, colourTU=colourTU)
        jntsTemp = mc.duplicate(bndJnts[0], rc=True)
        ikJnts = self.renameIKFKLimbs(jntsTemp, textToReplace="_BND_", textReplacement="_IK_", stripLastVal=1,
                                      renameThis=True, addToEnd="", )
        ikLegStretchLens = []
        ikLegStretchLens.append(mc.getAttr("{0}.translateX".format(ikJnts[1])))
        ikLegStretchLens.append(mc.getAttr("{0}.translateX".format(ikJnts[2])))

        newLayerNameIK = "{0}leg_IK_LYR".format(leftRight)

        CRU.layerEdit(ikJnts, newLayerName=newLayerNameIK)

        mc.setAttr("{0}.displayType".format(newLayerNameIK), 0)
        mc.setAttr("{0}.color".format(newLayerNameIK), 0)
        if isLeft:
            clrIKrgb = [0, 0.5, 1]
        else:
            clrIKrgb = [1, 0.5, 0]
        mc.setAttr("{0}.overrideColorRGB".format(newLayerNameIK), clrIKrgb[0], clrIKrgb[1], clrIKrgb[2])
        mc.setAttr("{0}.overrideRGBColors".format(newLayerNameIK), 1)

        CRU.layerEdit(bndJnts, bndLayer=True)

        # the jnt_BND_lyr is supposed to be for the skinning joints
        if self.cbTwists:
            # we want to not have the legs in the bnd layer if we have twists
            altBnds = [x for x in bndJnts if "leg" in x.lower() or "ankletwist" in x.lower() or "toeend" in x.lower()]
        else:
            altBnds = [x for x in bndJnts if
                       "legend" in x.lower() or "ankletwist" in x.lower() or "toeend" in x.lower()]

        CRU.layerEdit(altBnds, bndAltLayer=True, noRecurse=True)

        CRU.changeRotateOrder(bndJnts, "XZY")
        CRU.changeRotateOrder(fkJnts, "XZY")
        CRU.changeRotateOrder(ikJnts, "XZY")

        # creates the foot settings control

        jntFoot = [x for x in bndJnts if "foot" in x[-4:]][0]

        name = "settings_" + leftRight + "leg"
        ctrlFootSettings = CRU.createNailNoOffset(jntFoot, isLeft, name, bodySize=15, headSize=2, colourTU=colourTU,
                                                  pnt=True)

        grpSettings = "GRP_settings"
        if not mc.objExists(grpSettings):
            mc.group(n=grpSettings, w=True, em=True)
        mc.parent(ctrlFootSettings, grpSettings)
        CRU.layerEdit(grpSettings, newLayerName="settings_LYR", colourTU=CRU.clrSettings)
        # creates the FKIK blend control

        fkikBlendName = "fkik_blend"
        fkikBlendNiceName = "FK / IK Blend"
        # NOTE: we make the default value 0.5 for testing purposes
        mc.addAttr(ctrlFootSettings, longName=fkikBlendName, niceName=fkikBlendNiceName, at="float", k=True, min=0,
                   max=1, dv=1)

        self.makeBlendBasic(fkJnts, ikJnts, bndJnts, ctrlFootSettings, fkikBlendName, rotate=True, translate=True)

        fkJnts = self.createFKCtrls(fkJnts, colourTU, leftRight)

        # Stretch FK
        ctrlFKLengthKeyArray = self.makeFKStretch(fkJnts)

        # IK Setup
        ctrlIKFoot, ikLegs, ikBall, ikToe = self.createIKLegs(ikJnts, newLayerNameIK, leftRight)

        # we need to put this here in case we have the ankleTwist option
        if self.cbTwists:
            mkTwists = 4
            geoJntArrayExtend = self.makeTwists(mkTwists, bndJnts[0], bndJnts[1], ctrlFootSettings,
                                                ctrlIKFoot, leftRight)
            geoJntArray.extend(geoJntArrayExtend)
            altBnds = geoJntArrayExtend[-1]
            CRU.layerEdit(geoJntArrayExtend, bndLayer=True, noRecurse=True)
            CRU.layerEdit(altBnds, bndAltLayer=True, noRecurse=True)

            if self.cbAnkleTwist:
                # use the foot for the foot twist
                geoJntArrayExtend2 = self.makeTwists(mkTwists, bndJnts[1], bndJnts[3], ctrlFootSettings,
                                                     ctrlIKFoot, leftRight, fkikBlendName, )
            else:
                geoJntArrayExtend2 = self.makeTwists(mkTwists, bndJnts[1], bndJnts[2], ctrlFootSettings,
                                                     ctrlIKFoot, leftRight)
            altBnds = geoJntArrayExtend2[-1]

            CRU.layerEdit(geoJntArrayExtend2, bndLayer=True, noRecurse=True)
            CRU.layerEdit(altBnds, bndAltLayer=True, noRecurse=True)
            geoJntArray.extend(geoJntArrayExtend2)

        if self.cbGeo:
            CRU.tgpSetGeo(geoJntArray, setLayer=True, printOut=False)

            if not self.cbTwists:
                jntLegsNoTwist = [x for x in geoJntArray if "Leg" in x[-3:]]
                CRU.tgpSetGeoSpecial(jntLegsNoTwist, setLayer=True, keyWord="Seg", stretch=True)

        # IK Stretch
        locIKLegLenStart, locIKLegLenEnd, disIKLeg, disIKLegShape, ctrlIKLengthKeyArray = self.makeIKStretch(ikJnts,
                                                                                                             leftRight,
                                                                                                             ctrlIKFoot)

        # No flip knee for IK leg
        # pole vector
        grpNoFlipKnee, locKnee = self.createNoFlipIKLeg(ikJnts, ctrlIKFoot, ikLegs, leftRight)

        cDKList = self.createDualKnee(
            ikJnts, ctrlIKFoot, ikLegs, grpNoFlipKnee,
            locIKLegLenEnd, locIKLegLenStart,
            ctrlFootSettings, leftRight, newLayerNameIK)
        ikJntsPV, ikJntsNoFlip, ctrlKnee, animCrvPV, animCrvNoFlip, autoManualLN, locStartNoFlip, lenNoFlip, locStartPV, lenPV = cDKList

        cSKList = self.createSnappableKnee(ikJntsPV, ctrlKnee, leftRight, ctrlIKFoot, animCrvPV)

        locSnapUpperToKneeStart, disSnapUpper, disSnapLower, blndNdUpperStretchChoice, blndNdLowerStretchChoice = cSKList
        self.createNonUniformStretchNoFlip(ctrlIKFoot, leftRight, animCrvNoFlip, ikJntsNoFlip)

        grpKnee = self.toggleFKIKVisibility(ctrlFootSettings, ctrlIKFoot, ctrlKnee, fkJnts, fkikBlendName,
                                            autoManualLN, leftRight)

        grpIKConst, grpBNDConst, grpFKConst = self.organizeLeg(grpKnee,
                                                               bndJnts, ikJnts, ikJntsPV, ikJntsNoFlip,
                                                               fkJnts, ctrlIKFoot,
                                                               locStartNoFlip, lenNoFlip, locStartPV, lenPV,
                                                               locSnapUpperToKneeStart,
                                                               disSnapUpper, disSnapLower,
                                                               leftRight,
                                                               ctrlRootTrans)

        self.hipSetup(grpBNDConst, grpIKConst, grpFKConst,
                      jntIKHip,
                      grpDNTTorso, ctrlRootTrans,
                      ctrlFootSettings,
                      leftRight)
        self.fkHipTwistFix(grpBNDConst, ctrlFootSettings, fkikBlendName, leftRight)

        self.legIKScaleFix(lenPV, lenNoFlip,
                           animCrvPV, animCrvNoFlip,
                           ctrlRootTrans,
                           disSnapUpper, disSnapLower,
                           blndNdUpperStretchChoice, blndNdLowerStretchChoice,
                           leftRight)
        self.cleanLeg(ctrlFootSettings, ctrlIKFoot, ctrlKnee, grpKnee, fkJnts)
        # creates the ability to turn on and off the stretch
        self.setIKStretchOption(ctrlFootSettings, ikJntsPV, ikJntsNoFlip, ikLegStretchLens, leftRight, )
        if self.cbSwitchSetup:
            self.makeLegFKIKComplete(bndJnts, fkJnts, ctrlIKFoot)

        if isLeft:
            setVal = 0
        else:
            setVal = 1

        mc.setAttr("{0}.fkik_blend".format(ctrlFootSettings), setVal)

        # return

    def tgpMakeBC(self, mirrorSel=None, lrSel=None,
                  cbTwists=None, cbAnkleTwist=None, cbSwitchSetup=None, cbGeo=None, cbHip=None,
                  bndJnt=None, jntIKHipCheck=None, grpDNTTorsoCheck=None,
                  ctrlBodyCheck=None, ctrlRootTransCheck=None, *args):
        symmetry = CRU.checkSymmetry()  # we want symmetry turned off for this process
        if mirrorSel is None:
            mirrorSel = mc.radioButtonGrp("selLegMirrorType_rbg", q=True, select=True)
        if lrSel is None:
            lrSel = mc.radioButtonGrp("selLegType_rbg", q=True, select=True)

        if cbTwists is None:
            self.cbTwists = mc.checkBox("selCreateTwists_cb", q=True, v=True)
        else:
            self.cbTwists = cbTwists
        if cbAnkleTwist is None:
            self.cbAnkleTwist = mc.checkBox("selAnkleTwist_cb", q=True, v=True)
        else:
            self.cbAnkleTwist = cbAnkleTwist
        if cbSwitchSetup is None:
            self.cbSwitchSetup = mc.checkBox("selAddIKFKSwitching_cb", q=True, v=True)
        else:
            self.cbSwitchSetup = cbSwitchSetup
        if cbGeo is None:
            self.cbGeo = mc.checkBox("selGeo_cb", q=True, v=True)
        else:
            self.cbGeo = cbGeo
        if cbHip is None:
            self.cbHip = mc.checkBox("selSpineEnd_cb", q=True, v=True)
        else:
            self.cbHip = cbHip

        if mirrorSel == 1:
            mirrorRig = False
        else:
            mirrorRig = True

        if lrSel == 1:
            isLeft = True
            leftRight = CRU.valLeft
            leftRightMirror = CRU.valRight
            colourTU = CRU.clrLeftFK
            colourTUMirror = CRU.clrRightFK
        else:
            isLeft = False
            leftRight = CRU.valRight
            leftRightMirror = CRU.valLeft
            colourTU = CRU.clrRightFK
            colourTUMirror = CRU.clrLeftFK

        if jntIKHipCheck is None:
            jntIKHipCheck = mc.textFieldButtonGrp("jntIKHip_tfbg", q=True, text=True)
            passVal = "jntIKHip_tfbg"
        else:
            passVal = None
        jntIKHip = CRU.tgpGetTx(jntIKHipCheck, passVal, "joint", "IK Hip Joint", ["JNT", "hip", "IK"])

        if grpDNTTorsoCheck is None:
            grpDNTTorsoCheck = mc.textFieldButtonGrp("grpTorsoDNT_tfbg", q=True, text=True)
            passVal = "grpTorsoDNT_tfbg"
        else:
            passVal = None
        grpDNTTorso = CRU.tgpGetTx(grpDNTTorsoCheck, passVal, "transform", "Torso DO NOT TOUCH",
                                   ["GRP", "DO", "NOT", "TOUCH"],
                                   "group")
        if ctrlBodyCheck is None:
            ctrlBodyCheck = mc.textFieldButtonGrp("ctrlBody_tfbg", q=True, text=True)
            passVal = "ctrlBody_tfbg"
        else:
            passVal = None
        ctrlBody = CRU.tgpGetTx(ctrlBodyCheck, passVal, "nurbsCurve", "Body Control", ["CTRL", "body"],
                                "control")

        if ctrlRootTransCheck is None:
            ctrlRootTransCheck = mc.textFieldButtonGrp("rootTrans_tfbg", q=True, text=True)
            passVal = "rootTrans_tfbg"
        else:
            passVal = None
        ctrlRootTrans = CRU.tgpGetTx(ctrlRootTransCheck, passVal, "nurbsCurve", "Root Transform Control",
                                     ["CTRL", "rootTransform"], "control")

        if not jntIKHip:
            mc.warning("You need to select the IK Hip Control")
            return
        if not grpDNTTorso:
            mc.warning("You need to select the Do Not Touch Group")
            return
        if not ctrlBody:
            mc.warning("You need to select Body Control")
            return
        if not ctrlRootTrans:
            mc.warning("You need to select the Root Transform Control")
            return

        if bndJnt is None:
            bndJnt = mc.textFieldButtonGrp("jointLoad_tfbg", q=True, text=True)
            passVal = "jointLoad_tfbg"
        else:
            passVal = None
        try:
            jntLegRoot = bndJnt
        except:
            mc.warning("No joint selected!")
            return

        if not (CRU.checkLeftRight(isLeft, jntLegRoot)):
            # if the values are not lined up properly, break out
            mc.warning("You are selecting the incorrect side for the leg")
            return
        bndJnts = CRU.tgpGetJnts(bndJnt, passVal, "joint", "Root Leg Joint", ["JNT", "upper", "Leg"])

        checkList = bndJnts
        if checkList is None:
            checkList = [bndJnts]

        geoJntArray = bndJnts[:]

        # make sure the selections are not empty
        # However, editing them out is too much hassle,  it's easier just to leave them both false
        if ((checkList[0] == "") or checkList[0] is None):
            mc.warning("You are missing a selection!")
            return
        else:
            # CRU.createLocatorToDelete()

            if mirrorRig:
                toReplace = "_" + leftRight
                toReplaceWith = "_" + leftRightMirror
                geoJntArrayMirror = []
                bndJntsMirror = mc.mirrorJoint(jntLegRoot, mirrorYZ=True, mirrorBehavior=True,
                                               searchReplace=[toReplace, toReplaceWith])
                jntLegRootMirror = bndJntsMirror[0]
                try:
                    mc.parent(jntLegRootMirror, w=True)
                except:
                    pass
                for mb in bndJntsMirror:
                    if mc.objectType(mb) == "joint":
                        geoJntArrayMirror.append(mb)
                isLeftMirror = not isLeft

            self.makeLegComplete(bndJnts, colourTU, leftRight, isLeft, ctrlRootTrans, jntIKHip,
                                 grpDNTTorso, geoJntArray, )

            if mirrorRig:
                print("Mirroring")

                self.makeLegComplete(bndJntsMirror, colourTUMirror, leftRightMirror, isLeftMirror, ctrlRootTrans,
                                     jntIKHip,
                                     grpDNTTorso, geoJntArrayMirror, )

            # reset the symmetry to the default because otherwise we might get wonky results
            # mc.symmetricModelling(symmetry=symmetry)
