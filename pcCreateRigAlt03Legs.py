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


class pcCreateRigAlt03Legs(UI):
    def __init__(self):

        self.window = "bcWindow"
        self.title = "pcRigLegs"
        self.winSize = (500, 475)

        self.createUI()

    def createCustom(self, *args):
        # selection type

        mc.rowColumnLayout(nc=2, cw=[(1, 500), (2, 500)], cs=[1, 5], rs=[1, 3])

        mc.text(l="Select The Leg Root: ")
        mc.text(l="")
        mc.separator(st="in", h=17, w=500)
        mc.setParent("..")
        mc.rowColumnLayout(nc=3, cw=[(1, 125), (2, 150), (3, 150)], cs=[1, 5], rs=[1, 3],
                           cal=([1, "left"], [2, "left"], [3, "left"],))

        mc.text(l="Mirror Leg As Well?")
        # mc.setParent("..")
        mc.radioButtonGrp("selLegMirrorType_rbg", la2=["No", "Yes"], nrb=2, sl=1, cw2=[50, 50], )
        mc.text(l="")
        mc.checkBox("selCreateTwists_cb", l="Create Twists", en=True, v=False)
        mc.checkBox("selSpineEnd_cb", l="Connect To Hip", en=True, v=True)
        mc.setParent("..")
        mc.separator(st="in", h=17, w=500)

        mc.rowColumnLayout(nc=3, cw=[(1, 100), (2, 200), (3, 150)], cs=[1, 5], rs=[1, 3],
                           cal=([1, "left"], [2, "left"], [3, "left"],))
        mc.text(l="Initial Limb: ")
        mc.radioButtonGrp("selLegType_rbg", la2=["Left", "Right"], nrb=2, sl=1, cw2=[50, 50], )
        mc.setParent("..")
        mc.separator(st="in", h=17, w=500)

        # sources
        mc.rowColumnLayout(nc=2, cw=[(1, 140), (2, 360)], cs=[1, 5], rs=[1, 3])
        mc.text(bgc=(0.85, 0.65, 0.25), l="Leg: ")
        mc.textFieldButtonGrp("jointLoad_tfbg", cw=(1, 300), bl="  Load  ")

        mc.text(bgc=(0.85, 0.65, 0.25), l="IK Hip Joint: ")
        mc.textFieldButtonGrp("jntIKHip_tfbg", cw=(1, 300), bl="  Load  ", tx="JNT_IK_hip")

        mc.text(bgc=(0.85, 0.65, 0.25), l="Do Not Touch Torso Group: ")
        mc.textFieldButtonGrp("grpTorsoDNT_tfbg", cw=(1, 300), bl="  Load  ", tx="GRP_DO_NOT_TOUCH_torso")

        mc.text(bgc=(0.85, 0.65, 0.25), l="Body CTRL: ")
        mc.textFieldButtonGrp("ctrlBody_tfbg", cw=(1, 300), bl="  Load  ", tx="CTRL_body")

        mc.text(bgc=(0.85, 0.65, 0.25), l="Root Transform Control: ")
        mc.textFieldButtonGrp("rootTrans_tfbg", cw=(1, 300), bl="  Load  ", tx="CTRL_rootTransform_emma")

        mc.setParent("..")

        mc.separator(st="in", h=10, w=500)

        mc.rowColumnLayout(nc=2, cw=[(1, 100), (2, 370)], cs=[1, 5], rs=[1, 3])
        mc.checkBox("selGeo_cb", l="Affect Geometry", en=True, v=True)

        mc.setParent("..")

        # load buttons
        #
        mc.textFieldButtonGrp("jointLoad_tfbg", e=True, bc=self.loadSrc1Btn)

        mc.textFieldButtonGrp("jntIKHip_tfbg", e=True, bc=self.loadSrc2Btn)
        mc.textFieldButtonGrp("grpTorsoDNT_tfbg", e=True, bc=self.loadSrc3Btn)
        mc.textFieldButtonGrp("ctrlBody_tfbg", e=True, bc=self.loadSrc4Btn)
        mc.textFieldButtonGrp("rootTrans_tfbg", e=True, bc=self.loadSrc5Btn)

        self.selLoad = []
        self.jointArray = []
        mc.showWindow(self.window)

    def createButtonCmd(self, *args):
        self.tgpMakeBC()

    def loadSrc1Btn(self):
        self.selSrc1 = self.tgpLoadJntsBtn("jointLoad_tfbg", "joint", "Root Leg Joint", ["JNT", "upper", "Leg"])
        print(self.selSrc1)

    def loadSrc2Btn(self):
        self.selSrc2 = self.tgpLoadTxBtn("jntIKHip_tfbg", "joint", "IK Hip Joint", ["JNT", "hip", "IK"])
        print(self.selSrc2)

    def loadSrc3Btn(self):
        self.selSrc3 = self.tgpLoadTxBtn("grpTorsoDNT_tfbg", "transform", "Torso DO NOT TOUCH",
                                         ["GRP", "DO", "NOT", "TOUCH"],
                                         "group")
        print(self.selSrc3)

    def loadSrc4Btn(self):
        self.selSrc4 = self.tgpLoadTxBtn("ctrlBody_tfbg", "nurbsCurve", "COG Control", ["CTRL", "COG"],
                                         "control")
        print(self.selSrc4)

    def loadSrc5Btn(self):
        self.selSrc5 = self.tgpLoadTxBtn("rootTrans_tfbg", "nurbsCurve", "Root Transform Control",
                                         ["CTRL", "rootTransform", "follow"], "control")
        print(self.selSrc5)

    def loadSrc6Btn(self):
        self.selSrc6 = self.tgpLoadTxBtn("grpTorsoDNT_tfbg", "transform", "Torso DO NOT TOUCH",
                                         ["GRP", "DO", "NOT", "TOUCH"],
                                         "group")
        print(self.selSrc6)

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

    def tgpLoadJntsBtn(self, loadBtn, objectType, objectDesc, keywords, objectNickname=None):
        if objectNickname is None:
            objectNickname = objectType
        # hierarchy
        self.selLoad = []
        self.selLoad = mc.ls(sl=True, fl=True, type="joint")

        if (len(self.selLoad) != 1):
            mc.warning("Select only the root joint")
            return
        else:

            selName = self.selLoad[0]
            if not all(word.lower() in selName.lower() for word in keywords):
                mc.warning("That is the wrong {0}. Select the {1}".format(objectNickname, objectDesc))

                return

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
                nextJnts = mc.listRelatives(val, c=True, type="joint", ad=True)
                nextJnt = nextJnts[-2]
                nextJntVal = nextJnts[-1]

                # with the ankle, we can create the control

            nextJntYVal = mc.getAttr("{0}.ty".format(nextJntVal))
            nextJntIncrement = nextJntYVal / (numTwistsPlus1)
            twistJnt = mc.duplicate(val, po=True, n="ToDelete")

            # create the joint twists at the proper location

            # upper leg is positive, lower leg is negative
            '''
            # The calculation should look like this. The negative values may not be needed
            JNT_l_upperLegTwist1.rotateY = JNT_l_lowerLeg.rotateY * 0.25* CTRL_l_foot.upperLegTwist;
            JNT_l_upperLegTwist2.rotateY = JNT_l_lowerLeg.rotateY * 0.5* CTRL_l_foot.upperLegTwist;
            JNT_l_upperLegTwist3.rotateY = JNT_l_lowerLeg.rotateY * 0.75* CTRL_l_foot.upperLegTwist;
            
            JNT_l_lowerLegTwist1.rotateY = JNT_l_ankleTwist.rotateY * -0.25* CTRL_l_foot.lowerLegTwist;
            JNT_l_lowerLegTwist2.rotateY = JNT_l_ankleTwist.rotateY * -0.5* CTRL_l_foot.lowerLegTwist;
            JNT_l_lowerLegTwist3.rotateY = JNT_l_ankleTwist.rotateY * -0.75* CTRL_l_foot.lowerLegTwist;
            '''
            for x in range(twists):

                valx = x + 1
                twistTempName = "{0}Twist{1}".format(val, valx)

                twistTemp = mc.duplicate(twistJnt, n=twistTempName)

                mc.parent(twistTemp, jntLegArray[i])
                mc.setAttr("{0}.ty".format(twistTempName), nextJntIncrement * valx)
                twistJntsSubgroup.append(twistTemp[0])

                twistInverse = 1.0 / (numTwistsPlus1)
                '''
                # this was not necessary, but I am still keeping this as other rigs may still suffer this problem
                if i == 0:
                    twistInverse = 1.0 / (numTwistsPlus1)
                else:
                    twistInverse = -1.0 / (numTwistsPlus1)'''

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

    def makeBlend(self, jntsSrc1, jntsSrc2, jntsTgt, ctrl, ctrlAttr, rotate, translate, override=False, *args):

        blndNodeTrans = []
        blndNodeRot = []
        for i in range(len(jntsSrc1)):
            print("======")
            print("jntsSrc1[{0}]: {1}".format(i, jntsSrc1[i]))
            print("jntsSrc2[{0}]: {1}".format(i, jntsSrc2[i]))
            print("jntsTgt[{0}]: {1}".format(i, jntsTgt[i]))
            print("ctrl: {0}".format(ctrl))
            print("ctrlAttr: {0}".format(ctrlAttr))
            name = jntsTgt[i]
            if translate:
                val = ".translate"
                blndNodeTrans.append(mc.shadingNode("blendColors", au=True, name="{0}_trans_BCN###".format(name)))
                mc.connectAttr(jntsSrc1[i] + val, blndNodeTrans[i] + ".color1")
                mc.connectAttr(jntsSrc2[i] + val, blndNodeTrans[i] + ".color2")
                mc.connectAttr(blndNodeTrans[i] + ".output", jntsTgt[i] + "{0}".format(val))
                blndName = "{0}.{1}".format(ctrl, ctrlAttr)
                mc.connectAttr(blndName, blndNodeTrans[i] + ".blender", f=True)

            if rotate:
                val = ".rotate"
                blndNodeRot.append(mc.shadingNode("blendColors", au=True, name="{0}_rot_BCN###".format(name)))
                mc.connectAttr(jntsSrc1[i] + val, blndNodeRot[i] + ".color1")
                mc.connectAttr(jntsSrc2[i] + val, blndNodeRot[i] + ".color2")
                mc.connectAttr(blndNodeRot[i] + ".output", jntsTgt[i] + "{0}".format(val))
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

    def createFKCtrls(self, fkJnts, colourTU, *args):
        for i in range(len(fkJnts[:-1])):
            fkJnt = fkJnts[i]
            print(fkJnt)
            if "Leg" in fkJnt:
                legChild = mc.listRelatives(fkJnt, typ="joint")[0]
                legLen = mc.getAttr("{0}.translateX".format(legChild))
                print(legLen)
                if i == 0:
                    sizeTU = 13
                else:
                    sizeTU = 11
                ctrl, ctrlShape = CRU.createCTRLsFKDirect(fkJnt, size=sizeTU, orientVal=(1, 0, 0), colour=colourTU, )
                fkJnts[i] = ctrl

                mc.select(ctrlShape + ".cv[:]")

                mc.move(legLen * 0.5, 0, -legLen * 0.05, r=True, os=True)
            else:

                if "foot" in fkJnt:
                    sizeTU = 12
                    ctrl, ctrlShape = CRU.createCTRLsFKDirect(fkJnt, size=sizeTU, orientVal=(0, 1, 0),
                                                              colour=colourTU, )

                    mc.select(ctrlShape + ".cv[:]")
                    mc.rotate(0, 0, 90, ws=True)
                else:
                    sizeTU = 7
                    ctrl, ctrlShape = CRU.createCTRLsFKDirect(fkJnt, size=sizeTU, orientVal=(1, 0, 0),
                                                              colour=colourTU, )

                    mc.select(ctrlShape + ".cv[5:7]")
                    mc.select(ctrlShape + ".cv[0:1]", add=True)
                    mc.scale(0, cp=True, z=True)
                fkJnts[i] = ctrl

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
        ikJntFoot = [x for x in ikJnts if "foot" in x[-4:]][0]
        ikJntBall = [x for x in ikJnts if "ball" in x[-4:]][0]
        ikJntToe = [x for x in ikJnts if "toe" in x][0]

        size = mc.getAttr("{0}.tx".format(ikJnts[-1]))
        ctrlName = "CTRL_{0}foot".format(leftRight)
        orientVal = [0, 1, 0]
        ctrlIKFoot = mc.circle(r=size, n=ctrlName, nr=orientVal)[0]
        todelete = mc.pointConstraint(ikJntFoot, ctrlIKFoot)
        mc.delete(todelete)

        # adjust size for foot
        mc.select("{0}.cv[:]".format(ctrlIKFoot))
        mc.move(0, moveY=True, ws=True)
        mc.move(2.6, moveZ=True, r=True)
        mc.scale(.8, xz=True)
        mc.select("{0}.cv[3:7]".format(ctrlIKFoot))
        mc.move(size * 1.4, moveZ=True, r=True)
        mc.makeIdentity(ctrlIKFoot, apply=True)
        mc.select(cl=True)

        CRU.layerEdit(ctrlIKFoot, newLayerName=newLayerNameIK)
        CRU.changeRotateOrder(ctrlIKFoot, "ZXY")

        jntsToUseFoot = [ikJnts[0], ikJntFoot]
        ikSolver = "ikRPsolver"

        ikLegs = self.createIKVal(jntsToUseFoot, leftRight, "foot", ikSolver, )
        mc.parent(ikLegs[0], ctrlIKFoot)

        jntsToUseBall = [ikJntFoot, ikJntBall]
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
        # creates locators that measure distance for the leg
        ikJntFoot = [x for x in ikJnts if "foot" in x[-4:]][0]
        # create the starting space locator for the distance node
        locIKLegLenStart = "LOC_IK_{0}leg_lengthStart".format(leftRight)
        mc.spaceLocator(p=(0, 0, 0), name=locIKLegLenStart)
        todelete = mc.pointConstraint(ikJnts[0], locIKLegLenStart)
        mc.delete(todelete)

        locIKLegLenEnd = "LOC_IK_{0}leg_lengthEnd".format(leftRight)
        mc.spaceLocator(p=(0, 0, 0), name=locIKLegLenEnd)
        todelete = mc.pointConstraint(ikJntFoot, locIKLegLenEnd)
        mc.delete(todelete)

        disIKLeg = "LEN_IK_{0}leg".format(leftRight)
        disIKLegShape = self.createDistanceDimensionNode(locIKLegLenStart, locIKLegLenEnd, disIKLeg)
        mc.parent(locIKLegLenEnd, ctrlIKFoot)

        driverAttr = "distance"
        driverLen = mc.getAttr("{0}.{1}".format(disIKLegShape, driverAttr))

        upperLegLen = mc.getAttr("{0}.translateX".format(ikJnts[1]))
        lowerLegLen = mc.getAttr("{0}.translateX".format(ikJntFoot))
        sumLegLen = upperLegLen + lowerLegLen

        print("driverLen: {0}".format(driverLen))
        print("upperLegLen: {0}".format(upperLegLen))
        print("lowerLegLen: {0}".format(lowerLegLen))
        print("totalLegLen: {0}".format(sumLegLen))

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

    def createDistanceDimensionNode(self, startLoc, endLoc, lenNodeName):

        distDimShape = mc.distanceDimension(sp=(0, 0, 0), ep=(0, 0, 0))
        mc.connectAttr("{0}.worldPosition".format(startLoc), "{0}.startPoint".format(distDimShape), f=True)
        mc.connectAttr("{0}.worldPosition".format(endLoc), "{0}.endPoint".format(distDimShape), f=True)
        distDimParent = mc.listRelatives(distDimShape, p=True)
        mc.rename(distDimParent, lenNodeName)
        lenNodeNameShape = mc.listRelatives(lenNodeName, s=True)[0]
        return lenNodeNameShape

    def createNoFlipIKLeg(self, ikJnts, ctrlIKFoot, ikLegs, leftRight, *args):

        locKnee = "LOC_{0}knee".format(leftRight)
        mc.spaceLocator(p=(0, 0, 0), name=locKnee)
        todelete = mc.pointConstraint(ikJnts[1], locKnee)
        mc.delete(todelete)
        legLen = mc.getAttr("{0}.translateX".format(ikJnts[1]))
        mc.move(legLen, locKnee, r=True, moveZ=True)
        mc.makeIdentity(locKnee, apply=True)

        mc.poleVectorConstraint(locKnee, ikLegs[0])

        # now we make it so that we don't flip the knee
        # point snap the loc_knee to the JNT_IK_foot (or CTRL_foot since they're the same location)
        todelete = mc.pointConstraint(ctrlIKFoot, locKnee)
        mc.move(legLen, locKnee, r=True, moveX=True)
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

        kneeTwist = "kneeTwist"
        mc.addAttr(ctrlIKFoot, longName=kneeTwist, at="float", k=True)
        mc.connectAttr("{0}.{1}".format(ctrlIKFoot, kneeTwist), "{0}.rotateY".format(grpNoFlipKnee))
        mc.setAttr("{0}.v".format(locKnee), False)
        return grpNoFlipKnee, locKnee

    def createDualKnee(self, ikJnts, ctrlIKFoot, ikLegs, grpNoFlipKnee, locIKLegLenEnd, locIKLegLenStart,
                       ctrlFootSettings, leftRight, newLayerNameIK, *args):

        # get the noFlip values
        dupsNoFlip = mc.duplicate(ctrlIKFoot, ic=True, un=True, rc=True)
        leftRightVal = "_{0}".format(leftRight)
        print("dupsNoFlip: {0}".format(dupsNoFlip))

        mc.delete(ikLegs[0], locIKLegLenStart, locIKLegLenEnd, grpNoFlipKnee)

        dupsTrackNoFlip, dupsMoveNoFlip, returnLegNoFlip = self.duplicateNoFlipOrPV(locIKLegLenEnd, grpNoFlipKnee,
                                                                                    ikLegs, ctrlIKFoot,
                                                                                    dupsNoFlip, leftRightVal,
                                                                                    prefix="noFlip")

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
        print("dupsPVHDL: {0}".format(dupsPVHDL))
        print("dupsPVLocEnd: {0}".format(dupsPVLocEnd))
        dupsTrackPV, dupsMovePV, returnLegPV = self.duplicateNoFlipOrPV(dupsPVLocEnd, grpNoFlipKnee, dupsPVHDL,
                                                                        ctrlIKFoot,
                                                                        dupsPV, leftRightVal, prefix="pv",
                                                                        altPrefixReplace="noFlip", )
        mc.delete(dupsPVToDelete)
        dupsPVgrpLoc = [x for x in dupsMovePV if "GRP" in x]
        print("dupsPVgrpLoc: {0}".format(dupsPVgrpLoc))
        locPVKnee = mc.listRelatives(dupsPVgrpLoc)[0]
        print("locPVKnee: {0}".format(locPVKnee))
        mc.parent(locPVKnee, w=True)
        mc.delete(dupsPVgrpLoc)
        dupsPVHDL = [x for x in dupsMovePV if "HDL" in x][0]
        print("dupsPVHDL: {0}".format(dupsPVHDL))
        mc.setAttr("{0}.twist".format(dupsPVHDL), 0)
        mc.move(0, 0, 0, locPVKnee, os=True)

        # blend the auto/manual leg control
        longName = "autoManualKneeBlend"
        niceName = "Auto (noFlip) / Manual (PV) Knee Blend"
        # note: we se DV to 0.5 for testing purposes
        mc.addAttr(ctrlFootSettings, longName=longName, niceName=niceName, at="float", k=True, min=0, max=1, dv=0.5)

        ikJntsPV = mc.listRelatives(returnLegPV, type="joint", ad=True)
        ikJntsPV.append(returnLegPV)
        ikJntsPV.reverse()

        ikJntsNoFlip = mc.listRelatives(returnLegNoFlip, type="joint", ad=True)
        ikJntsNoFlip.append(returnLegNoFlip)
        ikJntsNoFlip.reverse()

        self.makeBlend(ikJntsPV, ikJntsNoFlip, ikJnts, ctrlFootSettings, longName, rotate=True, translate=False)

        # hide values
        mc.setAttr("{0}.v".format(ikJntsPV[0]), False)
        mc.setAttr("{0}.v".format(ikJntsNoFlip[0]), False)
        # note: I am keeping this visible for testing purposes
        # mc.setAttr("{0}.v".format(ikJntsPV[0]), False)

        # create a pyramid
        boxDimensionsLWH = [2, 2, 4]
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

    def duplicateNoFlipOrPV(self, locIKLegLenEnd, grpNoFlipKnee, ikLegs, ctrlIKFoot, dups, leftRightVal, prefix,
                            altPrefixReplace=None, *args):
        dupsTrack = []
        dupsMove = []
        checkToMove = [locIKLegLenEnd, grpNoFlipKnee, ikLegs[0]]
        toDelete = []
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
                if "CTRL" in dupReplace or "ball" in dupReplace:
                    toDelete.append(dupReplace)
                if "upperLeg" in dupReplace:
                    returnLeg = dupReplace

        mc.parent(dupsMove, ctrlIKFoot)
        mc.delete(toDelete)
        print("returnLeg: {0}".format(returnLeg))
        return dupsTrack, dupsMove, returnLeg

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

    def attachLegToHip(self, fkJnts, ikJnts, bndJnts, ikJntsDrive, fkJntOffsetCtrls, leftRight,
                       *args):
        # Constraining the bind joints to the fk and ik
        bndPntConstraint = mc.pointConstraint(fkJnts[0], ikJnts[0], bndJnts[0])[0]
        self.tgpSetDriverLegFKIKSwitch(ctrlFKIK, ctrlFKIKAttr, bndPntConstraint)

        # Constraining the ik joints to the ik drive
        ikPntConstraint = mc.pointConstraint(ikJntsDrive[0], ikJnts[0])[0]

        # creating the hip attachment and attaching the IK and IKdrive
        hipIKOffsetCtrl = self.createHip(leftRight, ikJnts, ikJntsDrive)

        # Constraining the upperLeg FK control to the upperLeg JNT
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
        bndJntsTempToes = mc.listRelatives(jntLegArray[0], type="joint", ad=True)

        # checking for the toes. If it exists, unparent it
        masterToes = [x for x in bndJntsTempToes if "masterToes" in x]
        if masterToes:
            masterToe = masterToes[0]
            toesParent = mc.listRelatives(masterToe, p=True)[0]
            mc.parent(masterToe, w=True)

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
        # checking for the toes. If it exists, reparent it
        if masterToes:
            mc.parent(masterToe, toesParent)

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

    def createLegOrFootIKNew(self, ikJntsToUse, leftRight, ikSuffix, ikSolver, createCtrl=False, colourTU=0,
                             *args):
        ikSide = leftRight + ikSuffix

        ikLegName = "IK_" + ikSide
        effLegName = "EFF_" + ikSide
        ikLegs = mc.ikHandle(n=ikLegName, sj=ikJntsToUse[0], ee=ikJntsToUse[-1], sol=ikSolver)
        mc.rename(ikLegs[1], effLegName)

        # we are going to hide this eventually anyways
        mc.setAttr("{0}.v".format(ikLegName), False)
        mc.setAttr("{0}.v".format(effLegName), False)

        # fkJntOffsetCtrls.append(self.createCTRLs(temp, size=9, ornt=True, colour=colourTU, orientVal=(0, 1, 0)))
        ikOffsetCtrl = None
        if createCtrl:
            # We just want to create a control at the location, we'll be parenting it.
            ikOffsetCtrl = CRU.createCTRLs(ikLegs[0], 9, pnt=False, ornt=False, prnt=False, colour=colourTU,
                                           addPrefix=True, orientVal=(0, 1, 0), boxDimensionsLWH=[6, 6, 6])
            return ikLegs, ikSide, ikOffsetCtrl

        return ikLegs, ikSide

    def createLegOrFootIK(self, ikJntsToUse, ikJntsDriveToUse, leftRight, colourTU, ikSuffix, createCtrl, ikSolver,
                          *args):
        ikSide = leftRight + ikSuffix

        ikLegName = "IK_" + ikSide
        effLegName = "EFF_" + ikSide
        ikLegs = mc.ikHandle(n=ikLegName, sj=ikJntsDriveToUse[0], ee=ikJntsDriveToUse[-1], sol=ikSolver)
        mc.rename(ikLegs[1], effLegName)

        # we are going to hide this eventually anyways
        mc.setAttr("{0}.v".format(ikLegName), False)
        mc.setAttr("{0}.v".format(effLegName), False)

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
            mc.parent(fkJntOffsetCtrls[0][0], hipIKOffsetCtrl[0], ctrlFKHip)

        # Hiding the visibility of the joints
        mc.setAttr("{0}.visibility".format(ikJnts[0]), False)
        mc.setAttr("{0}.visibility".format(ikJntsDrive[0]), False)
        mc.setAttr("{0}.visibility".format(fkJnts[0]), False)
        mc.setAttr("{0}.visibility".format(hipIKOffsetCtrl[1]), False)

        # locking and hiding the IK controls

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

        CRU.layerEdit(fkJnts, fkLayer=True, noRecurse=True)
        CRU.layerEdit(ikJnts, ikLayer=True, noRecurse=True)
        CRU.layerEdit(ikJntsDrive, ikdriveLayer=True, noRecurse=True)
        CRU.layerEdit(bndJnts, bndLayer=True, noRecurse=True)

        CRU.lockHideCtrls(ikOffsetCtrl[1], rotate=True, scale=True, visible=True)

        for fkOC in fkJntOffsetCtrls:
            CRU.lockHideCtrls(fkOC[1], translate=True, scale=True, visible=True)

    def makeLeg(self, bndJnts,
                colourTU,
                leftRight, isLeft, *args):

        # create the FK and IK joints
        jntsTemp = mc.duplicate(bndJnts[0], rc=True)
        fkJnts = self.renameIKFKLimbs(jntsTemp, textToReplace="_BND_", textReplacement="_FK_", stripLastVal=1,
                                      renameThis=True, addToEnd="", )
        newLayerNameFK = "{0}leg_FK_LYR".format(leftRight)
        CRU.layerEdit(fkJnts, newLayerName=newLayerNameFK, colourTU=colourTU)
        jntsTemp = mc.duplicate(bndJnts[0], rc=True)
        ikJnts = self.renameIKFKLimbs(jntsTemp, textToReplace="_BND_", textReplacement="_IK_", stripLastVal=1,
                                      renameThis=True, addToEnd="", )

        newLayerNameIK = "{0}leg_IK_LYR".format(leftRight)

        CRU.layerEdit(ikJnts, newLayerName=newLayerNameIK)

        mc.setAttr("{0}.displayType".format(newLayerNameIK), 0)
        mc.setAttr("{0}.color".format(newLayerNameIK), 0)
        if isLeft:
            clrRGB = [0, 0.5, 1]
        else:
            clrRGB = [1, 0.5, 0]
        mc.setAttr("{0}.overrideColorRGB".format(newLayerNameIK), clrRGB[0], clrRGB[1], clrRGB[2])
        mc.setAttr("{0}.overrideRGBColors".format(newLayerNameIK), 1)

        CRU.layerEdit(bndJnts, bndLayer=True)

        CRU.changeRotateOrder(bndJnts, "XZY")
        CRU.changeRotateOrder(fkJnts, "XZY")
        CRU.changeRotateOrder(ikJnts, "XZY")

        # creates the foot settings control
        jntFoot = [x for x in bndJnts if "foot" in x[-4:]][0]
        name = "settings_" + leftRight + "leg"
        ctrlFootSettings = CRU.createNailNoOffset(jntFoot, isLeft, name, bodySize=15, headSize=2, colour=colourTU,
                                                  pnt=True)

        grpSettings = "GRP_settings"
        if not mc.objExists(grpSettings):
            mc.group(n=grpSettings, w=True, em=True)
        mc.parent(ctrlFootSettings, grpSettings)
        CRU.layerEdit(grpSettings, newLayerName="settings_LYR", colourTU=9)

        # creates the FKIK blend control

        fkikBlendName = "fkik_blend"
        fkikBlendNiceName = "FK / IK Blend"
        # NOTE: we make the default value 0.5 for testing purposes
        mc.addAttr(ctrlFootSettings, longName=fkikBlendName, niceName=fkikBlendNiceName, at="float", k=True, min=0,
                   max=1, dv=1)

        self.makeBlend(fkJnts, ikJnts, bndJnts, ctrlFootSettings, fkikBlendName, rotate=True, translate=True)

        fkJnts = self.createFKCtrls(fkJnts, colourTU)

        # Stretch FK
        ctrlFKLengthKeyArray = self.makeFKStretch(fkJnts)

        # IK Setup
        # ctrlIKFoot, ikLegs, ikBall, ikToe = self.createIKLegs(ikJnts, newLayerNameIK, leftRight)
        ctrlIKFoot, ikLegs, ikBall, ikToe = self.createIKLegs(ikJnts, newLayerNameIK, leftRight)

        # IK Stretch
        locIKLegLenStart, locIKLegLenEnd, disIKLeg, disIKLegShape, ctrlIKLengthKeyArray = self.makeIKStretch(ikJnts,
                                                                                                             leftRight,
                                                                                                             ctrlIKFoot)

        # No flip knee for IK leg
        # pole vector
        grpNoFlipKnee, locKnee = self.createNoFlipIKLeg(ikJnts, ctrlIKFoot, ikLegs, leftRight)

        self.createDualKnee(ikJnts, ctrlIKFoot, ikLegs, grpNoFlipKnee, locIKLegLenEnd, locIKLegLenStart,
                            ctrlFootSettings, leftRight, newLayerNameIK)

        return

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

        # Adding Space Switching
        # NOTE: This is something I added from the finalizing section
        # self.makeArmSwitch(ctrlLimb, ctrlShoulder, ctrlChest, ctrlBody, ctrlRootTrans, leftRight, colourTU)
        self.makeLegSwitch(fkJntOffsetCtrls[0][1], ctrlFKHip, jntIKHip, ctrlBody, ctrlRootTrans,
                           leftRight, colourTU)

        # Organize the rig
        self.legCleanUp(fkJnts, ikJnts, ikJntsDrive, bndJnts,
                        ikOffsetCtrl, fkJntOffsetCtrls, hipIKOffsetCtrl, ctrlFKHip,
                        leftRight, ctrlFKIK, ctrlFKIKAttr, checkboxHip, footCtrlsOffsetCtrl)

        if checkGeo:
            CRU.tgpSetGeo(geoJntArray, setLayer=True)

    def makeLegSwitch(self, ctrlLimb, ctrlHipFK, ctrlHipIK, ctrlBody, ctrlRootTrans, leftRight, colourTU, *args):

        locArmFollowArray = []
        locShoulder = "LOC_" + leftRight + "legFKHipFollow"
        locArmFollowArray.append(locShoulder)
        locTorso = "LOC_" + leftRight + "legIKHipFollow"
        locArmFollowArray.append(locTorso)
        locCOG = "LOC_" + leftRight + "legCOGFollow"
        locArmFollowArray.append(locCOG)
        locWorld = "LOC_" + leftRight + "legWorldFollow"
        locArmFollowArray.append(locWorld)

        listParents = [ctrlHipFK, ctrlHipIK, ctrlBody, ctrlRootTrans]

        enumName = "fkLegFollow"
        enumVals = "fkHip:ikHip:COG:world"

        CRU.makeLimbSwitch(ctrlLimb, locArmFollowArray, listParents, enumName, enumVals, colourTU)

    def tgpMakeBC(self, *args):

        checkSelLeft = mc.radioButtonGrp("selLegType_rbg", q=True, select=True)
        print("check left: {0}".format(checkSelLeft))
        mirrorSel = mc.radioButtonGrp("selLegMirrorType_rbg", q=True, select=True)
        print("check mirror: {0}".format(mirrorSel))
        checkboxTwists = mc.checkBox("selCreateTwists_cb", q=True, v=True)
        print("check twists: {0}".format(checkboxTwists))

        checkGeo = mc.checkBox("selGeo_cb", q=True, v=True)
        print("check geo: {0}".format(checkGeo))

        jntIKHip = mc.textFieldButtonGrp("jntIKHip_tfbg", q=True, text=True)
        grpDNTTorso = mc.textFieldButtonGrp("grpTorsoDNT_tfbg", q=True, text=True)
        ctrlBody = mc.textFieldButtonGrp("ctrlBody_tfbg", q=True, text=True)
        ctrlRootTrans = mc.textFieldButtonGrp("rootTrans_tfbg", q=True, text=True)

        print("jntIKHip: {0}".format(jntIKHip))
        print("grpDNTTorso: {0}".format(grpDNTTorso))
        print("ctrlBody: {0}".format(ctrlBody))
        print("ctrlRootTrans: {0}".format(ctrlRootTrans))

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

        jntNames = mc.textFieldButtonGrp("jointLoad_tfbg", q=True, text=True)
        print("jntNames: {0}".format(jntNames))

        geoJntArray = self.jointArray
        bndJnts = self.jointArray
        print("geoJntArray: {0}".format(geoJntArray))
        checkboxHip = mc.checkBox("selSpineEnd_cb", q=True, v=True)
        print("checkboxHip: {0}".format(checkboxHip))

        try:
            jntLegRoot = self.jointArray[0]
        except:
            mc.warning("No joint selected!")
            return

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

        jntLegArray = self.jntLegArray
        print("jntLegArray: {0}".format(jntLegArray))
        jntLegFoot = [x for x in bndJnts if "Leg" in x[-3:] or "foot" in x[-4:]]
        print("jntLegFoot: {0}".format(jntLegFoot))

        # make sure the selections are not empty
        checkList = [jntNames]
        # However, editing them out is too much hassle,  it's easier just to leave them both false
        if ((checkList[0] == "")):
            mc.warning("You are missing a selection!")
            return
        else:
            CRU.createLocatorToDelete()
            if not (CRU.checkLeftRight(isLeft, jntLegRoot)):
                # if the values are not lined up properly, break out
                mc.warning("You are selecting the incorrect side for the leg")
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

            self.makeLeg(bndJnts, colourTU, leftRight, isLeft)
            return

            if mirrorRig:
                print("Mirroring")

                self.makeLeg(isLeftMirror, leftRightMirror,
                             jntLegArrayMirror,
                             checkGeo, geoJntArrayMirror, colourTUMirror, jntLegRootMirror,
                             ctrlFKIK, ctrlFKIKAttrMirror, ctrlFKHip, checkboxTwists,
                             checkboxSwitch, jntIKHip, ctrlBody, ctrlRootTrans,
                             checkboxHip=checkboxHip)
