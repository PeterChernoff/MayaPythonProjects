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
import pcCreateRigUtilities

reload(pcCreateRigUtilities)
from pcCreateRigUtilities import pcCreateRigUtilities as CRU


class pcCreateRigArms(UI):
    def __init__(self):

        self.window = "bcWindow"
        self.title = "pcRigArms"
        self.winSize = (500, 325)

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
        mc.rowColumnLayout(nc=3, cw=[(1, 125), (2, 150), (3, 150)], cs=[1, 5], rs=[1, 3],
                           cal=([1, "left"], [2, "left"], [3, "left"],))

        mc.text(l="Mirror Arm As Well?")
        # mc.setParent("..")
        mc.radioButtonGrp("selArmMirrorType_rbg", la2=["No", "Yes"], nrb=2, sl=2, cw2=[50, 50], )
        mc.text(l="")
        mc.checkBox("selCreateTwists_cb", l="Create Twists", en=True, v=True)
        mc.checkBox("selSpineEnd_cb", l="Connect To Spine", en=True, v=True)
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
        mc.text(bgc=(0.85, 0.65, 0.25), l="Shoulder: ")
        mc.textFieldButtonGrp("jointLoad_tfbg", cw=(1, 322), bl="  Load  ")

        mc.text(bgc=(0.85, 0.65, 0.25), l="FKIK Ctrl: ")
        mc.textFieldButtonGrp("ctrlLoad_tfbg", cw=(1, 322), bl="  Load  ", tx="CTRL_fkikSwitch")

        # mc.text(bgc=(0.85, 0.65, 0.25), l="COG: ")
        # mc.textFieldButtonGrp("cog_tfbg", cw=(1, 322), bl="  Load  ", tx="CTRL_COG")

        # To delete: May need to make this JNT_IK_spine_6
        mc.text(bgc=(0.85, 0.65, 0.25), l="Top Spine Joint: ")
        mc.textFieldButtonGrp("jntSpineTopLoad_tf", cw=(1, 322), bl="  Load  ", tx="JNT_IK_spine_6")

        mc.setParent("..")

        mc.separator(st="in", h=20, w=500)

        mc.rowColumnLayout(nc=2, cw=[(1, 100), (2, 370)], cs=[1, 5], rs=[1, 3])
        mc.checkBox("selGeo_cb", l="Affect Geometry", en=True, v=False)
        mc.setParent("..")

        mc.separator(st="in", h=20, w=500)

        # load buttons
        #

        mc.textFieldButtonGrp("jointLoad_tfbg", e=True, bc=self.loadSrc1Btn)
        mc.textFieldButtonGrp("ctrlLoad_tfbg", e=True, bc=self.loadCtrlBtn)
        mc.textFieldButtonGrp("jntSpineTopLoad_tf", e=True, bc=self.loadSrc2Btn)
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
        self.jntSel = self.tgpLoadTxBtn("jointLoad_tfbg", "joint")
        print(self.jntSel)

    def loadSrc2Btn(self):
        self.ctrlSel = self.tgpLoadJntSpine("jntSpineTopLoad_tf")
        print(self.ctrlSel)

    def loadSrc3Btn(self):
        self.grpSel = self.tgpLoadRigBtn("jointRigSpine_tfbg")
        print(self.grpSel)

    def loadSrc4Btn(self):
        self.grpSel2 = self.tgpLoadCOGBtn("cog_tfbg")
        print(self.grpSel2)

    def loadCtrlBtn(self, loadBtn):
        self.selLoad = []
        # self.selLoad = mc.ls(sl=True, fl=True, type="nurbsCurve")
        self.selLoad = mc.ls(sl=True, fl=True, type="transform")

        if (len(self.selLoad) != 1):
            mc.warning("Select only the Control")
            return
        else:
            selName = self.selLoad[0]
            mc.textFieldButtonGrp(loadBtn, e=True, tx=selName)
            print(selName)

    def tgpLoadRigBtn(self, loadBtn):
        self.selLoad = []
        # self.selLoad = mc.ls(sl=True, fl=True, type="nurbsCurve")
        self.selLoad = mc.ls(sl=True, fl=True, type="transform")

        if (len(self.selLoad) != 1):
            mc.warning("Select only the rig Group")
            return
        else:
            selName = self.selLoad[0]
            mc.textFieldButtonGrp(loadBtn, e=True, tx=selName)

    def tgpLoadCOGBtn(self, loadBtn):
        self.selLoad = []
        # self.selLoad = mc.ls(sl=True, fl=True, type="nurbsCurve")
        self.selLoad = mc.ls(sl=True, fl=True, type="transform")

        if (len(self.selLoad) != 1):
            mc.warning("Select only the COG Control")
            return
        else:
            selName = self.selLoad[0]
            mc.textFieldButtonGrp(loadBtn, e=True, tx=selName)

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
            self.jointArray = [x for x in self.jointArray if "End" not in x[-3:]]
            self.jointArmArray = [x for x in self.jointArray if "Arm" in x[-3:]]
            self.jointRoot = self.selLoad[0]
            self.jointClavicle = [x for x in self.jointArray if "clavicle" in x]
            self.jointScapula = [x for x in self.jointArray if "scapula" in x]

        return self.jointArray

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

    def tgpCreateLimbFKIFList(self, jntsTemp, textToReplace="", textReplacement="", stripLastVal=0, deleteThis=True,
                              renameThis=True, addToEnd="", *args):
        jntsReturn = []
        # creates a set of values. Normally, we want to delete, but we can also create a list from the values that simply don't include problematic node
        stripLastVal1 = stripLastVal * (-1)
        for i in range(len(jntsTemp)):
            toTest = jntsTemp[i]
            if mc.objectType(toTest) == "joint":
                if "Twist" in toTest:
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

    def tgpSetDriverArmFKIKSwitch(self, driver, driverAttr, driven, *args):
        w0w1Attr = mc.listAttr(driven)[-2:]
        self.setDriverDrivenValues(driver, driverAttr, driven, w0w1Attr[0], drivenValue=0, driverValue=1,
                                   modifyBoth="linear")
        self.setDriverDrivenValues(driver, driverAttr, driven, w0w1Attr[0], drivenValue=1, driverValue=0,
                                   modifyBoth="linear")
        self.setDriverDrivenValues(driver, driverAttr, driven, w0w1Attr[1], drivenValue=0, driverValue=0,
                                   modifyBoth="linear")
        self.setDriverDrivenValues(driver, driverAttr, driven, w0w1Attr[1], drivenValue=1, driverValue=1,
                                   modifyBoth="linear")

    def tgpAutoClavicleRotate(self, autoClav, targetLimb, ctrlClav, autoClavVal, *args):
        str = ""
        axes = ["X", "Y", "Z"]
        for ax in axes:
            # AUTO_CTRL_l_clavicle.rotateX = JNT_l_upperArm.rotateX * CTRL_l_clavicle.autoClavicle;
            str += "{0}.rotate{1} = {2}.rotate{1} * {3}.{4};\n".format(autoClav, ax, targetLimb, ctrlClav, autoClavVal)
        return str

    def tgpAutoScapulaRotate(self, autoScap, targetLimb, ctrlScap, autoScapVal, *args):

        # AUTO_CTRL_l_scapula.rotateX = JNT_l_shoulder.rotateZ * CTRL_l_scapula.autoScapula;

        str = "{0}.rotateX = {1}.rotateZ * {2}.{3};\n".format(autoScap, targetLimb, ctrlScap, autoScapVal)

        return str

    def tgpSetGeo(self, geoJntArray, *args):
        for i in range(len(geoJntArray)):
            try:

                theParent = geoJntArray[i]
                geoName = theParent.replace("JNT_", "GEO_")
                mc.parent(geoName, theParent)
                pivotTranslate = mc.xform(theParent, q=True, ws=True, rotatePivot=True)
                mc.makeIdentity(geoName, a=True, t=True, r=True, s=True)
                mc.xform(geoName, ws=True, pivots=pivotTranslate)

            except:
                mc.warning("Geo not properly named or available")

    def makeArm(self, isLeft, leftRight,
                jntArmArray, jntClavicle, jntScapula,
                geoJntArray, colourTU, jntShoulderRoot,
                ctrlFKIK, ctrlFKIKAttr, jntSpine6, checkboxTwists, makeExpression, makeTwistJnts, checkboxSpine,
                toReplace="", toReplaceWith="", *args):

        # Create the joint twists
        if checkboxTwists:
            # xprNameTwist, twistExpression, geoJntArray = self.makeTwists(3, leftRight, jntArmArray, geoJntArray, makeExpression, makeTwistJnts)
            xprNameTwist, twistExpression, geoJntArray = self.makeTwists(3, leftRight, jntArmArray, geoJntArray)

        # affect geo TO DELETE need to adjust this so it's when the geo is selected

        bndJnts, fkJnts, ikJnts = self.getBndFkIkJnts(jntArmArray[0], toReplace, toReplaceWith)

        fkLen = len(fkJnts)
        ikLen = len(ikJnts)
        bndLen = len(bndJnts)

        if bndLen != fkLen or bndLen != ikLen:
            mc.warning("Your arm joints are somehow not equal")
            return
        else:
            ikFkJntConstraints = []
            for i in range(bndLen):
                temp = mc.orientConstraint(fkJnts[i], ikJnts[i], bndJnts[i])[0]
                ikFkJntConstraints.append(temp)

        for i in range(len(ikFkJntConstraints)):
            self.tgpSetDriverArmFKIKSwitch(ctrlFKIK, ctrlFKIKAttr, ikFkJntConstraints[i])

        # we want to create FK controls for the limbs except the end
        armLength, fkJntOffsetCtrls = self.createArmFKs(fkJnts, colourTU)

        # create the shoulder control
        shoulderOffsetCtrl = self.setupShoulder(jntShoulderRoot, bndJnts[0], fkJntOffsetCtrls[0][0], colourTU)

        # create the clavicle
        if jntClavicle:
            clavicleOffsetCtrl = self.setupClavicle(jntClavicle[0], colourTU, leftRight, shoulderOffsetCtrl[1])

        # create the scapula
        if jntScapula:
            scapulaOffsetCtrl = self.setupScapula(jntScapula[0], colourTU, leftRight, shoulderOffsetCtrl[1],
                                                  jntShoulderRoot)

        # for testing purposes only, setting the IK to active:
        # mc.setAttr("{0}.{1}".format(ctrlFKIK, ctrlFKIKAttr), 0.5)


        # create the IKs
        ikOffsetCtrl, ikArms, ikJntsDrive, ikSide = self.createArmIK(ikJnts, leftRight, colourTU, isLeft)
        # create the twists
        self.setupIkElblowArmTwist(ikOffsetCtrl[1], ikJnts[1], ikArms[0], isLeft)

        # change the rotation order
        rotationChange = [ikJnts[1], self.jointArmArray[1], fkJnts[1], ikJntsDrive[1], fkJntOffsetCtrls[1][1]]

        self.changeRotateOrder(rotationChange, "YZX")

        # create elbow control
        elbowOffsetCtrl = self.createElbow(ikJntsDrive, leftRight, armLength, ikArms[0], isLeft)

        # Organize the rig
        self.armCleanUp(fkJnts[0], ikJnts[0], ikJntsDrive[0], jntShoulderRoot, checkboxSpine,
                        shoulderOffsetCtrl, scapulaOffsetCtrl, clavicleOffsetCtrl,
                        ikOffsetCtrl, elbowOffsetCtrl, ikArms[0], jntSpine6,
                        ikSide, fkJntOffsetCtrls, ctrlFKIK, ctrlFKIKAttr)

    # def makeTwists(self, numTwists, leftRight, jntArmArray, geoJntArray, makeExpression, makeTwistJnts, *args):
    def makeTwists(self, numTwists, leftRight, jntArmArray, geoJntArray, *args):
        numTwistsPlus1 = numTwists + 1
        twists = numTwists
        twistJnts = []
        twistExpression = ""
        for i in range(len(jntArmArray)):
            twistJntsSubgroup = []
            val = str(jntArmArray[i])
            nextJnt = mc.listRelatives(val, c=True, type="joint")[0]
            # if makeTwistJnts:
            nextJntYVal = mc.getAttr("{0}.ty".format(nextJnt))
            nextJntIncrement = nextJntYVal / (numTwistsPlus1)
            twistJnt = mc.duplicate(val, po=True, n="ToDelete")

            # create the joint twists at the proper location
            for x in range(twists):
                valx = x + 1
                twistTempName = "{0}Twist{1}".format(val, valx)

                # if makeTwistJnts:
                twistTemp = mc.duplicate(twistJnt, n=twistTempName)

                mc.parent(twistTemp, jntArmArray[i])
                mc.setAttr("{0}.ty".format(twistTempName), nextJntIncrement * valx)
                twistJntsSubgroup.append(twistTemp[0])

                twistInverse = 1.0 / (numTwistsPlus1)
                # if makeExpression:
                twistExpression += "{0}.rotateY = {1}.rotateY * {2};\n".format(twistTempName, nextJnt,
                                                                               valx * twistInverse)
                geoJntArray.append(twistTempName)

            # if makeTwistJnts:
            mc.delete(twistJnt)

            twistJnts.append(twistJntsSubgroup)

            # if makeExpression:
            twistExpression += "\n"

            # change to account for the limb
        xprNameTwist = "expr_" + leftRight + "armTwist"  # changes to account for the left or right

        # if makeExpression:
        mc.expression(s=twistExpression, n=xprNameTwist)

        return xprNameTwist, twistExpression, geoJntArray

    def getBndFkIkJnts(self, jointArmArray0, toReplace="", toReplaceWith="", *args):
        bndJntsTemp = mc.listRelatives(jointArmArray0, type="joint", ad=True)
        bndJnts = self.tgpCreateLimbFKIFList(bndJntsTemp, deleteThis=False, renameThis=False)
        bndJnts.append(jointArmArray0)
        bndJnts.reverse()

        ikJntsTemp = mc.duplicate(jointArmArray0, rc=True)
        ikJntRoot = ikJntsTemp[0]
        mc.parent(ikJntRoot, w=True)

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

    def setupIkElblowArmTwist(self, ikOffsetCtrl1, ikJnts1, ikArms0, isLeft, *args):
        elbowTwistAttr = "elbowTwist"
        mc.addAttr(ikOffsetCtrl1, longName=elbowTwistAttr, at="float", k=True)

        mc.connectAttr("{0}.{1}".format(ikOffsetCtrl1, elbowTwistAttr), ikJnts1 + ".rotateY")

        armTwistAttr = "armTwist"
        mc.addAttr(ikOffsetCtrl1, longName=armTwistAttr, at="float", k=True)

        ikCtrlArmTwistNode = "{0}_{1}_md".format(ikOffsetCtrl1, armTwistAttr)
        mc.shadingNode("multiplyDivide", n=ikCtrlArmTwistNode, au=True)

        # creates nodes that will affect whether or not the twist will go one way or another
        mc.setAttr("{0}.operation".format(ikCtrlArmTwistNode), 2)
        if isLeft:
            mc.setAttr("{0}.i2x".format(ikCtrlArmTwistNode), 1)
        else:
            mc.setAttr("{0}.i2x".format(ikCtrlArmTwistNode), -1)

        mc.connectAttr("{0}.{1}".format(ikOffsetCtrl1, armTwistAttr), ikCtrlArmTwistNode + ".i1x")
        mc.connectAttr("{0}.ox".format(ikCtrlArmTwistNode), ikArms0 + ".twist")

    def createElbow(self, ikJntsDrive, leftRight, armLength, ikArms0, isLeft, *args):

        elbowName = "CTRL_" + leftRight + "elbow"

        elbowOffsetCtrl = []
        elbowOffsetCtrl.append(mc.group(n="OFFSET_" + elbowName, w=True, em=True))
        elbowOffsetCtrl.append(mc.spaceLocator(p=(0, 0, 0), name=elbowName)[0])
        elbowOffsetCtrl.append(mc.group(n="AUTO_" + elbowName, w=True, em=True))

        mc.parent(elbowOffsetCtrl[2], elbowOffsetCtrl[0])
        mc.parent(elbowOffsetCtrl[1], elbowOffsetCtrl[2])

        toDelete = mc.pointConstraint(ikJntsDrive, elbowOffsetCtrl[0])
        toDelete2 = mc.aimConstraint(ikJntsDrive[1], elbowOffsetCtrl[0], aim=(0, 0, 1))

        mc.delete(toDelete, toDelete2)
        print(armLength)

        if not isLeft:
            armLength = -armLength

        mc.move(armLength / 2, elbowOffsetCtrl[0], z=True, os=True)

        mc.poleVectorConstraint(elbowOffsetCtrl[1], ikArms0)

        return elbowOffsetCtrl

    def createArmFKs(self, fkJnts, colourTU, *args):
        # we want to create FK controls for the limbs except the end
        fkJntOffsetCtrls = []
        for i in range(len(fkJnts[:-1])):
            temp = fkJnts[i]

            # def createCTRLs(self, s, size=3, prnt=False, ornt=False, pnt=False, orientVal=(1, 0, 0), colour=5, sections=None):
            fkJntOffsetCtrls.append(CRU.createCTRLs(temp, size=9, ornt=True, colour=colourTU, orientVal=(0, 1, 0)))
            armLength = mc.getAttr("{0}.ty".format(fkJnts[i + 1]))
            mc.select(fkJntOffsetCtrls[i][1] + ".cv[:]")
            mc.move(0, armLength * 0.5, 0, r=True, ls=True)

        # parent the fk lower arm controls under the fk upper arm controls
        mc.parent(fkJntOffsetCtrls[1][0], fkJntOffsetCtrls[0][1])

        return armLength, fkJntOffsetCtrls

    def setupShoulder(self, jntShoulderRoot, bndJnts0, fkJntOffsetCtrls00, colourTU, *args):
        shoulderOffsetCtrl = CRU.createCTRLs(jntShoulderRoot, size=5, ornt=True, colour=colourTU)
        shoulderLength = mc.getAttr("{0}.ty".format(bndJnts0))

        mc.select(shoulderOffsetCtrl[1] + ".cv[:]")
        mc.move(-shoulderLength * 0.65, shoulderLength * 0.8, 0, r=True, ls=True)

        mc.parent(fkJntOffsetCtrls00, shoulderOffsetCtrl[1])

        return shoulderOffsetCtrl

    def setupClavicle(self, jointClavicle0, colourTU, leftRight, shoulderOffsetCtrl1, *args):
        jntClav = jointClavicle0
        childClavicle = mc.listRelatives(jntClav, c=True, type="joint")[0]
        clavLength = mc.getAttr("{0}.ty".format(childClavicle))
        clavicleOffsetCtrl = CRU.createCTRLs(jntClav, size=6, ornt=True, colour=colourTU, orientVal=(0, 0, 1))
        mc.select(clavicleOffsetCtrl[1] + ".cv[:]")
        mc.move(clavLength * 0.5, clavLength * 0.5, 0, r=True, ls=True)
        autoAttrName = "autoClavicle"
        mc.addAttr(clavicleOffsetCtrl, longName=autoAttrName, at="float", k=True, min=0, max=1, dv=0.05)
        autoName = clavicleOffsetCtrl[2]
        xprNameClav = "expr_" + leftRight + "clavicle"

        # AUTO_CTRL_l_clavicle.rotateX = JNT_l_upperArm.rotateX * CTRL_l_clavicle.autoClavicle;
        exprStringClav = self.tgpAutoClavicleRotate(autoName, self.jointArmArray[0], clavicleOffsetCtrl[1],
                                                    autoAttrName)

        mc.expression(s=exprStringClav, n=xprNameClav)
        mc.parent(clavicleOffsetCtrl[0], shoulderOffsetCtrl1)

        return clavicleOffsetCtrl

    def setupScapula(self, jointScapula0, colourTU, leftRight, shoulderOffsetCtrl1, jntShoulderRoot, *args):
        jntScap = jointScapula0
        childScap = mc.listRelatives(jntScap, c=True, type="joint")[0]
        scapLength = mc.getAttr("{0}.ty".format(childScap))
        scapulaOffsetCtrl = CRU.createCTRLs(jntScap, size=6, ornt=True, colour=colourTU, orientVal=(1, 0, 0),
                                            sectionsTU=8)

        mc.select(scapulaOffsetCtrl[1] + ".cv[:]")
        mc.move(-scapLength * 0.5, scapLength * 0.5, 0, r=True, ls=True)
        autoAttrName = "autoScapula"
        mc.addAttr(scapulaOffsetCtrl, longName=autoAttrName, at="float", k=True, min=0, max=1, dv=0.5)
        autoName = scapulaOffsetCtrl[2]
        xprNameScap = "expr_" + leftRight + "scapula"

        # AUTO_CTRL_l_scapula.rotateX = JNT_l_shoulder.rotateZ * CTRL_l_scapula.autoScapula;
        exprStringScap = self.tgpAutoScapulaRotate(autoName, jntShoulderRoot, scapulaOffsetCtrl[1], autoAttrName)

        mc.expression(s=exprStringScap, n=xprNameScap)
        mc.parent(scapulaOffsetCtrl[0], shoulderOffsetCtrl1)

        return scapulaOffsetCtrl

    def createArmIK(self, ikJnts, leftRight, colourTU, isCopy, isLeft, *args):

        if isCopy:
            # if we're using the copy, we just want to get the list
            ikJntsDrive = []
            for ikJ in ikJnts:
                ikJntVal = ikJ + "Drive"
                ikJntsDrive.append(ikJntVal)
        else:
            ikJntsTDriveTemp = mc.duplicate(ikJnts[0], rc=True)
            ikJntsDrive = self.tgpCreateLimbFKIFList(ikJntsTDriveTemp, addToEnd="Drive", stripLastVal=1)

        ikSide = leftRight + "arm"

        ikArmName = "IK_" + ikSide
        effArmName = "EFF_" + ikSide
        ikArms = mc.ikHandle(n=ikArmName, sj=ikJntsDrive[0], ee=ikJntsDrive[-1], sol="ikRPsolver")
        mc.rename(ikArms[1], effArmName)

        # fkJntOffsetCtrls.append(self.createCTRLs(temp, size=9, ornt=True, colour=colourTU, orientVal=(0, 1, 0)))
        ikOffsetCtrl = self.createCTRLs(ikArms[0], 5, pnt=True, colour=colourTU, sectionsTU=6, addPrefix=True)

        mc.select(ikOffsetCtrl[1] + ".cv[:]")
        if isLeft:
            mc.rotate(0, "-25deg", "-25deg", r=True)
        else:
            mc.rotate(0, "25deg", "25deg", r=True)

        fkOrntUpperArm1 = mc.orientConstraint(ikJntsDrive[0], ikJnts[0])[0]
        fkOrntLowerArm1 = mc.orientConstraint(ikJntsDrive[1], ikJnts[1], skip="y")[0]

        return ikOffsetCtrl, ikArms, ikJntsDrive, ikSide

    def armCleanUp(self, fkJnts0, ikJnts0, ikJntsDrive0, jntShoulderRoot, checkboxSpine,
                   shoulderOffsetCtrl, scapulaOffsetCtrl, clavicleOffsetCtrl,
                   ikOffsetCtrl, elbowOffsetCtrl, ikArms0, jntSpine6, ikSide, isCopy, fkJntOffsetCtrls, ctrlFKIK,
                   ctrlFKIKAttr, *args):
        # TO DELETE: come back to make the elbow invisible
        if not isCopy:
            # since these joints are already parented if it's a copy, we just skip
            mc.parent(fkJnts0, ikJnts0, ikJntsDrive0, jntShoulderRoot)

        if checkboxSpine:
            # TO DELETE: May switch out to  JNT_IK_spine_6 (or second to last spine). Need to have Maintain offset)
            # mc.parentConstrain(shoulderOffsetCtrl[0], JNT_IK_spine_6,  mo=True)
            mc.parentConstraint(jntSpine6, shoulderOffsetCtrl[0])

        mc.pointConstraint(shoulderOffsetCtrl[1], jntShoulderRoot)

        # group OFFSET_CTRL_IK_l_arm, OFFSET_CTRL_l_elbow into GRP_CTRL_IK_l_arm
        ikGrpCtrlName = "GRP_CTRL_IK_" + ikSide
        ikGrpCtrl = mc.group(n=ikGrpCtrlName, w=True, em=True)

        mc.parent(ikOffsetCtrl[0], elbowOffsetCtrl[0], ikGrpCtrl)

        # group IK_l_arm, JNT_l_shouder into GRP_rig_l_arm
        armGrpRigName = "GRP_rig_" + ikSide
        armRigGrp = mc.group(n=armGrpRigName, w=True, em=True)

        mc.parent(ikArms0, jntShoulderRoot, armRigGrp)

        # locking and hiding the IK controls
        CRU.lockHideCtrls(ikOffsetCtrl[1], rotate=True, scale=True)
        for fkJntOC in fkJntOffsetCtrls:
            CRU.lockHideCtrls(fkJntOC[1], translate=True, scale=True)
        CRU.lockHideCtrls(shoulderOffsetCtrl[1], translate=True, scale=True)
        CRU.lockHideCtrls(scapulaOffsetCtrl[1], translate=True, scale=True)
        CRU.lockHideCtrls(clavicleOffsetCtrl[1], translate=True, scale=True)

        # linking JNT visibility to their respective parent
        mc.connectAttr("{0}.visibility".format(ikOffsetCtrl[1]), "{0}.visibility".format(ikArms0))
        mc.connectAttr("{0}.visibility".format(ikOffsetCtrl[1]), "{0}.visibility".format(ikJnts0))
        mc.connectAttr("{0}.visibility".format(ikOffsetCtrl[1]), "{0}.visibility".format(ikJntsDrive0))
        mc.connectAttr("{0}.visibility".format(ikOffsetCtrl[1]), "{0}.visibility".format(elbowOffsetCtrl[1]))
        mc.connectAttr("{0}.visibility".format(fkJntOffsetCtrls[0][1]), "{0}.visibility".format(fkJnts0))

        # set the FK to visible when not ctrlFKIK not 1 for arm attribute

        tangentToUse = ["linear", "step"]
        visMin = 0.001

        self.setDriverDrivenValues(ctrlFKIK, ctrlFKIKAttr, fkJntOffsetCtrls[0][1], "visibility", drivenValue=True,
                                   driverValue=0, modifyInOut=tangentToUse)
        self.setDriverDrivenValues(ctrlFKIK, ctrlFKIKAttr, fkJntOffsetCtrls[0][1], "visibility", drivenValue=True,
                                   driverValue=1 - visMin, modifyInOut=tangentToUse)
        self.setDriverDrivenValues(ctrlFKIK, ctrlFKIKAttr, fkJntOffsetCtrls[0][1], "visibility", drivenValue=False,
                                   driverValue=1, modifyInOut=tangentToUse)

        tangentToUse = ["linear", "step"]
        # set the IK to visible when not ctrlFKIK not 0 for arm attribute
        self.setDriverDrivenValues(ctrlFKIK, ctrlFKIKAttr, ikOffsetCtrl[1], "visibility", drivenValue=False,
                                   driverValue=0, modifyInOut=tangentToUse)
        self.setDriverDrivenValues(ctrlFKIK, ctrlFKIKAttr, ikOffsetCtrl[1], "visibility", drivenValue=True,
                                   driverValue=visMin, modifyInOut=tangentToUse)
        self.setDriverDrivenValues(ctrlFKIK, ctrlFKIKAttr, ikOffsetCtrl[1], "visibility", drivenValue=True,
                                   driverValue=1, modifyInOut=tangentToUse)

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

    def tgpMakeBC(self, *args):

        checkSelLeft = mc.radioButtonGrp("selArmType_rbg", q=True, select=True)
        mirrorSel = mc.radioButtonGrp("selArmMirrorType_rbg", q=True, select=True)

        checkboxTwists = mc.checkBox("selCreateTwists_cb", q=True, v=True)

        checkGeo = mc.checkBox("selGeo_cb", q=True, v=True)

        self.jntNames = mc.textFieldButtonGrp("jointLoad_tfbg", q=True, text=True)
        ctrlFKIK = mc.textFieldButtonGrp("ctrlLoad_tfbg", q=True, text=True)

        geoJntArray = self.jointArray
        checkboxSpine = mc.checkBox("selSpineEnd_cb", q=True, v=True)

        if checkboxSpine:
            jntSpine6 = mc.textFieldButtonGrp("jntSpineTopLoad_tf", q=True, text=True)
        else:
            jntSpine6 = None

        print(jntSpine6)

        try:
            jntShoulderRoot = self.jointArray[0]
        except:
            mc.warning("No joint selected!")
            return

        print(mirrorSel)
        if mirrorSel == 1:
            mirrorRig = False
        else:
            mirrorRig = True

        listCtrlFKIKAttr = ["l_arm", "r_arm", "l_leg", "r_leg"]
        if checkSelLeft == 1:
            isLeft = True
            leftRight = "l_"
            leftRightMirror = "r_"
            colourTU = 14
            colourTUMirror = 13
            ctrlFKIKAttr = listCtrlFKIKAttr[0]
            ctrlFKIKAttrMirror = listCtrlFKIKAttr[1]
        else:
            isLeft = False
            leftRight = "r_"
            leftRightMirror = "l_"
            colourTU = 13
            colourTUMirror = 14
            ctrlFKIKAttr = listCtrlFKIKAttr[1]
            ctrlFKIKAttrMirror = listCtrlFKIKAttr[0]

        toReplace = "_" + leftRight
        toReplaceWith = "_" + leftRightMirror

        if ctrlFKIK:
            for i in range(len(listCtrlFKIKAttr)):
                try:
                    mc.addAttr(ctrlFKIK, longName=listCtrlFKIKAttr[i], at="float", k=True, min=0, max=1, dv=0)
                except:
                    mc.warning("Error, attribute may already exist")
        # self.geoNames = mc.textFieldButtonGrp("GeoLoad_tfbg", q=True, text=True)

        # make sure the selections are not empty
        checkList = [self.jntNames]

        if ((checkList[0] == "")):
            mc.warning("You are missing a selection!")
            return
        else:

            if mirrorRig:
                pass
            
            
            self.makeArm(isLeft, leftRight,
                         self.jointArmArray, self.jointClavicle, self.jointScapula,
                         geoJntArray, colourTU, jntShoulderRoot,
                         ctrlFKIK, ctrlFKIKAttr, jntSpine6, checkboxTwists,
                         makeExpression=True, makeTwistJnts=True, isCopy=False,
                         checkboxSpine=checkboxSpine)

            print(mirrorRig)
            if mirrorRig:

                # TO DELETE: Consider changing things so that you duplicate the arm before creating the rest of the rig, so we don't have to constantly check to see if we've already made it before

                print("I got here!")
                toReplace = "_" + leftRight
                toReplaceWith = "_" + leftRightMirror
                mirrorBase = mc.mirrorJoint(jntShoulderRoot, mirrorYZ=True, mirrorBehavior=True,
                                            searchReplace=[toReplace, toReplaceWith])
                jntShoulderRootMirror = mirrorBase[0]
                mc.parent(jntShoulderRootMirror, w=True)
                for mb in mirrorBase:
                    if mc.objectType(mb) != "joint":
                        mc.delete(mb)
                    else:
                        geoJntArray.append(mb)
                isLeftMirror = not isLeft
                # we need to create mirror names for the arms
                jntArmArrayMirror = []
                for jntAA in self.jointArmArray:
                    jntArmArrayMirror.append(jntAA.replace(toReplace, toReplaceWith))
                jntClavicleMirror = []
                for clav in self.jointClavicle:
                    jntClavicleMirror.append(clav.replace(toReplace, toReplaceWith))
                jntScapulaMirror = []
                for scap in self.jointScapula:
                    jntScapulaMirror.append(scap.replace(toReplace, toReplaceWith))

                self.makeArm(isLeftMirror, leftRightMirror,
                             jntArmArrayMirror, jntClavicleMirror, jntScapulaMirror,
                             geoJntArray, colourTUMirror, jntShoulderRootMirror,
                             ctrlFKIK, ctrlFKIKAttrMirror, jntSpine6, checkboxTwists,
                             makeExpression=True, makeTwistJnts=False, isCopy=True,
                             checkboxSpine=checkboxSpine, toReplace=toReplace, toReplaceWith=toReplaceWith)

            if checkGeo:
                self.tgpSetGeo(geoJntArray)
