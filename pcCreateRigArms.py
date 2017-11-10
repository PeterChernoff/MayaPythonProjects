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


class pcCreateRigArms(UI):
    def __init__(self):

        self.window = "bcWindow"
        self.title = "pcRigArms"
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

        mc.text(bgc=(0.85, 0.65, 0.25), l="Top Spine Joint: ")
        mc.textFieldButtonGrp("jntSpineTopLoad_tf", cw=(1, 322), bl="  Load  ", tx="JNT_IK_spine_6")

        mc.setParent("..")

        mc.separator(st="in", h=20, w=500)

        mc.rowColumnLayout(nc=2, cw=[(1, 100), (2, 370)], cs=[1, 5], rs=[1, 3])
        mc.checkBox("selGeo_cb", l="Affect Geometry", en=True, v=True)
        mc.setParent("..")

        mc.separator(st="in", h=20, w=500)

        # load buttons
        mc.textFieldButtonGrp("jointLoad_tfbg", e=True, bc=self.loadSrc1Btn)
        mc.textFieldButtonGrp("jntSpineTopLoad_tf", e=True, bc=self.loadSrc2Btn)
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
        self.jntSel = self.tgpLoadTxBtn("jointLoad_tfbg", "joint")
        print(self.jntSel)

    def loadSrc2Btn(self):
        self.ctrlSel = self.tgpLoadJntSpine("jntSpineTopLoad_tf", "joint")
        print(self.ctrlSel)

    def loadSrc3Btn(self):
        print("hello")
        self.grpSel = self.tgpLoadCtrl("ctrlLoad_tfbg")
        print(self.grpSel)

    def tgpLoadCtrl(self, loadBtn):
        self.selLoad = []
        self.selLoad = mc.ls(sl=True, fl=True)

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

    def tgpLoadJntSpine(self, loadBtn, myType):
        # hierarchy
        self.selLoad = []
        self.selLoad = mc.ls(sl=True, fl=True, type=myType)

        if (len(self.selLoad) != 1):
            mc.warning("Select only the root joint")
            return
        else:

            selName = self.selLoad[0]
            mc.textFieldButtonGrp(loadBtn, e=True, tx=selName)

            # get the children joints
            self.parent = self.selLoad[0]

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
        CRU.setDriverDrivenValues(driver, driverAttr, driven, w0w1Attr[0], drivenValue=0, driverValue=1,
                                  modifyBoth="linear")
        CRU.setDriverDrivenValues(driver, driverAttr, driven, w0w1Attr[0], drivenValue=1, driverValue=0,
                                  modifyBoth="linear")
        CRU.setDriverDrivenValues(driver, driverAttr, driven, w0w1Attr[1], drivenValue=0, driverValue=0,
                                  modifyBoth="linear")
        CRU.setDriverDrivenValues(driver, driverAttr, driven, w0w1Attr[1], drivenValue=1, driverValue=1,
                                  modifyBoth="linear")

    def tgpAutoClavicleRotate(self, autoClav, targetLimb, ctrlClav, autoClavVal, *args):
        str = ""
        axes = ["X", "Y", "Z"]
        for ax in axes:
            # AUTO_CTRL_l_clavicle.rotateX = JNT_l_upperArm.rotateX * CTRL_l_clavicle.autoClavicle;
            str += "{0}.rotate{1} = {2}.rotate{1} * {3}.{4};\n".format(autoClav, ax, targetLimb, ctrlClav, autoClavVal)
        return str

    def makeArm(self, isLeft, leftRight,
                jntArmArray, jntClavicle, jntScapula,
                colourTU, jntShoulderRoot,
                ctrlFKIK, ctrlFKIKAttr, jntSpine6, checkboxTwists,
                checkboxSpine, checkGeo, geoJntArray, *args):

        # Adding the twist joints
        if checkboxTwists:
            # xprNameTwist, twistExpression, geoJntArray = self.makeTwists(3, leftRight, jntArmArray, geoJntArray, makeExpression)
            xprNameTwist, twistExpression, geoJntArray = self.makeTwists(3, leftRight, jntArmArray, geoJntArray)

        # NOTE: I use a slightly different order than the originals, leaving the SetGeo section to the lat

        # Creating FK and IK Joints
        bndJnts, fkJnts, ikJnts = self.getBndFkIkJnts(jntArmArray)

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
        shoulderOffsetCtrl = self.setupShoulder(jntShoulderRoot, bndJnts, fkJntOffsetCtrls, colourTU)

        # create the clavicle
        if jntClavicle:
            clavicleOffsetCtrl = self.setupClavicle(jntClavicle, colourTU, leftRight, shoulderOffsetCtrl)

        # create the scapula
        if jntScapula:
            scapulaOffsetCtrl = self.setupScapula(jntScapula, colourTU, leftRight, shoulderOffsetCtrl, )

        # for testing purposes only, setting the IK to active:
        mc.setAttr("{0}.{1}".format(ctrlFKIK, ctrlFKIKAttr), 0.5)

        # Setting up the IK Arm
        ikOffsetCtrl, ikArms, ikJntsDrive, ikSide = self.createArmIK(ikJnts, leftRight, colourTU, isLeft)
        # create the twists
        self.setupIkElblowArmTwist(ikOffsetCtrl, ikJnts, ikArms, isLeft)

        # change the rotation order
        rotationChange = [ikJnts[1], self.jointArmArray[1], fkJnts[1], ikJntsDrive[1], fkJntOffsetCtrls[1][1]]

        CRU.changeRotateOrder(rotationChange, "YZX")

        # Adding the Elbow Control
        elbowOffsetCtrl = self.createElbow(ikJntsDrive, leftRight, armLength, ikArms, isLeft)

        # Organize the rig
        self.armCleanUp(fkJnts, ikJnts, ikJntsDrive, jntShoulderRoot, checkboxSpine,
                        shoulderOffsetCtrl, scapulaOffsetCtrl, clavicleOffsetCtrl,
                        ikOffsetCtrl, elbowOffsetCtrl, ikArms, jntSpine6,
                        ikSide, fkJntOffsetCtrls, ctrlFKIK, ctrlFKIKAttr)

        if checkGeo:
            CRU.tgpSetGeo(geoJntArray)

    def makeTwists(self, numTwists, leftRight, jntArmArray, geoJntArray, *args):
        numTwistsPlus1 = numTwists + 1
        twists = numTwists
        twistJnts = []
        twistExpression = ""
        for i in range(len(jntArmArray)):
            twistJntsSubgroup = []
            val = str(jntArmArray[i])
            nextJnt = mc.listRelatives(val, c=True, type="joint")[0]
            nextJntYVal = mc.getAttr("{0}.ty".format(nextJnt))
            nextJntIncrement = nextJntYVal / (numTwistsPlus1)
            twistJnt = mc.duplicate(val, po=True, n="ToDelete")

            # create the joint twists at the proper location
            for x in range(twists):
                valx = x + 1
                twistTempName = "{0}Twist{1}".format(val, valx)

                twistTemp = mc.duplicate(twistJnt, n=twistTempName)

                mc.parent(twistTemp, jntArmArray[i])
                mc.setAttr("{0}.ty".format(twistTempName), nextJntIncrement * valx)
                twistJntsSubgroup.append(twistTemp[0])

                twistInverse = 1.0 / (numTwistsPlus1)

                twistExpression += "{0}.rotateY = {1}.rotateY * {2};\n".format(twistTempName, nextJnt,
                                                                               valx * twistInverse)
                geoJntArray.append(twistTempName)

            mc.delete(twistJnt)

            twistJnts.append(twistJntsSubgroup)

            twistExpression += "\n"

            # change to account for the limb
        xprNameTwist = "expr_" + leftRight + "armTwist"  # changes to account for the left or right

        mc.expression(s=twistExpression, n=xprNameTwist)

        return xprNameTwist, twistExpression, geoJntArray

    def getBndFkIkJnts(self, jointArmArray, *args):
        bndJntsTemp = mc.listRelatives(jointArmArray[0], type="joint", ad=True)
        bndJnts = self.tgpCreateLimbFKIFList(bndJntsTemp, deleteThis=False, renameThis=False)
        bndJnts.append(jointArmArray[0])
        bndJnts.reverse()

        ikJntsTemp = mc.duplicate(jointArmArray[0], rc=True)
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

    def setupIkElblowArmTwist(self, ikOffsetCtrl, ikJnts, ikArms, isLeft, *args):
        elbowTwistAttr = "elbowTwist"
        mc.addAttr(ikOffsetCtrl[1], longName=elbowTwistAttr, at="float", k=True)

        mc.connectAttr("{0}.{1}".format(ikOffsetCtrl[1], elbowTwistAttr), ikJnts[1] + ".rotateY")

        armTwistAttr = "armTwist"
        mc.addAttr(ikOffsetCtrl[1], longName=armTwistAttr, at="float", k=True)

        ikCtrlArmTwistNode = "{0}_{1}_md".format(ikOffsetCtrl[1], armTwistAttr)
        mc.shadingNode("multiplyDivide", n=ikCtrlArmTwistNode, au=True)

        # creates nodes that will affect whether or not the twist will go one way or another
        mc.setAttr("{0}.operation".format(ikCtrlArmTwistNode), 2)
        if isLeft:
            mc.setAttr("{0}.i2x".format(ikCtrlArmTwistNode), 1)
        else:
            mc.setAttr("{0}.i2x".format(ikCtrlArmTwistNode), -1)

        mc.connectAttr("{0}.{1}".format(ikOffsetCtrl[1], armTwistAttr), ikCtrlArmTwistNode + ".i1x")
        mc.connectAttr("{0}.ox".format(ikCtrlArmTwistNode), ikArms[0] + ".twist")

    def createElbow(self, ikJntsDrive, leftRight, armLength, ikArms, isLeft, *args):

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

        if not isLeft:
            armLength = -armLength

        mc.move(armLength / 2, elbowOffsetCtrl[0], z=True, os=True)

        mc.poleVectorConstraint(elbowOffsetCtrl[1], ikArms[0])

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

    def setupShoulder(self, jntShoulderRoot, bndJnts, fkJntOffsetCtrls, colourTU, *args):
        shoulderOffsetCtrl = CRU.createCTRLs(jntShoulderRoot, size=5, ornt=True, colour=colourTU)
        shoulderLength = mc.getAttr("{0}.ty".format(bndJnts[0]))

        mc.select(shoulderOffsetCtrl[1] + ".cv[:]")
        mc.move(-shoulderLength * 0.65, shoulderLength * 0.8, 0, r=True, ls=True)

        mc.parent(fkJntOffsetCtrls[0][0], shoulderOffsetCtrl[1])

        return shoulderOffsetCtrl

    def setupClavicle(self, jointClavicle, colourTU, leftRight, shoulderOffsetCtrl, *args):
        jntClav = jointClavicle[0]
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
        mc.parent(clavicleOffsetCtrl[0], shoulderOffsetCtrl[1])

        return clavicleOffsetCtrl

    def setupScapula(self, jointScapula, colourTU, leftRight, shoulderOffsetCtrl, *args):
        jntScap = jointScapula[0]
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

        # AUTO_CTRL_l_scapula.rotateX = -1*CTRL_l_shoulder.rotateZ * CTRL_l_scapula.autoScapula;
        exprStringScap = "{0}.rotateX = -1*{1}.rotateZ * {2}.{3};\n".format(autoName, shoulderOffsetCtrl[1],
                                                                            scapulaOffsetCtrl[1], autoAttrName)

        mc.expression(s=exprStringScap, n=xprNameScap)
        mc.parent(scapulaOffsetCtrl[0], shoulderOffsetCtrl[1])

        return scapulaOffsetCtrl

    def createArmIK(self, ikJnts, leftRight, colourTU, isLeft, *args):

        ikJntsTDriveTemp = mc.duplicate(ikJnts[0], rc=True)
        ikJntsDrive = self.tgpCreateLimbFKIFList(ikJntsTDriveTemp, addToEnd="Drive", stripLastVal=1)

        ikSide = leftRight + "arm"

        ikArmName = "IK_" + ikSide
        effArmName = "EFF_" + ikSide
        ikArms = mc.ikHandle(n=ikArmName, sj=ikJntsDrive[0], ee=ikJntsDrive[-1], sol="ikRPsolver")
        mc.rename(ikArms[1], effArmName)
        ikArms[1] = effArmName

        # fkJntOffsetCtrls.append(CRU.createCTRLs(temp, size=9, ornt=True, colour=colourTU, orientVal=(0, 1, 0)))
        ikOffsetCtrl = CRU.createCTRLs(ikArms[0], pnt=True, colour=colourTU, addPrefix=True, boxDimensionsLWH=[5, 5, 5])

        fkOrntUpperArm1 = mc.orientConstraint(ikJntsDrive[0], ikJnts[0])[0]
        fkOrntLowerArm1 = mc.orientConstraint(ikJntsDrive[1], ikJnts[1], skip="y")[0]

        return ikOffsetCtrl, ikArms, ikJntsDrive, ikSide

    def armCleanUp(self, fkJnts, ikJnts, ikJntsDrive, jntShoulderRoot, checkboxSpine,
                   shoulderOffsetCtrl, scapulaOffsetCtrl, clavicleOffsetCtrl,
                   ikOffsetCtrl, elbowOffsetCtrl, ikArms, jntSpine6, ikSide, fkJntOffsetCtrls, ctrlFKIK,
                   ctrlFKIKAttr, *args):

        mc.parent(fkJnts[0], ikJnts[0], ikJntsDrive[0], jntShoulderRoot)

        if checkboxSpine:
            mc.parentConstraint(jntSpine6, shoulderOffsetCtrl[0], mo=True)

        mc.pointConstraint(shoulderOffsetCtrl[1], jntShoulderRoot)

        # group OFFSET_CTRL_IK_l_arm, OFFSET_CTRL_l_elbow into GRP_CTRL_IK_l_arm
        ikGrpCtrlName = "GRP_CTRL_IK_" + ikSide
        ikGrpCtrl = mc.group(n=ikGrpCtrlName, w=True, em=True)

        mc.parent(ikOffsetCtrl[0], elbowOffsetCtrl[0], ikGrpCtrl)

        # group IK_l_arm, JNT_l_shouder into GRP_jnt_l_arm
        armGrpRigName = "GRP_jnt_" + ikSide
        armRigGrp = mc.group(n=armGrpRigName, w=True, em=True)

        mc.parent(ikArms[0], jntShoulderRoot, armRigGrp)

        # creating lists to set invisible
        fksToVisible = [fkJntOffsetCtrls[0][1], fkJnts[0]]
        iksToVisible = [ikOffsetCtrl[1], ikJnts[0], ikJntsDrive[0], elbowOffsetCtrl[1]]
        tangentToUse = ["linear", "step"]
        visMin = 0.001

        # set the FK to visible when not ctrlFKIK not 1 for arm attribute
        for i in range(len(fksToVisible)):
            CRU.setDriverDrivenValues(ctrlFKIK, ctrlFKIKAttr, fksToVisible[i], "visibility", drivenValue=True,
                                      driverValue=0, modifyInOut=tangentToUse)
            CRU.setDriverDrivenValues(ctrlFKIK, ctrlFKIKAttr, fksToVisible[i], "visibility", drivenValue=True,
                                      driverValue=1 - visMin, modifyInOut=tangentToUse)
            CRU.setDriverDrivenValues(ctrlFKIK, ctrlFKIKAttr, fksToVisible[i], "visibility", drivenValue=False,
                                      driverValue=1, modifyInOut=tangentToUse)

        tangentToUse = ["linear", "step"]
        # set the IK to visible when not ctrlFKIK not 0 for arm attribute
        for i in range(len(iksToVisible)):
            CRU.setDriverDrivenValues(ctrlFKIK, ctrlFKIKAttr, iksToVisible[i], "visibility", drivenValue=False,
                                      driverValue=0, modifyInOut=tangentToUse)
            CRU.setDriverDrivenValues(ctrlFKIK, ctrlFKIKAttr, iksToVisible[i], "visibility", drivenValue=True,
                                      driverValue=visMin, modifyInOut=tangentToUse)
            CRU.setDriverDrivenValues(ctrlFKIK, ctrlFKIKAttr, iksToVisible[i], "visibility", drivenValue=True,
                                      driverValue=1, modifyInOut=tangentToUse)

        # locking and hiding the IK controls
        CRU.lockHideCtrls(ikOffsetCtrl[1], rotate=True, scale=True, visible=True)
        for fkJntOC in fkJntOffsetCtrls:
            CRU.lockHideCtrls(fkJntOC[1], translate=True, scale=True)
            CRU.lockHideCtrls(fkJntOC[1], visible=True, toLock=False)
        CRU.lockHideCtrls(shoulderOffsetCtrl[1], translate=True, scale=True, visible=True)
        CRU.lockHideCtrls(scapulaOffsetCtrl[1], translate=True, scale=True, visible=True)
        CRU.lockHideCtrls(clavicleOffsetCtrl[1], translate=True, scale=True, visible=True)
        CRU.lockHideCtrls(elbowOffsetCtrl[1], rotate=True, scale=True, visible=True)

        # hiding the visibility for the FK

        # locking and hiding the effectors and IK
        # to delete: May need to not have this hidden
        mc.setAttr("{0}.visibility".format(ikArms[0]), False)
        CRU.lockHideCtrls(ikArms[0], visible=True)
        CRU.lockHideCtrls(ikArms[1], visible=True)

        CRU.layerEdit(ikJnts, ikLayer=True, noRecurse=True)
        CRU.layerEdit(fkJnts, fkLayer=True, noRecurse=True)
        CRU.layerEdit(ikJntsDrive, ikdriveLayer=True, noRecurse=True)

    def tgpMakeBC(self, *args):

        checkSelLeft = mc.radioButtonGrp("selArmType_rbg", q=True, select=True)
        mirrorSel = mc.radioButtonGrp("selArmMirrorType_rbg", q=True, select=True)

        checkboxTwists = mc.checkBox("selCreateTwists_cb", q=True, v=True)

        checkGeo = mc.checkBox("selGeo_cb", q=True, v=True)

        self.jntNames = mc.textFieldButtonGrp("jointLoad_tfbg", q=True, text=True)
        ctrlFKIK = mc.textFieldButtonGrp("ctrlLoad_tfbg", q=True, text=True)

        geoJntArray = self.jointArray[:]
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

        jntArmArray = self.jointArmArray[:]
        jntClavicle = self.jointClavicle[:]
        jntScapula = self.jointScapula[:]

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

            # CRU.createLocatorToDelete()

            # checks if the starting joint is correct to the direction we want
            if not (CRU.checkLeftRight(isLeft, jntShoulderRoot)):
                # if the values are not lined up properly, break out
                mc.warning("You are selecting the incorrect side")
                return

            if mirrorRig:
                mirrorBase = mc.mirrorJoint(jntShoulderRoot, mirrorYZ=True, mirrorBehavior=True,
                                            searchReplace=[toReplace, toReplaceWith])
                jntShoulderRootMirror = mirrorBase[0]
                # mc.parent(jntShoulderRootMirror, w=True)
            self.makeArm(isLeft, leftRight,
                         jntArmArray, jntClavicle, jntScapula,
                         colourTU, jntShoulderRoot,
                         ctrlFKIK, ctrlFKIKAttr, jntSpine6, checkboxTwists,
                         checkboxSpine, checkGeo, geoJntArray)

            print(mirrorRig)
            if mirrorRig:

                print("Mirroring")

                isLeftMirror = not isLeft
                # we need to create mirror names for the arms
                jntArmArrayMirror = []
                for jntAA in jntArmArray:
                    jntArmArrayMirror.append(jntAA.replace(toReplace, toReplaceWith))
                jntClavicleMirror = []
                for clav in jntClavicle:
                    jntClavicleMirror.append(clav.replace(toReplace, toReplaceWith))
                jntScapulaMirror = []
                for scap in jntScapula:
                    jntScapulaMirror.append(scap.replace(toReplace, toReplaceWith))
                geoJntArrayMirror = []
                for mb in mirrorBase:

                    if mc.objectType(mb) == "joint" and "End" not in mb:
                        geoJntArrayMirror.append(mb)
                # print("geoJntArrayMirror is {0}".format(geoJntArrayMirror))
                self.makeArm(isLeftMirror, leftRightMirror,
                             jntArmArrayMirror, jntClavicleMirror, jntScapulaMirror,
                             colourTUMirror, jntShoulderRootMirror,
                             ctrlFKIK, ctrlFKIKAttrMirror, jntSpine6, checkboxTwists,
                             checkboxSpine, checkGeo, geoJntArrayMirror)
