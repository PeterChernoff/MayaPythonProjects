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
from pcCreateRigUtilities import pcCreateRigUtilities as CRU

reload(pcCreateRigUtilities)


class pcCreateRigFingers(UI):
    def __init__(self):

        self.window = "bcWindow"
        self.title = "pcRigFingers"
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

        mc.text(l="Mirror Fingers As Well?")
        # mc.setParent("..")
        mc.radioButtonGrp("selFingersMirrorType_rbg", la2=["No", "Yes"], nrb=2, sl=2, cw2=[50, 50], )
        mc.text(l="")
        mc.setParent("..")
        mc.separator(st="in", h=20, w=500)

        mc.rowColumnLayout(nc=3, cw=[(1, 100), (2, 200), (3, 150)], cs=[1, 5], rs=[1, 3],
                           cal=([1, "left"], [2, "left"], [3, "left"],))
        mc.text(l="Initial Limb: ")
        mc.radioButtonGrp("selFingersType_rbg", la2=["Left", "Right"], nrb=2, sl=1, cw2=[50, 50], )
        mc.setParent("..")
        mc.separator(st="in", h=20, w=500)

        # sources
        mc.rowColumnLayout(nc=2, cw=[(1, 100), (2, 370)], cs=[1, 5], rs=[1, 3])
        mc.text(bgc=(0.85, 0.65, 0.25), l="Fingers Control: ")
        mc.textFieldButtonGrp("ctrlFingersLoad_tfbg", cw=(1, 322), bl="  Load  ")

        mc.text(bgc=(0.85, 0.65, 0.25), l="Palm CTRL: ")
        mc.textFieldButtonGrp("ctrlPalmLoad_tf", cw=(1, 322), bl="  Load  ", tx="CTRL_l_palm")

        mc.setParent("..")

        mc.separator(st="in", h=20, w=500)

        # load buttons
        #

        mc.textFieldButtonGrp("ctrlFingersLoad_tfbg", e=True, bc=self.loadSrc1Btn)
        mc.textFieldButtonGrp("ctrlPalmLoad_tf", e=True, bc=self.loadSrc2Btn)

        self.selLoad = []
        self.ctrlsArray = []
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
        self.ctrlsSel = self.tgpLoadTxBtn("ctrlFingersLoad_tfbg", "nurbsCurve")
        print(self.ctrlsSel)

    def loadSrc2Btn(self):
        self.ctrlSel = self.loadCtrlBtn("ctrlPalmLoad_tf")
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
            return selName

            # print(selName)

    def tgpLoadTxBtn(self, loadBtn, myType):
        # hierarchy
        self.selLoad = []
        self.selLoad = mc.ls(sl=True, fl=True, type="transform")

        if (len(self.selLoad) != 1):
            mc.warning("Select only the root control")
            return
        else:

            if CRU.checkObjectType(self.selLoad[0]) != "nurbsCurve":
                mc.warning("The Control should be a nurbsCurve")
                return
            selName = ', '.join(self.selLoad)
            mc.textFieldButtonGrp(loadBtn, e=True, tx=selName)

            # get the children joints
            self.parent = self.selLoad[0]
            self.child = mc.listRelatives(self.selLoad, ad=True, type="transform")
            # collect the joints in an array
            self.ctrlsArray = [self.parent]
            # reverse the order of the children joints
            self.child.reverse()

            # add to the current list
            self.ctrlsArray.extend(self.child)
            # print(self.ctrlsArray)
            ctrlsArraySorted = []
            # print(self.ctrlsArray)
            # sort the array
            for i in range(len(self.ctrlsArray)):
                sels = mc.listRelatives(self.ctrlsArray[i], c=True, s=True)
                if myType in mc.objectType(sels) or myType == mc.objectType(sels):
                    ctrlsArraySorted.append(self.ctrlsArray[i])

            self.ctrlsRoot = self.selLoad[0]
            # print(ctrlsArraySorted)
            self.ctrlsArray = ctrlsArraySorted

        return self.ctrlsArray

    def makeFingers(self, ctrlPalm, ctrlsArray, leftRight, colourTU, *args):

        fingersPalmSetup = mc.listRelatives(ctrlPalm, ad=True, s=False)
        fingersPalmSetup.reverse()
        print(fingersPalmSetup)
        autoThumbs = [x for x in fingersPalmSetup if ("thumb" in x.lower()) and "AUTO" in x]
        autoIndex = [x for x in fingersPalmSetup if ("index" in x.lower()) and "AUTO" in x]
        autoMiddle = [x for x in fingersPalmSetup if ("middle" in x.lower()) and "AUTO" in x]
        autoRing = [x for x in fingersPalmSetup if ("ring" in x.lower()) and "AUTO" in x]
        autoPink = [x for x in fingersPalmSetup if ("pink" in x.lower()) and "AUTO" in x]
        ctrlFingers = [x for x in ctrlsArray if ("fingers" in x.lower())][0]
        ctrlArrayFingers = [x for x in ctrlsArray if ("fingers" not in x.lower())]
        ctrlThumb = [x for x in ctrlsArray if ("thumb" in x.lower())][0]
        ctrlIndex = [x for x in ctrlsArray if ("index" in x.lower())][0]
        ctrlMiddle = [x for x in ctrlsArray if ("middle" in x.lower())][0]
        ctrlRing = [x for x in ctrlsArray if ("ring" in x.lower())][0]
        ctrlPink = [x for x in ctrlsArray if ("pink" in x.lower())][0]

        # TIMRP = Thumb, Index, Middle, Ring, Pinkie
        autoTIMRP = [autoThumbs, autoIndex, autoMiddle, autoRing, autoPink]

        ctrlTIMRP = [ctrlThumb, ctrlIndex, ctrlMiddle, ctrlRing, ctrlPink]

        fingerAttr = ["curl", "scrunch", "spread"]
        handAttr = list(fingerAttr)

        handAttr.append("relax")
        valsMinMaxDef = [-10, 10, 0]

        # add the fingers control attributes
        for i in range(len(handAttr)):
            mc.addAttr(ctrlFingers, longName=handAttr[i], at="float", k=True, min=valsMinMaxDef[0],
                       max=valsMinMaxDef[1], dv=valsMinMaxDef[2])

        # add the fingers control attributes for the individual fingers
        for i in range(len(fingerAttr)):
            for j in range(len(ctrlTIMRP)):
                mc.addAttr(ctrlTIMRP[j], longName=fingerAttr[i], at="float", k=True, min=valsMinMaxDef[0],
                           max=valsMinMaxDef[1], dv=valsMinMaxDef[2])

        # creating the Finger Curl
        self.fingerCurlsSetup(ctrlArrayFingers, autoTIMRP, ctrlFingers, handAttr)

        # creating the Finger scrunch
        self.fingerScrunchSetup(ctrlArrayFingers, autoTIMRP, ctrlFingers, handAttr)

        # creating the Finger spread
        self.fingerSpreadSetup(ctrlArrayFingers, autoTIMRP, ctrlFingers, handAttr)

        # creating the Finger relax
        self.fingerRelaxSetup(ctrlArrayFingers, autoTIMRP, ctrlFingers, handAttr)

        # Cleaning up
        self.fingersCleanup(ctrlFingers, ctrlPalm, colourTU)

    def fingersCleanup(self, ctrlFingers, ctrlPalm, colourTU, *args):

        mc.parent(ctrlFingers, ctrlPalm)

        checkList = mc.listRelatives(ctrlFingers)
        for i in range(len(checkList)):
            if mc.objectType(checkList[i]) == "transform":
                CRU.lockHideCtrls(checkList[i], translate=True, rotate=True, scale=True, toHide=True, visible=True,
                                  toLock=False)
        mc.makeIdentity(ctrlFingers, apply=True, translate=True, rotate=True, scale=True)

        # get the non-shape values
        lockValues = mc.listRelatives(ctrlFingers, c=True, s=False, type="transform")
        lockValues.append(ctrlFingers)
        print(lockValues)

        for i in range(len(lockValues)):
            CRU.lockHideCtrls(lockValues[i], translate=True, rotate=True, scale=True, visible=True)

            mc.setAttr('{0}.overrideEnabled'.format(lockValues[i]), 1)
            mc.setAttr("{0}.overrideColor".format(lockValues[i]), colourTU)

    def fingerCurlsSetup(self, ctrlArrayFingers, autoTIMRP, ctrlFingers, fingerAttr, *args):

        # set at 0 for curl and rotateX, and the thumb values
        driverVal = 0
        self.fingerCurls(ctrlArrayFingers, autoTIMRP, ctrlFingers, fingerAttr, driverVal, fingersAttrArray=0,
                         thumbsAttrArrayDriven=0, )

        # self.fingerCurlsIndividual(ctrlArrayFingers, autoTIMRP, fingerAttr, driverVal, fingersCurlArray=0, thumbsCurlArrayDriven=0)

        # set at 10 for curl and rotateX, and the thumb values

        thumbCurlsXP10 = [10, 45, 70]
        thumbCurlsZP10 = [20, 0]

        curlsFinger1XP10 = 5

        indexCurlP10 = 70
        indexCurlsP10 = [curlsFinger1XP10, indexCurlP10, indexCurlP10, indexCurlP10]

        middleCurlP10 = 76
        middleCurlsP10 = [curlsFinger1XP10, middleCurlP10, middleCurlP10, middleCurlP10]

        ringCurlP10 = 67
        ringCurlsP10 = [curlsFinger1XP10, ringCurlP10, ringCurlP10, ringCurlP10]

        pinkCurlP10 = 67
        pinkCurlsP10 = [curlsFinger1XP10, pinkCurlP10, pinkCurlP10, pinkCurlP10]
        fingersCurlXP10 = [thumbCurlsXP10, indexCurlsP10, middleCurlsP10, ringCurlsP10, pinkCurlsP10]

        driverVal = 10
        self.fingerCurls(ctrlArrayFingers, autoTIMRP, ctrlFingers, fingerAttr, driverVal, fingersCurlXP10,
                         thumbCurlsZP10, )
        # self.fingerCurlsIndividual(ctrlArrayFingers, autoTIMRP, fingerAttr, driverVal, fingersCurlXP10, thumbCurlsZP10)

        # set at -10 for curl and rotateX, and the thumb values

        fingersCurlXN10 = []

        thumbCurlsXN10 = [-10, -15, -10]
        thumbCurlsZN10 = [-10, -10]

        fingersCurlXN10.append(thumbCurlsXN10)
        # index middle
        curls_IMX1_N10 = -3
        # ring pinkie
        curls_RPX1_N10 = -4
        curlsRestN10 = -25

        indexCurlsN10 = [curls_IMX1_N10, curlsRestN10, curlsRestN10, curlsRestN10]

        middleCurlsN10 = [curls_IMX1_N10, curlsRestN10, curlsRestN10, curlsRestN10]

        ringCurlsN10 = [curls_RPX1_N10, curlsRestN10, curlsRestN10, curlsRestN10]

        pinkCurlsN10 = [curls_RPX1_N10, curlsRestN10, curlsRestN10, curlsRestN10]
        fingersCurlXN10 = [thumbCurlsXN10, indexCurlsN10, middleCurlsN10, ringCurlsN10, pinkCurlsN10]

        driverVal = -10
        self.fingerCurls(ctrlArrayFingers, autoTIMRP, ctrlFingers, fingerAttr, driverVal, fingersCurlXN10,
                         thumbCurlsZN10, )

    def fingerCurls(self, ctrlArrayFingers, autoTIMRP, ctrlFingers, fingerAttr, driverVal, fingersAttrArray=0,
                    thumbsAttrArrayDriven=0, *args):
        # sets the value for the finger curls, and the individual finger curls
        fingerAttrVal = fingerAttr[0]

        for i in range(len(ctrlArrayFingers)):
            for j in range(len(autoTIMRP[i])):
                # setDriverDrivenValues(driver, driverAttribute, driven, drivenAttribute, driverValue, drivenValue,):
                # set all the x values in curl to 0
                if isinstance(fingersAttrArray, int):
                    valToUse = fingersAttrArray

                else:

                    valToUse = fingersAttrArray[i][j]
                CRU.setDriverDrivenValues(ctrlFingers, fingerAttrVal, autoTIMRP[i][j], "rotateX", driverVal,
                                          valToUse)
                CRU.setDriverDrivenValues(ctrlArrayFingers[i], fingerAttrVal, autoTIMRP[i][j], "rotateX",
                                          driverVal, valToUse)

        if isinstance(thumbsAttrArrayDriven, int):
            # if the value is an integer, we use the integer, if the value is a list, we use the list
            valToUse = [thumbsAttrArrayDriven, thumbsAttrArrayDriven]
        else:
            valToUse = [thumbsAttrArrayDriven[0], thumbsAttrArrayDriven[1]]

        CRU.setDriverDrivenValues(ctrlFingers, fingerAttr[0], autoTIMRP[0][0], "rotateZ", driverVal, valToUse[0])
        CRU.setDriverDrivenValues(ctrlFingers, fingerAttr[0], autoTIMRP[0][1], "rotateZ", driverVal, valToUse[1])

        CRU.setDriverDrivenValues(ctrlArrayFingers[0], fingerAttrVal, autoTIMRP[0][0], "rotateZ", driverVal,
                                  valToUse[0])
        CRU.setDriverDrivenValues(ctrlArrayFingers[0], fingerAttrVal, autoTIMRP[0][1], "rotateZ", driverVal,
                                  valToUse[1])

    def fingerScrunchSetup(self, ctrlArrayFingers, autoTIMRP, ctrlFingers, fingerAttr, *args):

        driverVal = 0

        self.fingerScrunch(ctrlArrayFingers, autoTIMRP, ctrlFingers, fingerAttr, driverVal, 0, 0)

        driverVal = 10
        scrunchFinger_2XP10 = -50
        scrunchFinger_3XP10 = 50
        scrunchFinger_4XP10 = 50
        scrunchFingers_234XP10 = [0, scrunchFinger_2XP10, scrunchFinger_3XP10, scrunchFinger_4XP10]

        scrunchThumb_2XP10 = -30
        scrunchThumb_3XP10 = 80
        scrunchThumb_23XP10 = [0, scrunchThumb_2XP10, scrunchThumb_3XP10]

        self.fingerScrunch(ctrlArrayFingers, autoTIMRP, ctrlFingers, fingerAttr, driverVal, scrunchFingers_234XP10,
                           scrunchThumb_23XP10)

        driverVal = -10
        scrunchFinger_2XN10 = 15
        scrunchFinger_3XN10 = -30
        scrunchFinger_4XN10 = -40
        scrunchFingers_234XN10 = [0, scrunchFinger_2XN10, scrunchFinger_3XN10, scrunchFinger_4XN10]

        scrunchThumb_2XN10 = 20
        scrunchThumb_3XN10 = -40
        scrunchThumb_23XN10 = [0, scrunchThumb_2XN10, scrunchThumb_3XN10]
        self.fingerScrunch(ctrlArrayFingers, autoTIMRP, ctrlFingers, fingerAttr, driverVal, scrunchFingers_234XN10,
                           scrunchThumb_23XN10)

    def fingerScrunch(self, ctrlArrayFingers, autoTIMRP, ctrlFingers, fingerAttr, driverVal, fingersAttrArray=0,
                      thumbsAttrArrayDriven=0, *args):
        # sets the value for the finger scrunch, and the individual finger scrunches
        fingerAttrVal = fingerAttr[1]

        for i in range(len(ctrlArrayFingers)):
            for j in range(len(autoTIMRP[i])):
                # setDriverDrivenValues(driver, driverAttribute, driven, drivenAttribute, driverValue, drivenValue,):
                # set all the x values in curl to 0
                if j != 0:
                    if i == 0:
                        # 0 is the thumb version, if properly set up

                        if isinstance(thumbsAttrArrayDriven, int):
                            valToUse = thumbsAttrArrayDriven
                        else:
                            valToUse = thumbsAttrArrayDriven[j]
                        # sets the thumb as a fingers control
                        CRU.setDriverDrivenValues(ctrlFingers, fingerAttrVal, autoTIMRP[i][j], "rotateX", driverVal,
                                                  valToUse)
                        # sets the thumb individual control
                        CRU.setDriverDrivenValues(ctrlArrayFingers[i], fingerAttrVal, autoTIMRP[i][j], "rotateX",
                                                  driverVal, valToUse)
                    else:
                        # the rest are the other fingers
                        if isinstance(fingersAttrArray, int):
                            valToUse = fingersAttrArray
                        else:
                            valToUse = fingersAttrArray[j]
                        # sets the fingers as a whole

                        CRU.setDriverDrivenValues(ctrlFingers, fingerAttrVal, autoTIMRP[i][j], "rotateX", driverVal,
                                                  valToUse)
                        # sets the fingers individually
                        CRU.setDriverDrivenValues(ctrlArrayFingers[i], fingerAttrVal, autoTIMRP[i][j], "rotateX",
                                                  driverVal, valToUse)

    def fingerSpreadSetup(self, ctrlArrayFingers, autoTIMRP, ctrlFingers, fingerAttr, *args):

        driverVal = 0

        self.fingerSpread(ctrlArrayFingers, autoTIMRP, ctrlFingers, fingerAttr, driverVal, 0, 0)

        driverVal = 10

        spreadX_P10_Thumb = [-12, -12]
        spreadZ_P10_Thumb = [4, 4]
        spread_P10Thumb = [spreadX_P10_Thumb, spreadZ_P10_Thumb]

        spreadZ_P10_Index = [2, 15]
        spreadZ_P10_Middle = [1, 7]
        spreadZ_P10_Ring = [-1, -8]
        spreadZ_P10_Pink = [-2, -15]
        spreadZ_P10_Fingers = [0, spreadZ_P10_Index, spreadZ_P10_Middle, spreadZ_P10_Ring, spreadZ_P10_Pink]

        self.fingerSpread(ctrlArrayFingers, autoTIMRP, ctrlFingers, fingerAttr, driverVal, spreadZ_P10_Fingers,
                          spread_P10Thumb)

        driverVal = -10
        spreadX_N10_Thumb = [12, 12]
        spreadZ_N10_Thumb = [-14, -14]
        spread_N10Thumb = [spreadX_N10_Thumb, spreadZ_N10_Thumb]

        spreadZ_N10_Index = [-5, -15]
        spreadZ_N10_Middle = [-2, -4]
        spreadZ_N10_Ring = [2, 5]
        spreadZ_N10_Pink = [5, 17]
        spreadZ_N10_Fingers = [0, spreadZ_N10_Index, spreadZ_N10_Middle, spreadZ_N10_Ring, spreadZ_N10_Pink]
        self.fingerSpread(ctrlArrayFingers, autoTIMRP, ctrlFingers, fingerAttr, driverVal, spreadZ_N10_Fingers,
                          spread_N10Thumb)

    def fingerSpread(self, ctrlArrayFingers, autoTIMRP, ctrlFingers, fingerAttr, driverVal, fingersAttrArray=0,
                     thumbsAttrArrayDriven=0, *args):
        # sets the value for the finger scrunch, and the individual finger scrunches
        fingerAttrVal = fingerAttr[2]
        for i in range(len(ctrlArrayFingers)):
            for j in range(len(autoTIMRP[i])):
                # setDriverDrivenValues(driver, driverAttribute, driven, drivenAttribute, driverValue, drivenValue,):
                # set all the x values in curl to 0
                if j < 2:
                    # we only do this for the first two finger joints
                    if i == 0:
                        # 0 is the thumb version, if properly set up

                        if isinstance(thumbsAttrArrayDriven, int):
                            valToUseX = thumbsAttrArrayDriven
                            valToUseZ = thumbsAttrArrayDriven
                        else:
                            valToUseX = thumbsAttrArrayDriven[0][j]
                            valToUseZ = thumbsAttrArrayDriven[1][j]
                        # sets the thumb as a fingers control
                        CRU.setDriverDrivenValues(ctrlFingers, fingerAttrVal, autoTIMRP[i][j], "rotateX", driverVal,
                                                  valToUseX)
                        CRU.setDriverDrivenValues(ctrlFingers, fingerAttrVal, autoTIMRP[i][j], "rotateZ", driverVal,
                                                  valToUseZ)

                        # sets the thumb individual control
                        CRU.setDriverDrivenValues(ctrlArrayFingers[i], fingerAttrVal, autoTIMRP[i][j], "rotateX",
                                                  driverVal, valToUseX)
                        CRU.setDriverDrivenValues(ctrlArrayFingers[i], fingerAttrVal, autoTIMRP[i][j], "rotateZ",
                                                  driverVal, valToUseZ)
                    else:

                        if isinstance(fingersAttrArray, int):
                            valToUse = fingersAttrArray
                        else:
                            valToUse = fingersAttrArray[i][j]
                        # sets the thumb as a fingers control
                        CRU.setDriverDrivenValues(ctrlFingers, fingerAttrVal, autoTIMRP[i][j], "rotateZ", driverVal,
                                                  valToUse)

                        # sets the thumb individual control
                        CRU.setDriverDrivenValues(ctrlArrayFingers[i], fingerAttrVal, autoTIMRP[i][j], "rotateZ",
                                                  driverVal, valToUse)

    def fingerRelaxSetup(self, ctrlArrayFingers, autoTIMRP, ctrlFingers, fingerAttr, *args):

        driverVal = 0

        self.fingerRelax(ctrlArrayFingers, autoTIMRP, ctrlFingers, fingerAttr, driverVal, 0, 0)

        driverVal = 10

        relaxX_P10_Index = [2, 10, 20, 25]
        relaxX_P10_Middle = [4, 15, 25, 30]
        relaxX_P10_Ring = [6, 20, 30, 35]
        relaxX_P10_Pink = [8, 25, 35, 40]
        relaxX_P10_Fingers = [0, relaxX_P10_Index, relaxX_P10_Middle, relaxX_P10_Ring, relaxX_P10_Pink]

        self.fingerRelax(ctrlArrayFingers, autoTIMRP, ctrlFingers, fingerAttr, driverVal, relaxX_P10_Fingers)

        driverVal = -10

        relaxX_N10_Index = [8, 30, 40, 45]
        relaxX_N10_Middle = [6, 25, 35, 40]
        relaxX_N10_Ring = [4, 15, 25, 30]
        relaxX_N10_Pink = [2, 10, 20, 25]
        relaxX_N10_Fingers = [0, relaxX_N10_Index, relaxX_N10_Middle, relaxX_N10_Ring, relaxX_N10_Pink]
        self.fingerRelax(ctrlArrayFingers, autoTIMRP, ctrlFingers, fingerAttr, driverVal, relaxX_N10_Fingers)

    def fingerRelax(self, ctrlArrayFingers, autoTIMRP, ctrlFingers, fingerAttr, driverVal, fingersAttrArray=0, *args):
        # sets the value for the finger scrunch, and the individual finger scrunches
        fingerAttrVal = fingerAttr[3]
        for i in range(len(ctrlArrayFingers)):
            # skip the thumb
            if i != 0:
                for j in range(len(autoTIMRP[i])):
                    # setDriverDrivenValues(driver, driverAttribute, driven, drivenAttribute, driverValue, drivenValue,):
                    # set all the x values in curl to 0
                    # we skip the thumb
                    if isinstance(fingersAttrArray, int):
                        valToUse = fingersAttrArray
                    else:
                        valToUse = fingersAttrArray[i][j]
                    # sets the fingers as a whole
                    # we don't work with the fingers individually
                    CRU.setDriverDrivenValues(ctrlFingers, fingerAttrVal, autoTIMRP[i][j], "rotateX", driverVal,
                                              valToUse)

    def tgpCreateMirror(self, ctrlFingers, leftRightReplace, leftRightReplaceMirror):
        ctrlFingersMirrorWork = mc.duplicate(ctrlFingers, rc=True)

        ctrlFingersMirror = []

        offsetCtrlStuffMirror = []
        for i in range(len(ctrlFingersMirrorWork)):
            # switch the l/r,
            print("--------")
            print(ctrlFingersMirrorWork[i])
            toRename = ctrlFingersMirrorWork[i].replace(leftRightReplace, leftRightReplaceMirror)[:-1]
            print(toRename)
            mc.rename(ctrlFingersMirrorWork[i], toRename)
            ctrlFingersMirror.append(toRename)
        ctrlFingersMirrorTop = ctrlFingersMirror[0]
        # takes the initial offset value, duplicates it, flips the values around, then freezes the transformation
        # translates everything into place
        mirrorTrans = mc.xform(ctrlFingersMirrorTop, q=True, ws=True, rotatePivot=True)
        mirrorRot = mc.xform(ctrlFingersMirrorTop, q=True, ws=True, rotation=True)
        print("MirrorTrans = {0}".format(mirrorTrans))
        print("MirrorAxis = {0}".format(mirrorRot))
        mirrorTransX = mirrorTrans[0] * -1
        mirrorTransY = mirrorTrans[1]
        mirrorTransZ = mirrorTrans[2]
        mirrorRotX = mirrorRot[0] * 1
        mirrorRotY = mirrorRot[1] * -1
        mirrorRotZ = mirrorRot[2] * -1

        mirrorXScal = mc.getAttr("{0}.sx".format(ctrlFingersMirrorTop)) * -1
        print(mirrorTrans)
        print(mirrorXScal)

        # mirrors the values
        '''mc.setAttr("{0}.tx".format(ctrlFingersMirrorTop), mirrorTransX)
        mc.setAttr("{0}.sx".format(ctrlFingersMirrorTop), mirrorXScal)
        mc.setAttr("{0}.rx".format(ctrlFingersMirrorTop), mirrorRotX)
        mc.setAttr("{0}.ry".format(ctrlFingersMirrorTop), mirrorRotY)
        mc.setAttr("{0}.rz".format(ctrlFingersMirrorTop), mirrorRotZ)'''

        mc.xform(ctrlFingersMirrorTop, translation=(mirrorTransX, mirrorTransY, mirrorTransZ))
        mc.xform(ctrlFingersMirrorTop, scale=( mirrorXScal, 1, 1) )
        mc.xform(ctrlFingersMirrorTop, rotation = (mirrorRotX, mirrorRotY, mirrorRotZ))

        checkList = mc.listRelatives(ctrlFingersMirrorTop)
        for i in range(len(checkList)):
            if mc.objectType(checkList[i]) == "transform":
                CRU.lockHideCtrls(checkList[i], translate=True, rotate=True, scale=True, toHide=True, visible=True,
                                  toLock=False)
        # mc.scale(-1, ctrlFingersMirrorTop, x=True, pivot=(0,0,0), a=True)
        mc.makeIdentity(ctrlFingersMirrorTop, apply=True, translate=True, scale=True)

        return ctrlFingersMirror, ctrlFingersMirrorTop

    def tgpMakeBC(self, *args):

        checkSelLeft = mc.radioButtonGrp("selFingersType_rbg", q=True, select=True)
        mirrorSel = mc.radioButtonGrp("selFingersMirrorType_rbg", q=True, select=True)
        ctrlFingerNames = mc.textFieldButtonGrp("ctrlFingersLoad_tfbg", q=True, text=True)

        ctrlPalm = mc.textFieldButtonGrp("ctrlPalmLoad_tf", q=True, text=True)

        try:
            fingerRoot = self.ctrlsArray[0]

        except:
            mc.warning("No locator selected!")
            return

        ctrlsArray = self.ctrlsArray

        print("-------")

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
        checkList = [ctrlFingerNames]
        # note: the isCopy is not applicable due to the differences between the leg and arm joint setup.
        # However, editing them out is too much hassle,  it's easier just to leave them both false
        if ((checkList[0] == "")):
            mc.warning("You are missing a selection!")
            return
        else:

            CRU.createLocatorToDelete()

            if mirrorRig:
                # we want to get the finger control before we add anything to it. When doing this programmatically, it's easier
                # make sure the children are not locked
                ctrlsArrayMirror, ctrlFingerNames = self.tgpCreateMirror(ctrlFingerNames, leftRightReplace,
                                                                         leftRightReplaceMirror)

            self.makeFingers(ctrlPalm, ctrlsArray, leftRight, colourTU)

            print(mirrorRig)
            if mirrorRig:
                print("I got here!")

                isLeftMirror = not isLeft

                ctrlPalmMirror = ctrlPalm.replace(leftRightReplace, leftRightReplaceMirror)

                print(ctrlsArray)

                self.makeFingers(ctrlPalmMirror, ctrlsArrayMirror, leftRightMirror, colourTUMirror)
