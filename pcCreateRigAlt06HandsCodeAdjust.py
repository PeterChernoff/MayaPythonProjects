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


class pcCreateRigAlt06HandsCodeAdjust(object):
    def __init__(self, ):
        self.makeFingersComplete("l_")
        self.makeFingersComplete("r_")
        pass

    def makeFingersAttr(self, ctrl, attr, cmpdCTRLs, valPos, valNeg, drvnAttr, passVals, skipNeg=False, isLocked=False):
        # the 4 finger joints
        tangentToUse = ["linear", "linear"]
        for j in range(len(valPos)):
            if passVals[j]:
                if isLocked:
                    CRU.lockHideCtrls(cmpdCTRLs[j], rotate=True, attrVisible=True, toLock=False)
                    # to delete: need to relock things at the end

                CRU.setDriverDrivenValues(ctrl, attr, cmpdCTRLs[j], drvnAttr, 0, 0, modifyInOut=tangentToUse)
                CRU.setDriverDrivenValues(ctrl, attr, cmpdCTRLs[j], drvnAttr, 10, valPos[j], modifyInOut=tangentToUse)
                if not skipNeg:
                    CRU.setDriverDrivenValues(ctrl, attr, cmpdCTRLs[j], drvnAttr, -10, valNeg[j],
                                              modifyInOut=tangentToUse)

                if isLocked:
                    CRU.lockHideCtrls(cmpdCTRLs[j], rotate=True)

        return

    def makeFingersCompound(self, ctrlTIMRP, fingerAttr, cmpdCtrlTIMRP, isHand=False):
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
                valPos1 = [10, 40, 35, 90]
                valNeg1 = [-5, -15, -30, -25]

                # thumb scrunch
                valPos2 = [15, -25, 55, 90]
                valNeg2 = [0, -12, -20, -20]

                # thumb lean
                valPos3 = [0, 25, 25, 25]
                valNeg3 = [0, -25, -25, -25]

                # thumb relax
                #  no relax for thumb

                # thumb spread
                passVals5 = [True, True, True, False]
                drvnAttr5 = "rz"
                drvnAttr5y = "ry"

                valPos5 = [0, -15, -15, 0]
                valNeg5 = [45, 35, 0, 0]

                valPos5y = [0, -15, 0, 0]
                valNeg5y = [0, -40, 0, 0]

            else:
                # finger curls
                valPos1 = [10, 65, 80, 100]
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
                    valPos5 = [5, 15]
                    valNeg5 = [-5, -10]
                elif i == 2:
                    # middle
                    valPos5 = [-2, -1]
                    valNeg5 = [1, 1]
                elif i == 3:
                    # ring
                    valPos5 = [-5, -10]
                    valNeg5 = [5.5, 7.5]
                elif i == 4:
                    # pinky
                    valPos5 = [-7.5, -30]
                    valNeg5 = [10, 20]

            drvnAttr1 = "rz"
            drvnAttr2 = "rz"
            drvnAttr3 = "ry"
            drvnAttr4 = "rz"
            if isHand:
                ctrlPass = ctrlTIMRP
            else:
                ctrlPass = ctrlTIMRP[i]

            self.makeFingersAttr(ctrlPass, fingerAttr[0], cmpdCtrlTIMRP[i], valPos1, valNeg1, drvnAttr1, passVals1,
                                 isLocked=True)
            self.makeFingersAttr(ctrlPass, fingerAttr[1], cmpdCtrlTIMRP[i], valPos2, valNeg2, drvnAttr2, passVals2,
                                 isLocked=True)
            self.makeFingersAttr(ctrlPass, fingerAttr[2], cmpdCtrlTIMRP[i], valPos3, valNeg3, drvnAttr3, passVals3,
                                 isLocked=True)
            if i != 0:
                # skip the thumb
                self.makeFingersAttr(ctrlPass, fingerAttr[3], cmpdCtrlTIMRP[i], valPos4, valNeg4, drvnAttr4, passVals4,
                                     isLocked=True)
            self.makeFingersAttr(ctrlPass, fingerAttr[4], cmpdCtrlTIMRP[i], valPos5, valNeg5, drvnAttr5, passVals5,
                                 isLocked=True)
            if i == 0:
                self.makeFingersAttr(ctrlPass, fingerAttr[4], cmpdCtrlTIMRP[i], valPos5y, valNeg5y, drvnAttr5y,
                                     passVals5,
                                     isLocked=True)

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

                valPosX = [0, 10, 0, 0]
                drvnAttrX = "rx"

                valPosY = [0, 10, 0, 0]
                drvnAttrY = "ry"

            else:
                # finger curls
                valPosZ = [10, 65, 80, 100]
                # valPosZ = [10, 95, 95, 115]

            drvnAttr1 = "rz"

            self.makeFingersAttr(ctrlHand, handAttr[5], cmpdCtrlTIMRP[i], valPosZ, valNeg, drvnAttr1, passVals1,
                                 skipNeg=True, isLocked=True)
            if i == 0:
                # only for thumb
                self.makeFingersAttr(ctrlHand, handAttr[5], cmpdCtrlTIMRP[i], valPosX, valNeg, drvnAttrX, passVals1,
                                     skipNeg=True, isLocked=True)
                self.makeFingersAttr(ctrlHand, handAttr[5], cmpdCtrlTIMRP[i], valPosY, valNeg, drvnAttrY, passVals1,
                                     skipNeg=True, isLocked=True)
        return

    def makeSpreadFix(self, cmpdCtrlTIMRP, ctrlTIMRP, ctrlHand):
        fingerValsNeg = [-41, -15, -4, 1, 15]
        fingerValsPos = [15, 25, 5, -10, -30]
        for i in range(len(cmpdCtrlTIMRP)):

            if i == 0:
                CRU.setDriverDrivenValues(ctrlTIMRP[i], "spread", cmpdCtrlTIMRP[i][1], "rz", 0, 0, modifyBoth="linear")
                CRU.setDriverDrivenValues(ctrlTIMRP[i], "spread", cmpdCtrlTIMRP[i][1], "rz", -10, 35,
                                          modifyBoth="linear")
                CRU.setDriverDrivenValues(ctrlTIMRP[i], "spread", cmpdCtrlTIMRP[i][1], "rz", 10, -20,
                                          modifyBoth="linear")

                CRU.setDriverDrivenValues(ctrlHand, "spread", cmpdCtrlTIMRP[i][1], "rz", 0, 0, modifyBoth="linear")
                CRU.setDriverDrivenValues(ctrlHand, "spread", cmpdCtrlTIMRP[i][1], "rz", -10, 35, modifyBoth="linear")
                CRU.setDriverDrivenValues(ctrlHand, "spread", cmpdCtrlTIMRP[i][1], "rz", 10, -20, modifyBoth="linear")

            # sets the JNT_cmpdCTRL_finger1
            CRU.setDriverDrivenValues(ctrlTIMRP[i], "spread", cmpdCtrlTIMRP[i][1], "ry", 0, 0)
            CRU.setDriverDrivenValues(ctrlTIMRP[i], "spread", cmpdCtrlTIMRP[i][1], "ry", -10, fingerValsNeg[i],
                                      modifyBoth="linear")
            CRU.setDriverDrivenValues(ctrlTIMRP[i], "spread", cmpdCtrlTIMRP[i][1], "ry", 10, fingerValsPos[i],
                                      modifyBoth="linear")

            CRU.setDriverDrivenValues(ctrlHand, "spread", cmpdCtrlTIMRP[i][1], "ry", 0, 0)
            CRU.setDriverDrivenValues(ctrlHand, "spread", cmpdCtrlTIMRP[i][1], "ry", -10, fingerValsNeg[i],
                                      modifyBoth="linear")
            CRU.setDriverDrivenValues(ctrlHand, "spread", cmpdCtrlTIMRP[i][1], "ry", 10, fingerValsPos[i],
                                      modifyBoth="linear")
        return

    def getJntArray(self, jointArray, fingerType, subType=None):
        if subType is None:
            fingerArray = [x for x in jointArray if (fingerType in x.lower())]

        else:
            fingerArray = [x for x in jointArray if (fingerType in x.lower()) and subType in x]
        for i in range(len(fingerArray)):
            if "Base" in fingerArray[i]:
                move = fingerArray.pop(i)
                fingerArray.insert(0, move, )
                break

        if fingerType == "thumb":
            for i in range(len(fingerArray)):
                if "Orbit" in fingerArray[i]:
                    move = fingerArray.pop(i)
                    fingerArray.insert(1, move)
                    break

        return fingerArray

    def getSuperJntArray(self, jointArray, subType, isControl=False):
        jntThumbs = self.getJntArray(jointArray, "thumb", subType)
        jntPointer = self.getJntArray(jointArray, "pointer", subType)
        jntMiddle = self.getJntArray(jointArray, "middle", subType)
        jntRing = self.getJntArray(jointArray, "ring", subType)
        jntPink = self.getJntArray(jointArray, "pink", subType)

        if not isControl:
            jntTIMRP = [jntThumbs, jntPointer, jntMiddle, jntRing, jntPink]
        else:
            jntTIMRP = []
            jntTIMRP.extend(jntThumbs)
            jntTIMRP.extend(jntPointer)
            jntTIMRP.extend(jntMiddle)
            jntTIMRP.extend(jntRing)
            jntTIMRP.extend(jntPink)
        return jntTIMRP

    def makeFingersComplete(self, leftRight, *args):

        valsMinMaxDef = [-10, 10, 0]
        fingerAttr = ["curl", "scrunch", "lean", "relax", "spread"]

        cmpdCtrlTIMRP = mc.ls('*cmpdCTRL_{0}*'.format(leftRight), type='joint')

        # print("check: {0}".format(cmpdCtrlTIMRP))

        cmpdCtrlTIMRP = self.getSuperJntArray(cmpdCtrlTIMRP, "cmpdCTRL")

        # print("check: {0}".format(cmpdCtrlTIMRP))

        ctrlTIMRPSetup = mc.ls('CTRL_{0}*'.format(leftRight), type='nurbsCurve')

        ctrlTIMRPSetup = self.getSuperJntArray(ctrlTIMRPSetup, "CTRL", isControl=True)
        ctrlTIMRP = []
        for i in range(len(ctrlTIMRPSetup)):
            parent = mc.listRelatives(ctrlTIMRPSetup[i], p=True)[0]
            ctrlTIMRP.append(parent)

        # print("ctrlTIMRP: {0}".format(ctrlTIMRP))

        self.makeFingersCompound(ctrlTIMRP, fingerAttr, cmpdCtrlTIMRP)

        # create the hand
        ctrlHand = "CTRL_{0}hand".format(leftRight)

        handAttr = ["curl", "scrunch", "lean", "relax", "spread", "fist"]

        self.makeFingersCompound(ctrlHand, handAttr, cmpdCtrlTIMRP, isHand=True)

        self.makeFistCompound(ctrlHand, handAttr, cmpdCtrlTIMRP)

        # Compound finger controls
        # Palm Control

        # Spread  Fix
        self.makeSpreadFix(cmpdCtrlTIMRP, ctrlTIMRP, ctrlHand)
