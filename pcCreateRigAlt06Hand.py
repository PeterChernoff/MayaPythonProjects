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


class pcCreateRigAlt06Hand(UI):
    def __init__(self):

        self.window = "bcWindow"
        self.title = "pcRigHands"
        self.winSize = (500, 450)

        self.createUI()

    def createCustom(self, *args):
        # selection type

        mc.rowColumnLayout(nc=2, cw=[(1, 500), (2, 500)], cs=[1, 5], rs=[1, 3])

        mc.text(l="Select The Hand Base Joint: ")
        mc.text(l="")
        mc.separator(st="in", h=17, w=500)
        mc.setParent("..")
        mc.rowColumnLayout(nc=3, cw=[(1, 125), (2, 150), (3, 150)], cs=[1, 5], rs=[1, 3],
                           cal=([1, "left"], [2, "left"], [3, "left"],))

        mc.text(l="Mirror Hand As Well?")
        # mc.setParent("..")
        mc.radioButtonGrp("selHandMirrorType_rbg", la2=["No", "Yes"], nrb=2, sl=2, cw2=[50, 50], )
        mc.text(l="")
        mc.setParent("..")
        mc.separator(st="in", h=20, w=500)

        mc.rowColumnLayout(nc=3, cw=[(1, 100), (2, 200), (3, 150)], cs=[1, 5], rs=[1, 3],
                           cal=([1, "left"], [2, "left"], [3, "left"],))
        mc.text(l="Initial Limb: ")
        mc.radioButtonGrp("selHandType_rbg", la2=["Left", "Right"], nrb=2, sl=1, cw2=[50, 50], )
        mc.setParent("..")
        mc.separator(st="in", h=20, w=500)

        # sources
        mc.rowColumnLayout(nc=2, cw=[(1, 100), (2, 380)], cs=[1, 5], rs=[1, 3])
        mc.text(bgc=(0.85, 0.65, 0.25), l="handBase Joint: ")
        mc.textFieldButtonGrp("jntFingersLoad_tfbg", cw=(1, 322), bl="  Load  ", tx="JNT_BND_l_handBase")

        mc.text(bgc=(0.85, 0.65, 0.25), l="Palm Loc: ")
        mc.textFieldButtonGrp("locPalmLoad_tf", cw=(1, 322), bl="  Load  ", tx="LOC_l_palmInner")

        mc.text(bgc=(0.85, 0.65, 0.25), l="Arm Bind End: ")
        mc.textFieldButtonGrp("jntBindEndLoad_tf", cw=(1, 322), bl="  Load  ", tx="JNT_l_arm_bindEnd")

        mc.text(bgc=(0.85, 0.65, 0.25), l="Root Transform\nControl: ")
        mc.textFieldButtonGrp("rootTrans_tfbg", cw=(1, 322), bl="  Load  ", tx="CTRL_rootTransform_emma")

        mc.text(bgc=(0.85, 0.65, 0.25), l="Arm's Hand Joint: ")
        mc.textFieldButtonGrp("jntHandLoad_tfbg", cw=(1, 322), bl="  Load  ", tx="JNT_BND_l_hand")

        mc.text(bgc=(0.85, 0.65, 0.25), l="Arm Control\nSettings: ")
        mc.textFieldButtonGrp("ctrlSettingsLoad_tfbg", cw=(1, 322), bl="  Load  ", tx="CTRL_settings_l_arm")

        mc.setParent("..")

        mc.separator(st="in", h=20, w=500)

        mc.rowColumnLayout(nc=2, cw=[(1, 100), (2, 370)], cs=[1, 5], rs=[1, 3])
        mc.checkBox("selGeo_cb", l="Affect Geometry", en=True, v=True)

        mc.setParent("..")

        # load buttons
        #

        mc.textFieldButtonGrp("jntFingersLoad_tfbg", e=True, bc=self.loadSrc1Btn)
        mc.textFieldButtonGrp("locPalmLoad_tf", e=True, bc=self.loadSrc2Btn)
        mc.textFieldButtonGrp("jntBindEndLoad_tf", e=True, bc=self.loadSrc3Btn)
        mc.textFieldButtonGrp("rootTrans_tfbg", e=True, bc=self.loadSrc4Btn)
        mc.textFieldButtonGrp("jntHandLoad_tfbg", e=True, bc=self.loadSrc5Btn)
        mc.textFieldButtonGrp("ctrlSettingsLoad_tfbg", e=True, bc=self.loadSrc6Btn)

        self.selLoad = []
        self.jntsArray = []
        self.locArray = []
        mc.showWindow(self.window)

    def createButtonCmd(self, *args):
        self.tgpMakeBC()

    def loadSrc1Btn(self):
        self.selSrc1 = self.tgpLoadJntsBtn("jntFingersLoad_tfbg", "joint", "Hand Base Joint", ["jnt", "handBase"],
                                           "joint")
        print(self.selSrc1)

    def loadSrc2Btn(self):
        self.selSrc2 = self.tgpLoadLocsBtn("locPalmLoad_tf", "locator", "Inner Palm Locator", ["loc", "palmInner"],
                                           "locator")
        print(self.selSrc2)

    def loadSrc3Btn(self):
        self.selSrc3 = self.tgpLoadTxBtn("jntBindEndLoad_tf", "joint", "Hand Base Joint", ["jnt", "arm", "bindEnd"],
                                         "joint")
        print(self.selSrc3)

    def loadSrc4Btn(self):
        self.selSrc4 = self.tgpLoadTxBtn("rootTrans_tfbg", "nurbsCurve", "Root Transform\nControl",
                                         ["ctrl", "rootTransform"], "control")
        print(self.selSrc4)

    def loadSrc5Btn(self):
        self.selSrc5 = self.tgpLoadTxBtn("jntHandLoad_tfbg", "joint", "Hand Joint",
                                         ["jnt", "bnd", "hand", ], "joint")
        print(self.selSrc5)

    def loadSrc6Btn(self):
        self.selSrc6 = self.tgpLoadTxBtn("ctrlSettingsLoad_tfbg", "nurbsCurve", "Arm Control Setting",
                                         ["ctrl", "arm", "settings", ], "control")
        print(self.selSrc6)

    def tgpLoadLocsBtn(self, loadBtn, objectType, objectDesc, keywords, objectNickname=None):
        if objectNickname is None:
            objectNickname = objectType
        # hierarchy
        self.selLoad = []
        self.selLoad = mc.ls(sl=True, fl=True, type="transform")

        if (len(self.selLoad) != 1):
            mc.warning("Select only the {0}".format(objectDesc))
            return
        else:
            selName = self.selLoad[0]
            # get the children joints
            returner = self.tgpLoadLocMethod(selName, loadBtn, objectType, objectDesc, keywords, objectNickname)
            if returner is None:
                return None

        return self.locArray

    def tgpLoadLocMethod(self, selName, loadBtn, objectType, objectDesc, keywords, objectNickname=None):
        if objectNickname is None:
            objectNickname = objectType

        if CRU.checkObjectType(selName) != objectType:
            mc.warning("{0} should be a {1}".format(objectDesc, objectNickname))
            return

        if not all(word.lower() in selName.lower() for word in keywords):
            mc.warning("That is the wrong {0}. Select the {1}".format(objectNickname, objectDesc))
            return
        mc.textFieldButtonGrp(loadBtn, e=True, tx=selName)

        self.parent = selName
        self.child = mc.listRelatives(selName, ad=True, type="transform")
        # collect the joints in an array
        self.locArray = [self.parent]
        # reverse the order of the children joints
        self.child.reverse()

        # add to the current list
        self.locArray.extend(self.child)
        locArraySorted = []
        for i in range(len(self.locArray)):
            sels = mc.listRelatives(self.locArray[i], c=True, s=True)
            if objectType in mc.objectType(sels) or objectType == mc.objectType(sels):
                locArraySorted.append(self.locArray[i])

        self.locRoot = selName
        self.locArray = locArraySorted

        return self.locArray

    def tgpLoadTxBtn(self, loadBtn, objectType, objectDesc, keywords, objectNickname=None):
        if objectNickname is None:
            objectNickname = objectType

        self.selLoad = []
        self.selLoad = mc.ls(sl=True, fl=True, type="transform")

        if (len(self.selLoad) != 1):
            mc.warning("Select only the {0}".format(objectDesc))
            return
        else:
            selName = self.selLoad[0]
            selName = self.tgpGetTx(selName, loadBtn, objectType, objectDesc, keywords, objectNickname)
            '''if CRU.checkObjectType(self.selLoad[0]) != objectType:
                mc.warning("{0} should be a {1}".format(objectDesc, objectNickname))
                return

            if not all(word.lower() in selName.lower() for word in keywords):
                mc.warning("That is the wrong {0}. Select the {1}".format(objectNickname, objectDesc))
                return
            mc.textFieldButtonGrp(loadBtn, e=True, tx=selName)'''
            return selName

    def tgpGetTx(self, selName, loadBtn, objectType, objectDesc, keywords, objectNickname=None, ):

        if CRU.checkObjectType(selName) != objectType:
            mc.warning("{0} should be a {1}".format(objectDesc, objectNickname))
            return

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
        self.selLoad = mc.ls(sl=True, fl=True, type=objectType)

        if (len(self.selLoad) != 1):
            mc.warning("Select only the {0}".format(objectDesc))
            return
        else:

            selName = self.selLoad[0]

            returner = self.tgpGetJnts(selName, loadBtn, objectType, objectDesc, keywords, objectNickname)
            # print("returner: {0}".format(returner))
            if returner is None:
                return None

        return self.jointArray

    def tgpGetJnts(self, selName, loadBtn, objectType, objectDesc, keywords, objectNickname=None, ):
        if objectNickname is None:
            objectNickname = objectType

        if CRU.checkObjectType(selName) != objectType:
            mc.warning("{0} should be a {1}".format(objectDesc, objectNickname))
            return

        if not all(word.lower() in selName.lower() for word in keywords):
            mc.warning("That is the wrong {0}. Select the {1}".format(objectNickname, objectDesc))
            return

        mc.textFieldButtonGrp(loadBtn, e=True, tx=selName)

        # get the children joints
        self.parent = selName
        self.child = mc.listRelatives(selName, ad=True, type="joint")
        # collect the joints in an array
        self.jointArray = [self.parent]
        # reverse the order of the children joints
        self.child.reverse()

        # add to the current list
        self.jointArray.extend(self.child)

        # removes if the last joint is End
        self.jointRoot = selName
        return self.jointArray

    def getJntArray(self, jointArray, fingerType, subType=None):
        if subType is None:
            fingerArray = [x for x in jointArray if (fingerType in x.lower())]
        else:
            fingerArray = [x for x in jointArray if (fingerType in x.lower()) and subType in x]
        return fingerArray

    def getSuperJntArray(self, jointArray, subType):
        jntThumbs = self.getJntArray(jointArray, "thumb", subType)
        jntPointer = self.getJntArray(jointArray, "pointer", subType)
        jntMiddle = self.getJntArray(jointArray, "middle", subType)
        jntRing = self.getJntArray(jointArray, "ring", subType)
        jntPink = self.getJntArray(jointArray, "pink", subType)

        jntTIMRP = [jntThumbs, jntPointer, jntMiddle, jntRing, jntPink]
        return jntTIMRP

    def makeOrientJoints(self, bndTIMRP):
        # creates the orient joints
        orntTIMRP = []
        for i in range(len(bndTIMRP)):
            # note: when duplicating, I am going to use the duplicated end joint rather than the original. It's easier but this may end up screwing things up
            dupVals = mc.duplicate(bndTIMRP[i][1], rc=True)
            orntJnts = []
            for j in range(len(dupVals)):
                # in case we duplicate a geometry
                if mc.objectType(dupVals[j]) == "joint":
                    orntJnts.append(dupVals[j])
                else:
                    mc.delete(dupVals[j])
            if "thumb" not in bndTIMRP[i][1]:
                # thumbs have a different numbering
                for k in range(len(orntJnts)):
                    renameVal = "{0}{1}".format(orntJnts[k][:-1].replace("JNT_BND_", "JNT_ORNT_"), k + 1)
                    mc.rename(orntJnts[k], renameVal)
                    orntJnts[k] = renameVal
            else:
                for k in range(len(orntJnts)):
                    if "Orbit" not in orntJnts[k]:
                        renameVal = "{0}{1}".format(orntJnts[k][:-1].replace("JNT_BND_", "JNT_ORNT_"), k)
                    else:
                        renameVal = "{0}".format(orntJnts[k][:-1].replace("JNT_BND_", "JNT_ORNT_"))
                    mc.rename(orntJnts[k], renameVal)
                    orntJnts[k] = renameVal
            bndTIMRPTemp = bndTIMRP[i][1:]

            for l in range(len(bndTIMRPTemp)):
                # parent the BND joint under the orient joint
                # this is where we might have an issue regarding using the duplicated JNT_ORNT as the last value
                if l == len(bndTIMRPTemp) - 1:
                    mc.delete(bndTIMRPTemp[l])
                else:
                    mc.parent(bndTIMRPTemp[l], orntJnts[l])
                    mc.parent(orntJnts[l + 1], bndTIMRPTemp[l])

            orntTIMRP.append(orntJnts)
        return orntTIMRP

    def makeFKJoints(self, jointArray):
        jntFKBase = jointArray[0].replace("BND", "CTRL")
        dupVals = mc.duplicate(jointArray[0], rc=True, n=jntFKBase)
        jointArrayFKHand = []
        for j in range(len(dupVals)):
            # in case we duplicate a geometry
            if mc.objectType(dupVals[j]) == "joint":
                jointArrayFKHand.append(dupVals[j])
            else:
                mc.delete(dupVals[j])
        fkTIMRP = self.getSuperJntArray(jointArrayFKHand, "BND")

        modBaseJntsLater = []

        for i in range(len(fkTIMRP)):
            for j in range(len(fkTIMRP[i])):
                replaceVal = "CTRL_FK_"
                dontSkipFK = True
                if (j == 0):
                    # a finger, the first value
                    addVal = ""
                    dontSkipFK = False
                elif (i == 0 and j < 2):
                    # a thumb, at the orient joint
                    addVal = ""
                elif (i == 0):
                    # a thumb, after skipping the base and orient
                    addVal = j - 1
                else:
                    # not a thumb, afte skipping the fingerBase
                    addVal = j

                renameVal = "{0}{1}".format(fkTIMRP[i][j][:-1].replace("JNT_BND_", replaceVal), addVal)
                mc.rename(fkTIMRP[i][j], renameVal)
                fkTIMRP[i][j] = renameVal
                if dontSkipFK:
                    toDelete = "toDelete"
                    orientVal = (1, 0, 0)
                    childJoint = mc.listRelatives(renameVal, type="joint")[0]
                    sizeMove = mc.getAttr("{0}.tx".format(childJoint)) / 2
                    if i == 0:
                        size = 1.5
                    else:
                        size = 1
                    mc.circle(nr=orientVal, r=size, n=toDelete)
                    fkShapeName = "{0}Shape".format(renameVal)

                    fkShape = mc.listRelatives(toDelete, s=True)[0]

                    mc.parent(fkShape, renameVal, s=True, r=True)
                    mc.delete(toDelete)
                    mc.rename(fkShape, fkShapeName)
                    mc.select("{0}.cv[:]".format(fkShapeName))

                    mc.move(sizeMove, 0, 0, r=True, os=True)
                else:
                    modBaseJntsLater.append(renameVal)
        return fkTIMRP, jntFKBase, modBaseJntsLater

    def makeCmpdControl(self, jntFKBase, modBaseJntsLater):
        jntFKHandJnts = mc.listRelatives(jntFKBase, type="joint", ad=True)
        jntFKHandJnts.append(jntFKBase)
        jntFKHandJnts.reverse()
        cmpdCtrlTIMRP = self.getSuperJntArray(jntFKHandJnts, "ORNT")

        for i in range(len(modBaseJntsLater)):
            renameVal = modBaseJntsLater[i].replace("CTRL_FK_", "JNT_cmpdCTRL_")
            mc.rename(modBaseJntsLater[i], renameVal)
            modBaseJntsLater[i] = renameVal

        for i in range(len(cmpdCtrlTIMRP)):
            for j in range(len(cmpdCtrlTIMRP[i])):
                replaceVal = "JNT_cmpdCTRL_"
                if i == 0:
                    # if the thumb, skip numbering the first two
                    if j == 0:
                        addVal = ""
                    else:
                        addVal = j
                else:
                    # if not the thumb
                    addVal = j + 1
                renameVal = "{0}{1}".format(cmpdCtrlTIMRP[i][j][:-1].replace("JNT_ORNT_", replaceVal), addVal)
                mc.rename(cmpdCtrlTIMRP[i][j], renameVal)
                cmpdCtrlTIMRP[i][j] = renameVal

        jntFKHandJnts = mc.listRelatives(jntFKBase, type="joint", ad=True)
        jntFKHandJnts.append(jntFKBase)
        jntFKHandJnts.reverse()

        cmpdCtrlTIMRP = self.getSuperJntArray(jntFKHandJnts, "cmpdCTRL")
        fkTIMRP = self.getSuperJntArray(jntFKHandJnts, "CTRL_FK")

        return jntFKHandJnts, cmpdCtrlTIMRP, fkTIMRP

    def connectHandJoints(self, fkTIMRP, bndTIMRP, cmpdCTRLTIMRP, orntTIMRP):
        rots = ["rx", "ry", "rz"]
        trans = ["tx", "ty", "tz"]

        for i in range(len(fkTIMRP)):
            for j in range(len(fkTIMRP[i])):
                for k in range(len(rots)):
                    mc.connectAttr("{0}.{1}".format(fkTIMRP[i][j], rots[k]),
                                   "{0}.{1}".format(bndTIMRP[i][j + 1], rots[k]))

        for i in range(len(cmpdCTRLTIMRP)):
            for j in range(len(cmpdCTRLTIMRP[i])):
                translateThis = True
                if j == 0:
                    # we want the fingerBase if we're at the first value
                    target = bndTIMRP[i][j]
                else:
                    # we want the other orients if we're past the first value
                    target = orntTIMRP[i][j - 1]

                if j < 2 or (i == 0 and j < 3):
                    # skip the first two joints or three if the thumb is there
                    translateThis = False

                for k in range(len(rots)):
                    mc.connectAttr("{0}.{1}".format(cmpdCTRLTIMRP[i][j], rots[k]), "{0}.{1}".format(target, rots[k]))
                    if translateThis:
                        mc.connectAttr("{0}.{1}".format(cmpdCTRLTIMRP[i][j], trans[k]),
                                       "{0}.{1}".format(target, trans[k]))

        return

    def makeFingersAttr(self, ctrl, attr, cmpdCTRLs, valPos, valNeg, drvnAttr, passVals, skipNeg=False):
        # the 4 finger joints
        tangentToUse = ["linear", "linear"]
        for j in range(len(valPos)):
            if passVals[j]:
                CRU.setDriverDrivenValues(ctrl, attr, cmpdCTRLs[j], drvnAttr, 0, 0, modifyInOut=tangentToUse)
                CRU.setDriverDrivenValues(ctrl, attr, cmpdCTRLs[j], drvnAttr, 10, valPos[j], modifyInOut=tangentToUse)
                if not skipNeg:
                    CRU.setDriverDrivenValues(ctrl, attr, cmpdCTRLs[j], drvnAttr, -10, valNeg[j],
                                              modifyInOut=tangentToUse)

        return

    def makeFingersCompound(self, ctrlTIRMP, fingerAttr, cmpdCtrlTIMRP, isHand=False):
        # sets up the curls

        for i in range(len(cmpdCtrlTIMRP)):

            # the 1 represents the curl
            # the 2 represents the scrunch
            # the 3 represents the lean
            # the 4 represents the relax
            # the 5 represents the spread
            passVals1 = [True, True, True, True]  # skip the false values for curl
            passVals2 = [False, True, True, True]  # skip the false values for scrunch
            passVals3 = [False, True, True, True]  # skip the false values for lean
            passVals4 = [True, True, True, True]  # skip the false values for relax

            if i == 0:
                # thumb curls
                valPos1 = [10, 40, 50, 90]
                valNeg1 = [-5, -15, -30, -25]

                # thumb scrunch
                valPos2 = [0, -25, 55, 90]
                valNeg2 = [0, -12, -20, -20]

                # thumb lean
                valPos3 = [0, 25, 25, 25]
                valNeg3 = [0, -25, -25, -25]

                # thumb relax
                #  no relax for thumb

                # thumb spread
                passVals5 = [True, True, True, False]
                drvnAttr5 = "rz"

                valPos5 = [-15, -5, -15, 0]
                valNeg5 = [45, 0, 0, 0]

            else:
                # finger curls
                valPos1 = [10, 95, 95, 115]
                valNeg1 = [-5, -35, -35, -35]

                # finger scrunch
                valPos2 = [0, -47, 120, 62]
                valNeg2 = [0, -12, -15, -18]

                # finger lean
                valPos3 = [0, 25, 25, 25]
                valNeg3 = [0, -25, -25, -25]

                # finger relax

                posI = (i - 1) * 2.5
                negI = (i - 1) * 2.5

                valPos4 = [5 + posI, 20 + posI, 15 + posI, 10 + posI]
                valNeg4 = [7.5 - negI, 27.5 - negI, 22.5 - negI, 17.5 - negI]

                # finger spread

                passVals = [True, True, False, False]  # skip the false values
                drvnAttr5 = "ry"

                if i == 1:
                    # index
                    valPos5 = [7.5, 7.5]
                    valNeg5 = [-5, 0]
                elif i == 2:
                    # middle
                    valPos5 = [1.5, 0]
                    valNeg5 = [-1.5, 0]
                elif i == 3:
                    # ring
                    valPos5 = [-5, -4.5]
                    valNeg5 = [1.5, 0]
                elif i == 4:
                    # pinky
                    valPos5 = [-7.5, -30]
                    valNeg5 = [5, 0]

            drvnAttr1 = "rz"
            drvnAttr2 = "rz"
            drvnAttr3 = "ry"
            drvnAttr4 = "rz"
            if isHand:
                ctrlPass = ctrlTIRMP
            else:
                ctrlPass = ctrlTIRMP[i]

            self.makeFingersAttr(ctrlPass, fingerAttr[0], cmpdCtrlTIMRP[i], valPos1, valNeg1, drvnAttr1, passVals1)
            self.makeFingersAttr(ctrlPass, fingerAttr[1], cmpdCtrlTIMRP[i], valPos2, valNeg2, drvnAttr2, passVals2)
            self.makeFingersAttr(ctrlPass, fingerAttr[2], cmpdCtrlTIMRP[i], valPos3, valNeg3, drvnAttr3, passVals3)
            if i != 0:
                # skip the thumb
                self.makeFingersAttr(ctrlPass, fingerAttr[3], cmpdCtrlTIMRP[i], valPos4, valNeg4, drvnAttr4, passVals4)
            self.makeFingersAttr(ctrlPass, fingerAttr[4], cmpdCtrlTIMRP[i], valPos5, valNeg5, drvnAttr5, passVals5)

        return

    def makeFistCompound(self, ctrlHand, handAttr, cmpdCtrlTIMRP):
        # sets up the curls

        for i in range(len(cmpdCtrlTIMRP)):

            # the 1 represents the curl
            passVals1 = [True, True, True, True]  # skip the false values for curl

            valNeg = [0, 0, 0, 0, ]
            if i == 0:
                # thumb curls
                valPosZ = [10, 45, 20, 80]

                valPosX = [0, -15, 0, 0]
                drvnAttrX = "rx"

                valPosY = [0, 10, 0, 0]
                drvnAttrY = "ry"

            else:
                # finger curls
                valPosZ = [10, 95, 95, 115]

            drvnAttr1 = "rz"

            self.makeFingersAttr(ctrlHand, handAttr[5], cmpdCtrlTIMRP[i], valPosZ, valNeg, drvnAttr1, passVals1,
                                 skipNeg=True)
            if i == 0:
                # only for thumb
                self.makeFingersAttr(ctrlHand, handAttr[5], cmpdCtrlTIMRP[i], valPosX, valNeg, drvnAttrX, passVals1,
                                     skipNeg=True)
                self.makeFingersAttr(ctrlHand, handAttr[5], cmpdCtrlTIMRP[i], valPosY, valNeg, drvnAttrY, passVals1,
                                     skipNeg=True)
        return

    def addFingerStretch(self, ctrl, cmpdCtrl, skipJoints):
        lengthAttr = "length"

        mc.addAttr(ctrl, longName=lengthAttr, at="float", k=True, min=0, dv=1)
        for j in range(len(cmpdCtrl)):
            if j <= skipJoints:
                # skip the first few joints
                pass
            else:

                lenX = mc.getAttr("{0}.tx".format(cmpdCtrl[j]))

                CRU.setDriverDrivenValues(ctrl, lengthAttr, cmpdCtrl[j], "tx", 0, 0, modifyInOut=["stepnext", "spline"])
                CRU.setDriverDrivenValues(ctrl, lengthAttr, cmpdCtrl[j], "tx", 1, lenX,
                                          modifyBoth="spline")
                # mc.selectKey(cl=True)
                mc.selectKey(cmpdCtrl[j], k=1, attribute="tx")
                mc.setInfinity(poi='cycleRelative')

        return

    def makeFingerGeoStretch(self, orntJnts, bndJnts, skipJoints, leftRight):
        # makes the fingers stretch
        for x in range(len(orntJnts)):
            if x <= skipJoints:
                # under normal circumstances, skip the first orient joint, or first two if thumb
                pass
            else:
                # creates the multiply divide node
                baseName = orntJnts[x].replace("JNT_ORNT_", "")
                normDivGeo = "{0}_normalize_DIV".format(baseName)
                mc.shadingNode("multiplyDivide", n=normDivGeo, au=True)
                mc.setAttr("{0}.operation".format(normDivGeo), 2)

                # get the base length:
                lenX = mc.getAttr("{0}.tx".format(orntJnts[x]))

                mc.setAttr("{0}.input2X".format(normDivGeo), lenX)
                mc.connectAttr("{0}.tx".format(orntJnts[x]), "{0}.input1X".format(normDivGeo))
                geoName = bndJnts[x].replace("JNT_BND_", "GEO_")

                # get the geoName
                mc.connectAttr("{0}.outputX".format(normDivGeo), "{0}.scaleX".format(geoName))
        return

    def makeIKFingers(self, cmpdCtrlJnts, bndJnts, orntJnts, checkThumb, leftRight):
        # duplicate the finger
        # fingerBase
        fb = 0
        if checkThumb:
            fBP = + 2
        else:
            fBP = + 1
        print("cmpdCtrlJnts[{1}]: {0}".format(cmpdCtrlJnts[fBP], fBP))
        baseVal = cmpdCtrlJnts[fBP].split("JNT_cmpdCTRL_")[1][:-1]
        ikDup = mc.duplicate(cmpdCtrlJnts[fb + 1], rc=True)

        # parent the last cmpdCTRL under the first, then delete the rest
        ikStraightStartTemp = ikDup[0]
        ikStraightEndTemp = ikDup[-1]
        mc.parent(ikStraightEndTemp, ikStraightStartTemp)
        mc.delete(ikDup[1])
        ikStrStart = "JNT_{0}_straightStart".format(baseVal)
        ikStrEnd = "JNT_{0}_straightEnd".format(baseVal)
        mc.rename(ikStraightStartTemp, ikStrStart)
        mc.rename(ikStraightEndTemp, ikStrEnd)

        ikStrFingers = [ikStrStart, ikStrEnd]

        # set up the ik stretch
        hdlFinger = "HDL_{0}_straight".format(baseVal)
        effFinger = "EFF_{0}_straight".format(baseVal)
        ikSolver = "ikSCsolver"
        ikFinger = mc.ikHandle(sj=ikStrStart, ee=ikStrEnd, sol=ikSolver)
        mc.rename(ikFinger[0], hdlFinger)
        mc.rename(ikFinger[1], effFinger)

        ikFinger[0] = hdlFinger
        ikFinger[1] = effFinger

        # gruop them appropriately
        grpHDL = "GRP_{0}hand_straightHDL".format(leftRight)
        if not mc.objExists(grpHDL):
            mc.group(n=grpHDL, w=True, em=True)
        # put the finger Handle into the group
        mc.parent(hdlFinger, grpHDL)

        # we want to put this on the first joint for most fingers, but the
        mc.parent(cmpdCtrlJnts[fb + 1], ikStrStart)

        # create spacing joint for other hand
        ikFingerStr = "JNT_{0}_straight".format(baseVal)
        mc.duplicate(ikStrStart, n=ikFingerStr, po=True)

        mc.parent(ikFingerStr, bndJnts[fb])

        mc.parent(orntJnts[fb], ikFingerStr)

        # connect the fingers
        rots = ["rx", "ry", "rz"]
        for x in range(len(rots)):
            mc.connectAttr("{0}.{1}".format(ikStrStart, rots[x]), "{0}.{1}".format(ikFingerStr, rots[x]))

        return ikFinger, grpHDL, ikStrFingers

    def makePalmRaise(self, ctrlHand, locArray, leftRight):
        palmAttr = "palmRaise"

        if leftRight == self.valLeft:
            m = 1
        else:
            m = -1

        mc.addAttr(ctrlHand, longName=palmAttr, at="float", k=True, min=-90,
                   max=90, dv=0)
        CRU.setDriverDrivenValues(ctrlHand, palmAttr, locArray[-1], "rz", 0, 0, modifyBoth="spline")
        CRU.setDriverDrivenValues(ctrlHand, palmAttr, locArray[-1], "rz", 90, -90 * m, modifyBoth="spline")
        CRU.setDriverDrivenValues(ctrlHand, palmAttr, locArray[-1], "rz", -90, 90 * m, modifyBoth="spline")
        return

    def makeSideRoll(self, ctrlHand, locArray):
        palmAttr = "sideRoll"

        mc.addAttr(ctrlHand, longName=palmAttr, at="float", k=True, min=-90,
                   max=90, dv=0)
        CRU.setDriverDrivenValues(ctrlHand, palmAttr, locArray[0], "rx", 0, 0, modifyBoth="spline")
        CRU.setDriverDrivenValues(ctrlHand, palmAttr, locArray[1], "rx", 0, 0, modifyBoth="spline")

        CRU.setDriverDrivenValues(ctrlHand, palmAttr, locArray[1], "rx", 90, -90, modifyBoth="spline")

        CRU.setDriverDrivenValues(ctrlHand, palmAttr, locArray[0], "rx", -90, 90, modifyBoth="spline")
        return

    def cleanPalms(self, locArray, grpHDL, ctrlHand, ctrlTIRMP, jntConstHand, leftRight):

        # hide these values
        mc.setAttr("{0}.visibility".format(locArray[0]), False)
        mc.setAttr("{0}.visibility".format(grpHDL), False)

        # create group for controls
        grpCtrlHand = "GRP_CTRL_{0}hand".format(leftRight)
        mc.group(n=grpCtrlHand, w=True, em=True)
        addHand = ctrlTIRMP[:]
        addHand.append(ctrlHand)
        mc.parent(addHand, grpCtrlHand)

        # have the jntConstHand parent Constrain the bndBaseHand

        mc.parentConstraint(jntConstHand, grpCtrlHand, mo=True)

        return grpCtrlHand

    def makeSpreadFix(self, cmpdCtrlTIMRP, ctrlTIRMP, ctrlHand):
        fingerValsNeg = [-35, -8, -4, 1, 7]
        fingerValsPos = [15, 25, 5, -10, -30]
        for i in range(len(cmpdCtrlTIMRP)):
            print("cmpdCtrlTIMRP[{1}] {0}".format(cmpdCtrlTIMRP[i], i))
            if i == 0:
                CRU.setDriverDrivenValues(ctrlTIRMP[i], "spread", cmpdCtrlTIMRP[i][1], "rz", 0, 0, modifyBoth="linear")
                CRU.setDriverDrivenValues(ctrlTIRMP[i], "spread", cmpdCtrlTIMRP[i][1], "rz", -10, 35,
                                          modifyBoth="linear")
                CRU.setDriverDrivenValues(ctrlTIRMP[i], "spread", cmpdCtrlTIMRP[i][1], "rz", 10, -20,
                                          modifyBoth="linear")

                CRU.setDriverDrivenValues(ctrlHand, "spread", cmpdCtrlTIMRP[i][1], "rz", 0, 0, modifyBoth="linear")
                CRU.setDriverDrivenValues(ctrlHand, "spread", cmpdCtrlTIMRP[i][1], "rz", -10, 35, modifyBoth="linear")
                CRU.setDriverDrivenValues(ctrlHand, "spread", cmpdCtrlTIMRP[i][1], "rz", 10, -20, modifyBoth="linear")

            # sets the JNT_cmpdCTRL_finger1
            CRU.setDriverDrivenValues(ctrlTIRMP[i], "spread", cmpdCtrlTIMRP[i][1], "ry", 0, 0)
            CRU.setDriverDrivenValues(ctrlTIRMP[i], "spread", cmpdCtrlTIMRP[i][1], "ry", -10, fingerValsNeg[i],
                                      modifyBoth="linear")
            CRU.setDriverDrivenValues(ctrlTIRMP[i], "spread", cmpdCtrlTIMRP[i][1], "ry", 10, fingerValsPos[i],
                                      modifyBoth="linear")

            CRU.setDriverDrivenValues(ctrlHand, "spread", cmpdCtrlTIMRP[i][1], "ry", 0, 0)
            CRU.setDriverDrivenValues(ctrlHand, "spread", cmpdCtrlTIMRP[i][1], "ry", -10, fingerValsNeg[i],
                                      modifyBoth="linear")
            CRU.setDriverDrivenValues(ctrlHand, "spread", cmpdCtrlTIMRP[i][1], "ry", 10, fingerValsPos[i],
                                      modifyBoth="linear")
        return

    def addHandToArm(self, jntBindEnd, jntFKBase, bndBaseHand, jntArmHandBnd, jntConstHand, locArray, grpCtrlHand,
                     grpHDL, ctrlRootTrans, geoPalm, leftRight):
        grpHand = "GRP_{0}hand".format(leftRight)
        mc.group(n=grpHand, w=True, em=True)

        mc.parent(jntFKBase, bndBaseHand, locArray[0], grpCtrlHand, grpHDL, grpHand)
        mc.parent(grpHand, ctrlRootTrans)

        # create the do not touch
        grpDNT = "GRP_DO_NOT_TOUCH_{0}hand".format(leftRight)
        mc.group(n=grpDNT, w=True, em=True)

        mc.parent(grpDNT, grpHand)
        mc.parent(bndBaseHand, locArray[0], grpHDL, grpDNT)
        if geoPalm is not None:
            mc.parent(geoPalm, grpDNT)

        # create the const hand and parent the locators under it
        grpHandConst = "GRP_const_{0}hand".format(leftRight)
        mc.group(n=grpHandConst, w=True, em=True)
        mc.parent(grpHandConst, grpDNT)
        mc.parent(locArray[0], grpHandConst)

        # pivot the Const hand to the wrist
        toDelete = mc.spaceLocator(p=(0, 0, 0), name="toDelete")[0]
        CRU.constrainMove(jntBindEnd, toDelete, point=True)
        pivotTranslate = mc.xform(toDelete, q=True, ws=True, rotatePivot=True)
        mc.delete(toDelete)
        mc.xform(grpHandConst, ws=True, pivots=pivotTranslate)

        mc.parentConstraint(jntArmHandBnd, grpHandConst, mo=True)

        # fixing some issues
        mc.parent(grpHDL, grpHandConst)

        # we are tying the bind end joint to the new hand and fingers to allow the arm to move appropriately
        toDelete = mc.listRelatives(jntBindEnd, type="parentConstraint")[0]
        mc.delete(toDelete)

        mc.parentConstraint(jntConstHand, jntBindEnd, mo=True)

        return

    def setVisibilityModifiers(self, ctrlSettings, grpCtrlHand, jntFKBase):
        # sets the visibility of the finger FK controls
        handFKVisAttr = "hand_FK_visibility"

        mc.addAttr(ctrlSettings, longName=handFKVisAttr, at="bool", k=True)
        mc.setAttr("{0}.{1}".format(ctrlSettings, handFKVisAttr), True)
        mc.connectAttr("{0}.{1}".format(ctrlSettings, handFKVisAttr), "{0}.visibility".format(jntFKBase))

        # sets the visibility of the finger controls
        handCtrlVisAttr = "hand_CTRL_visibility"

        mc.addAttr(ctrlSettings, longName=handCtrlVisAttr, at="bool", k=True)
        mc.setAttr("{0}.{1}".format(ctrlSettings, handCtrlVisAttr), True)
        mc.connectAttr("{0}.{1}".format(ctrlSettings, handCtrlVisAttr), "{0}.visibility".format(grpCtrlHand))

        return

    def cleanupFingersMethod(self, jntFKBase, grpCtrlHand, ikStrFingerTIMRP, cmpdCtrlTIMRP, fkTIMRP, ctrlHand,
                             ctrlTIRMP, bndBaseHand):
        # lock and hide various traits
        CRU.lockHideCtrls(jntFKBase, translate=True, rotate=True, scale=True, visibility=True)
        CRU.lockHideCtrls(grpCtrlHand, translate=True, rotate=True, scale=True, visibility=True)

        # we have to hide certain traits, not lock them
        for i in range(len(cmpdCtrlTIMRP)):
            for j in range(len(cmpdCtrlTIMRP[i])):
                CRU.lockHideCtrls(cmpdCtrlTIMRP[i][j], translate=True, scale=True, visibility=True, rotate=True, )
                CRU.lockHideCtrls(cmpdCtrlTIMRP[i][j], theVals=["radi"], channelBox=False)

            for j in range(len(fkTIMRP[i])):
                CRU.lockHideCtrls(fkTIMRP[i][j], translate=True, scale=True, visibility=True)
                CRU.lockHideCtrls(fkTIMRP[i][j], theVals=["radi"], channelBox=False)

            # we don't want to lock the rotate values for the start
            mc.setAttr("{0}.visibility".format(ikStrFingerTIMRP[i][0]), False)
            CRU.lockHideCtrls(ikStrFingerTIMRP[i][0], translate=True, scale=True, visibility=True)
            CRU.lockHideCtrls(ikStrFingerTIMRP[i][0], rotate=True, toLock=False)

            # we don't want to lock the translate values for the end
            CRU.lockHideCtrls(ikStrFingerTIMRP[i][1], rotate=True, scale=True, visibility=True)
            CRU.lockHideCtrls(ikStrFingerTIMRP[i][1], translate=True, toLock=False)

            # hide the controls stuff
            CRU.lockHideCtrls(ctrlTIRMP[i], translate=True, scale=True, visibility=True, rotate=True, )

        CRU.lockHideCtrls(ctrlHand, translate=True, scale=True, visibility=True, rotate=True, )

        CRU.layerEdit(bndBaseHand, bndLayer=True)

        return

    def makeFingersComplete(self, jointArrayBaseHand, locArray, jntBindEnd, jntArmHandBnd, ctrlRootTrans, ctrlSettings,
                            checkGeo, leftRight, colourTU, *args):

        for i in range(len(locArray)):
            if isinstance(locArray[i], int):
                mc.setAttr('{0}.overrideEnabled'.format(locArray[i]), 1)

                mc.setAttr("{0}.overrideColor".format(locArray[i]), colourTU)
            else:
                mc.setAttr("{0}.overrideColorRGB".format(locArray[i]), colourTU[0], colourTU[1], colourTU[2])
                mc.setAttr("{0}.overrideRGBColors".format(locArray[i]), 1)

        newLayerNameFK = "{0}hand_FK_LYR".format(leftRight)
        bndBaseHand = jointArrayBaseHand[0]

        geoJntArray = jointArrayBaseHand[:]
        print ("geoJntArray: {0}".format(geoJntArray))

        # TIMRP = Thumb, Index, Middle, Ring, Pinkie
        bndTIMRP = self.getSuperJntArray(jointArrayBaseHand,
                                         "BND")  # [jntThumbs, jntPointer, jntMiddle, jntRing, jntPink]

        # here we would skin the hand if we had skinning turned on
        if checkGeo:
            CRU.tgpSetGeo(geoJntArray, setLayer=True, printOut=False)
            geoPalm = "{0}Skin".format(bndBaseHand.replace("JNT_BND_", "GEO_"))
            skinPalm = "{0}palmSkin".format(leftRight)
            mc.skinCluster(geoJntArray[0], geoPalm, n=skinPalm, dr=6)
            CRU.layerEdit(geoPalm, geoLayer=True)
        # probably the geo too

        # Orient setup
        orntTIMRP = self.makeOrientJoints(bndTIMRP)
        jointArrayReplace = []
        # we have renamed/deleted several joints, so we are purging it and resetting it
        for i in range(len(jointArrayBaseHand)):
            if mc.objExists(jointArrayBaseHand[i]):
                jointArrayReplace.append(jointArrayBaseHand[i])
        jointArray = jointArrayReplace
        bndTIMRP = self.getSuperJntArray(jointArray, "BND")  # we did some adjustments so we may need to reset this one

        # FK Setup
        fkTIMRP, jntFKBase, modBaseJntsLater = self.makeFKJoints(jointArray, )
        for i in range(len(fkTIMRP)):
            CRU.layerEdit(fkTIMRP[i], newLayerName=newLayerNameFK, colourTU=colourTU)

        jntFKHandJnts, cmpdCtrlTIMRP, fkTIMRP = self.makeCmpdControl(jntFKBase, modBaseJntsLater)

        jntBaseHandJnts = mc.listRelatives(bndBaseHand, ad=True, type="joint")
        jntBaseHandJnts.append(bndBaseHand)
        jntBaseHandJnts.reverse()

        # Connect Joints
        self.connectHandJoints(fkTIMRP, bndTIMRP, cmpdCtrlTIMRP, orntTIMRP)

        #  Compound finger controls
        ctrlTIRMP = []
        handsLayer = "hands_cmpdCTRL_LYR"
        for i in range(len(bndTIMRP)):
            orientVal = (1, 0, 0)
            size = 0.5
            ctrlName = bndTIMRP[i][0][:-4].replace("JNT_BND_", "CTRL_")
            mc.circle(nr=orientVal, r=size, n=ctrlName)
            CRU.constrainMove(bndTIMRP[i][0], ctrlName, parent=True)
            mc.move(0, 2, 0, ctrlName, r=True)
            ctrlTIRMP.append(ctrlName)
            mc.makeIdentity(ctrlName, apply=True)

        CRU.layerEdit(ctrlTIRMP, newLayerName=handsLayer, colourTU=CRU.clrHandCtrl)

        valsMinMaxDef = [-10, 10, 0]
        fingerAttr = ["curl", "scrunch", "lean", "relax", "spread"]
        for i in range(len(ctrlTIRMP)):
            # add the attributes
            for j in range(len(fingerAttr)):
                minVal = valsMinMaxDef[0]
                maxVal = valsMinMaxDef[1]
                defVal = valsMinMaxDef[2]

                mc.addAttr(ctrlTIRMP[i], longName=fingerAttr[j], at="float", k=True, min=minVal,
                           max=maxVal, dv=defVal)

        self.makeFingersCompound(ctrlTIRMP, fingerAttr, cmpdCtrlTIMRP)

        # create the hand
        ctrlHand = "CTRL_{0}hand".format(leftRight)
        orientVal = (1, 0, 0)
        size = 0.5
        mc.circle(nr=orientVal, r=size, n=ctrlHand, sections=10)
        CRU.constrainMove([ctrlTIRMP[2], ctrlTIRMP[3]], ctrlHand, parent=True)
        mc.select("{0}.cv[:]".format(ctrlHand))
        mc.scale(1, 1.45, 1, r=True, os=True)
        mc.select("{0}.cv[7:9] ".format(ctrlHand))
        mc.select("{0}.cv[0] ".format(ctrlHand), add=True)
        mc.move(0, -0.35, -2.7, r=True, os=True)

        mc.select("{0}.cv[2:5] ".format(ctrlHand))
        mc.move(0, -0, 2.65, r=True, os=True)
        mc.select(cl=True)
        mc.makeIdentity(ctrlHand, apply=True)
        CRU.layerEdit(ctrlHand, newLayerName=handsLayer, colourTU=CRU.clrHandCtrl)

        handAttr = ["curl", "scrunch", "lean", "relax", "spread", "fist"]

        valsMinMaxDef = [-10, 10, 0]
        for i in range(len(handAttr)):
            # add the attributes to the hand

            if "fist" in handAttr[i]:
                minVal = 0
            else:
                minVal = valsMinMaxDef[0]
            maxVal = valsMinMaxDef[1]

            defVal = valsMinMaxDef[2]

            mc.addAttr(ctrlHand, longName=handAttr[i], at="float", k=True, min=minVal,
                       max=maxVal, dv=defVal)
        self.makeFingersCompound(ctrlHand, handAttr, cmpdCtrlTIMRP, isHand=True)

        self.makeFistCompound(ctrlHand, handAttr, cmpdCtrlTIMRP)

        # Compound finger controls
        # Palm Control

        rotsTrans = ["rx", "ry", "rz", "tx", "ty", "tz"]

        for i in range(len(rotsTrans)):
            mc.connectAttr("{0}.{1}".format(jntFKBase, rotsTrans[i]),
                           "{0}.{1}".format(bndBaseHand, rotsTrans[i]))
        jntConstHand = "JNT_baseConst_{0}hand".format(leftRight)
        mc.duplicate(bndBaseHand, n=jntConstHand, po=True)
        # parent the const under the LOC_palmMiddle
        mc.parent(jntConstHand, locArray[-1])

        mc.parentConstraint(jntConstHand, jntFKBase)

        ikFingerTIMRP = []
        ikStrFingerTIMRP = []
        # IK Fingers
        for i in range(len(cmpdCtrlTIMRP)):

            if i == 0:
                # we will come back to this
                checkThumb = True
            else:
                checkThumb = False
            # finger base helps us determine whcih values we use in case of thumb in particular
            ikFinger, grpHDL, ikStrFingers = self.makeIKFingers(cmpdCtrlTIMRP[i], bndTIMRP[i], orntTIMRP[i], checkThumb,
                                                                leftRight)
            ikFingerTIMRP.append(ikFinger)
            ikStrFingerTIMRP.append(ikStrFingers)

        # Custom Attributes
        # Palm Raise
        self.makePalmRaise(ctrlHand, locArray, leftRight)

        # side roll
        self.makeSideRoll(ctrlHand, locArray)

        # Cleaning Up
        grpCtrlHand = self.cleanPalms(locArray, grpHDL, ctrlHand, ctrlTIRMP, jntConstHand, leftRight)
        # Spread  Fix
        self.makeSpreadFix(cmpdCtrlTIMRP, ctrlTIRMP, ctrlHand)

        # Hand global transform and cleanup
        # finger stretch
        for i in range(len(ctrlTIRMP)):
            if i == 0:
                skipJoints = 2
            else:
                skipJoints = 1
            self.addFingerStretch(ctrlTIRMP[i], cmpdCtrlTIMRP[i], skipJoints)

        if checkGeo:
            for i in range(len(orntTIMRP)):
                if i == 0:
                    skipJoints = 1
                else:
                    skipJoints = 0
                self.makeFingerGeoStretch(orntTIMRP[i], bndTIMRP[i], skipJoints, leftRight)

        # Attach to Arm
        if not checkGeo:
            geoPalm = None
        self.addHandToArm(jntBindEnd, jntFKBase, bndBaseHand, jntArmHandBnd, jntConstHand, locArray, grpCtrlHand,
                          grpHDL, ctrlRootTrans, geoPalm, leftRight)

        # Visibility Attributes
        self.setVisibilityModifiers(ctrlSettings, grpCtrlHand, jntFKBase)

        self.cleanupFingersMethod(jntFKBase, grpCtrlHand, ikStrFingerTIMRP, cmpdCtrlTIMRP, fkTIMRP, ctrlHand, ctrlTIRMP,
                                  bndBaseHand)

        if checkGeo:
            # turn off the inherits transform
            mc.setAttr("{0}.inheritsTransform".format(geoPalm), 0)

    def tgpCreateMirror(self, locArray, toReplace, toReplaceMirror):

        # when you make a duplicate, the order of the duplicated children will get reversed. This reverses the reverse.
        locMirrorWork = mc.duplicate(locArray, rc=True)

        print("locMirrorWork: {0}".format(locMirrorWork))

        locMirror = []

        for i in range(len(locMirrorWork)):
            # switch the l/r,
            toRename = locMirrorWork[i].replace(toReplace, toReplaceMirror)[:-1]
            mc.rename(locMirrorWork[i], toRename)
            locMirror.append(toRename)

        print("locArray: {0}".format(locArray))
        print("locMirror: {0}".format(locMirror))

        locMirrorTop = locMirror[0]
        # takes the initial offset value, duplicates it, flips the values around, then freezes the transformation
        # translates everything into place
        mirrorTrans = mc.xform(locMirrorTop, q=True, ws=True, rotatePivot=True)
        # the rotatations should be zeroed out
        # mirrorRot = mc.xform(locMirrorTop, q=True, ws=True, rotation=True)
        mirrorTransX = mirrorTrans[0] * -1
        mirrorTransY = mirrorTrans[1]
        mirrorTransZ = mirrorTrans[2]

        '''mirrorRotX = mirrorRot[0] * 1
        mirrorRotY = mirrorRot[1] * -1
        mirrorRotZ = mirrorRot[2] * -1'''

        mirrorXScal = mc.getAttr("{0}.sx".format(locMirrorTop)) * -1

        # mirrors the values

        mc.xform(locMirrorTop, translation=(mirrorTransX, mirrorTransY, mirrorTransZ))
        mc.xform(locMirrorTop, scale=(mirrorXScal, 1, 1))
        # mc.xform(locMirrorTop, rotation=(mirrorRotX, mirrorRotY, mirrorRotZ))
        checkList = mc.listRelatives(locMirrorTop)

        # fix the scale and rotates
        for i in range(len(locMirror)):
            if i == 0:
                pass
            else:
                mc.parent(locMirror[i], w=True)

        for i in range(len(locMirror)):
            mc.makeIdentity(locMirror[i], apply=True, scale=True, rotate=True)

        for i in range(len(locMirror)):
            if i == 0:
                pass
            else:
                mc.parent(locMirror[i], locMirror[i - 1])
        return locMirror

    def tgpMakeBC(self, *args):

        checkSelLeft = mc.radioButtonGrp("selHandType_rbg", q=True, select=True)
        mirrorSel = mc.radioButtonGrp("selHandMirrorType_rbg", q=True, select=True)

        jntFingerNamesCheck = mc.textFieldButtonGrp("jntFingersLoad_tfbg", q=True, text=True)
        jntFingerNames = self.tgpGetJnts(jntFingerNamesCheck, "jntFingersLoad_tfbg", "joint", "Hand Base Joint",
                                         ["jnt", "handBase"], "joint")

        checkGeo = mc.checkBox("selGeo_cb", q=True, v=True)

        locPalm = mc.textFieldButtonGrp("locPalmLoad_tf", q=True, text=True)
        locArray = self.tgpLoadLocMethod(locPalm, "locPalmLoad_tf", "locator", "Inner Palm Locator",
                                         ["loc", "palmInner"], "locator")

        jntBindEndCheck = mc.textFieldButtonGrp("jntBindEndLoad_tf", q=True, text=True)
        jntBindEnd = self.tgpGetTx(jntBindEndCheck, "jntBindEndLoad_tf", "joint", "Hand Base Joint",
                                   ["jnt", "arm", "bindEnd"],
                                   "joint")

        ctrlRootTransCheck = mc.textFieldButtonGrp("rootTrans_tfbg", q=True, text=True)
        ctrlRootTrans = self.tgpGetTx(ctrlRootTransCheck, "rootTrans_tfbg", "nurbsCurve", "Root Control",
                                      ["CTRL", "rootTransform"], "control")

        jntArmHandBndCheck = mc.textFieldButtonGrp("jntHandLoad_tfbg", q=True, text=True)
        jntArmHandBnd = self.tgpGetTx(jntArmHandBndCheck, "jntHandLoad_tfbg", "joint", "Hand Joint",
                                      ["jnt", "bnd", "hand", ], "joint")

        ctrlSettingsCheck = mc.textFieldButtonGrp("ctrlSettingsLoad_tfbg", q=True, text=True)
        ctrlSettings = self.tgpGetTx(ctrlSettingsCheck, "ctrlSettingsLoad_tfbg", "nurbsCurve", "Arm Control Setting",
                                     ["ctrl", "arm", "settings", ], "control")

        '''if len(self.locArray) == 0:
            locArray = self.tgpLoadLocMethod(locPalm)
        else:
            locArray = self.locArray'''

        try:
            fingerRoot = self.jointArray[0]

        except:
            mc.warning("No control selected!")
            return

        jointArrayBaseHand = self.jointArray[:]

        self.valLeft = "l_"
        self.valRight = "r_"

        if mirrorSel == 1:
            mirrorRig = False
        else:
            mirrorRig = True

        if checkSelLeft == 1:
            isLeft = True
            leftRight = "l_"
            leftRightMirror = "r_"
            colourTU = CRU.clrLeftFK
            colourTUMirror = CRU.clrRightFK
            leftRight = self.valLeft
            leftRightMirror = self.valRight
        else:
            isLeft = False
            leftRight = "r_"
            leftRightMirror = "l_"
            colourTU = CRU.clrRightFK
            colourTUMirror = CRU.clrLeftFK
            leftRight = self.valRight
            leftRightMirror = self.valLeft

        toReplace = "_" + leftRight
        toReplaceMirror = "_" + leftRightMirror

        # make sure the selections are not empty
        checkList = [jntFingerNames]
        # note: the isCopy is not applicable due to the differences between the leg and arm joint setup.
        # However, editing them out is too much hassle,  it's easier just to leave them both false
        if ((checkList[0] == "")):
            mc.warning("You are missing a selection!")
            return
        else:

            CRU.createLocatorToDelete()
            if not (CRU.checkLeftRight(isLeft, fingerRoot)):
                # if the values are not lined up properly, break out
                mc.warning("You are selecting the incorrect side for the fingers control")
                return

            if not (CRU.checkLeftRight(isLeft, locPalm)):
                # if the values are not lined up properly, break out
                mc.warning("You are selecting the incorrect side for the locators")
                return

            if not (CRU.checkLeftRight(isLeft, jntBindEnd)):
                # if the values are not lined up properly, break out
                mc.warning("You are selecting the incorrect side for the bind end")
                return

            if mirrorRig:
                # we want to get the finger control before we add anything to it. When doing this programmatically, it's easier
                jntBindEndMirror = jntBindEnd.replace(toReplace, toReplaceMirror)
                jntArmHandBndMirror = jntArmHandBnd.replace(toReplace, toReplaceMirror)
                ctrlSettingsMirror = ctrlSettings.replace(toReplace, toReplaceMirror)

                jointArrayBaseHandMirror = mc.mirrorJoint(jointArrayBaseHand[0], mirrorYZ=True, mirrorBehavior=True,
                                                          searchReplace=[toReplace, toReplaceMirror])
                print("jointArrayBaseHandMirror: {0}".format(jointArrayBaseHandMirror))

                # make sure the children are not locked
                locArrayMirror = self.tgpCreateMirror(locArray, toReplace,
                                                      toReplaceMirror)

            self.makeFingersComplete(jointArrayBaseHand, locArray, jntBindEnd, jntArmHandBnd, ctrlRootTrans,
                                     ctrlSettings,
                                     checkGeo, leftRight, colourTU)
            if mirrorRig:
                print("Mirroring")

                isLeftMirror = not isLeft

                # ctrlPalmMirror = ctrlPalm.replace(leftRightReplace, leftRightReplaceMirror)

                self.makeFingersComplete(jointArrayBaseHandMirror, locArrayMirror, jntBindEndMirror,
                                         jntArmHandBndMirror, ctrlRootTrans, ctrlSettingsMirror,
                                         checkGeo, leftRightMirror, colourTUMirror)
