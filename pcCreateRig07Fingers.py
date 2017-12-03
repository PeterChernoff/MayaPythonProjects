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
from pcCreateRig00AUtilities import pcCreateRigUtilities as CRU

reload(pcCreateRig00AUtilities)


class pcCreateRig07Fingers(UI):
    def __init__(self):

        self.window = "bcWindow"
        self.title = "pcRigFingers"
        self.winSize = (500, 325)

        self.createUI()

    def createCustom(self, *args):
        # selection type

        mc.rowColumnLayout(nc=2, cw=[(1, 500), (2, 500)], cs=[1, 5], rs=[1, 3])

        mc.text(l="Select The Fingers Control: ")
        mc.text(l="")
        mc.separator(st="in", h=17, w=500)
        mc.setParent("..")
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
        mc.rowColumnLayout(nc=2, cw=[(1, 100), (2, 380)], cs=[1, 5], rs=[1, 3])
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
        self.selSrc1 = self.tgpLoadCtrlsBtn("ctrlFingersLoad_tfbg", "nurbsCurve", "Fingers Control", ["CTRL", "fingers"],
                                             "control")
        print(self.selSrc1)

    def loadSrc2Btn(self):
        self.selSrc2 = self.tgpLoadTxBtn("ctrlPalmLoad_tf", "nurbsCurve", "Palm Control", ["CTRL", "palm"],
                                         "control")
        print(self.selSrc2)

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

    def tgpLoadCtrlsBtn(self, loadBtn, objectType, objectDesc, keywords, objectNickname=None):
        if objectNickname is None:
            objectNickname = objectType
        # hierarchy
        self.selLoad = []
        self.selLoad = mc.ls(sl=True, fl=True, type="transform")

        if (len(self.selLoad) != 1):
            mc.warning("Select only the {0} control".format(objectDesc))
            return
        else:

            if CRU.checkObjectType(self.selLoad[0]) != objectType:
                mc.warning("The Control should be a {0}".format(objectType))
                return
            selName = self.selLoad[0]

            if not all(word.lower() in selName.lower() for word in keywords):
                mc.warning("That is the wrong {0}. Select the {1}".format(objectNickname, objectDesc))
                return

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
            ctrlsArraySorted = []
            # sort the array
            for i in range(len(self.ctrlsArray)):
                sels = mc.listRelatives(self.ctrlsArray[i], c=True, s=True)
                if objectType in mc.objectType(sels) or objectType == mc.objectType(sels):
                    ctrlsArraySorted.append(self.ctrlsArray[i])

            self.ctrlsRoot = self.selLoad[0]
            self.ctrlsArray = ctrlsArraySorted

        return self.ctrlsArray

    def makeFingers(self, ctrlPalm, ctrlsArray, leftRight, colourTU, *args):

        fingersPalmSetup = mc.listRelatives(ctrlPalm, ad=True, s=False)
        fingersPalmSetup.reverse()
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

        for i in range(len(lockValues)):
            CRU.lockHideCtrls(lockValues[i], translate=True, rotate=True, scale=True, visible=True)

            mc.setAttr('{0}.overrideEnabled'.format(lockValues[i]), 1)
            mc.setAttr("{0}.overrideColor".format(lockValues[i]), colourTU)

    def fingerCurlsSetup(self, ctrlArrayFingers, autoTIMRP, ctrlFingers, fingerAttr, *args):

        # set at 0 for curl and rotateX, and the thumb values
        driverVal = 0
        curl_P0_Digits = []
        # setup for the 0 curls
        for i in range(len(autoTIMRP)):
            if i == 0:
                curl_P0_Digits.append([[0, 0, 0], autoTIMRP[i], ctrlArrayFingers[i], "rotateX", ])
                curl_P0_Digits.append([[0, 0, None], autoTIMRP[i], ctrlArrayFingers[i], "rotateZ", ])
            else:
                fingersToAddX = [[0, 0, 0, 0], autoTIMRP[i], ctrlArrayFingers[i], "rotateX", ]
                curl_P0_Digits.append(fingersToAddX)

        self.setDigitVals(curl_P0_Digits, driverVal, ctrlFingers, fingerAttr[0])

        # set at 10 for curl and rotateX, and the thumb values
        driverVal = 10

        curl_P10_ThumbX = [[10, 45, 70], autoTIMRP[0], ctrlArrayFingers[0], "rotateX", ]
        curl_P10_ThumbZ = [[20, 0, None], autoTIMRP[0], ctrlArrayFingers[0], "rotateZ", ]

        curl_P10_IndexX = [[5, 70, 70, 70], autoTIMRP[1], ctrlArrayFingers[1], "rotateX", ]
        curl_P10_MiddleX = [[5, 76, 76, 76], autoTIMRP[2], ctrlArrayFingers[2], "rotateX", ]
        curl_P10_RingX = [[5, 67, 67, 67], autoTIMRP[3], ctrlArrayFingers[3], "rotateX", ]
        curl_P10_PinkX = [[5, 62, 62, 62], autoTIMRP[4], ctrlArrayFingers[4], "rotateX", ]

        curl_P10_Digits = [curl_P10_ThumbX, curl_P10_ThumbZ,
                           curl_P10_IndexX,
                           curl_P10_MiddleX,
                           curl_P10_RingX,
                           curl_P10_PinkX]

        self.setDigitVals(curl_P10_Digits, driverVal, ctrlFingers, fingerAttr[0])

        # set at -10 for curl and rotateX, and the thumb values
        driverVal = -10
        curl_N10_DigitsIM = [-3, -25, -25, -25]
        curl_N10_DigitsRP = [-4, -25, -25, -25]

        curl_N10_ThumbX = [[-10, -15, -10], autoTIMRP[0], ctrlArrayFingers[0], "rotateX", ]
        curl_N10_ThumbZ = [[-10, 10, None], autoTIMRP[0], ctrlArrayFingers[0], "rotateZ", ]

        curl_N10_IndexX = [curl_N10_DigitsIM, autoTIMRP[1], ctrlArrayFingers[1], "rotateX", ]
        curl_N10_MiddleX = [curl_N10_DigitsIM, autoTIMRP[2], ctrlArrayFingers[2], "rotateX", ]
        curl_N10_RingX = [curl_N10_DigitsRP, autoTIMRP[3], ctrlArrayFingers[3], "rotateX", ]
        curl_N10_PinkX = [curl_N10_DigitsRP, autoTIMRP[4], ctrlArrayFingers[4], "rotateX", ]

        curl_N10_Digits = [curl_N10_ThumbX, curl_N10_ThumbZ,
                           curl_N10_IndexX,
                           curl_N10_MiddleX,
                           curl_N10_RingX,
                           curl_N10_PinkX]

        self.setDigitVals(curl_N10_Digits, driverVal, ctrlFingers, fingerAttr[0])

    def fingerScrunchSetup(self, ctrlArrayFingers, autoTIMRP, ctrlFingers, fingerAttr, *args):

        driverVal = 0

        scrunch_P0_Digits = []
        # setup for the 0 scrunch
        for i in range(len(autoTIMRP)):
            if i == 0:
                scrunch_P0_Digits.append([[None, 0, 0], autoTIMRP[i], ctrlArrayFingers[i], "rotateX", ])
            else:
                scrunch_P0_Digits.append([[None, 0, 0, 0], autoTIMRP[i], ctrlArrayFingers[i], "rotateX", ])
                # scrunch_P0_Digits.append(fingersToAddX)

        self.setDigitVals(scrunch_P0_Digits, driverVal, ctrlFingers, fingerAttr[1])

        driverVal = 10
        scrunch_P10_Other = [None, -50, 50, 50]  # good value

        scrunch_P10_ThumbsX = [[None, -30, 80], autoTIMRP[0], ctrlArrayFingers[0], "rotateX", ]
        scrunch_P10_IndexX = [scrunch_P10_Other, autoTIMRP[1], ctrlArrayFingers[1], "rotateX", ]
        scrunch_P10_MiddleX = [scrunch_P10_Other, autoTIMRP[2], ctrlArrayFingers[2], "rotateX", ]
        scrunch_P10_RingX = [scrunch_P10_Other, autoTIMRP[3], ctrlArrayFingers[3], "rotateX", ]
        scrunch_P10_PinkX = [scrunch_P10_Other, autoTIMRP[4], ctrlArrayFingers[4], "rotateX", ]

        scrunch_P10_Digits = [scrunch_P10_ThumbsX,
                              scrunch_P10_IndexX,
                              scrunch_P10_MiddleX,
                              scrunch_P10_RingX,
                              scrunch_P10_PinkX]
        self.setDigitVals(scrunch_P10_Digits, driverVal, ctrlFingers, fingerAttr[1])

        driverVal = -10
        scrunch_N10_Other = [None, 15, -30, -40]

        scrunch_N10_ThumbsX = [[None, 20, -40], autoTIMRP[0], ctrlArrayFingers[0], "rotateX", ]
        scrunch_N10_IndexX = [scrunch_N10_Other, autoTIMRP[1], ctrlArrayFingers[1], "rotateX", ]
        scrunch_N10_MiddleX = [scrunch_N10_Other, autoTIMRP[2], ctrlArrayFingers[2], "rotateX", ]
        scrunch_N10_RingX = [scrunch_N10_Other, autoTIMRP[3], ctrlArrayFingers[3], "rotateX", ]
        scrunch_N10_PinkX = [scrunch_N10_Other, autoTIMRP[4], ctrlArrayFingers[4], "rotateX", ]

        scrunch_N10_Digits = [scrunch_N10_ThumbsX,
                              scrunch_N10_IndexX,
                              scrunch_N10_MiddleX,
                              scrunch_N10_RingX,
                              scrunch_N10_PinkX]
        self.setDigitVals(scrunch_N10_Digits, driverVal, ctrlFingers, fingerAttr[1])

    def fingerSpreadSetup(self, ctrlArrayFingers, autoTIMRP, ctrlFingers, fingerAttr, *args):
        driverVal = 0

        spread_P0_Digits = []
        # setup for the 0 spread
        for i in range(len(autoTIMRP)):
            if i == 0:
                spread_P0_Digits.append([[0, 0, None], autoTIMRP[i], ctrlArrayFingers[i], "rotateX", ])
                spread_P0_Digits.append([[0, 0, None], autoTIMRP[i], ctrlArrayFingers[i], "rotateZ", ])
            else:
                spread_P0_Digits.append([[0, 0, None, None], autoTIMRP[i], ctrlArrayFingers[i], "rotateZ", ])
                # spread_P0_Digits.append(fingersToAddX)

        self.setDigitVals(spread_P0_Digits, driverVal, ctrlFingers, fingerAttr[2])

        driverVal = 10

        spread_P10_ThumbsX = [[-12, -12, None], autoTIMRP[0], ctrlArrayFingers[0], "rotateX", ]
        spread_P10_ThumbsZ = [[4, 4, None], autoTIMRP[0], ctrlArrayFingers[0], "rotateZ", ]

        spread_P10_IndexZ = [[2, 15, None, None], autoTIMRP[1], ctrlArrayFingers[1], "rotateZ", ]
        spread_P10_MiddleZ = [[1, 7, None, None], autoTIMRP[2], ctrlArrayFingers[2], "rotateZ", ]
        spread_P10_RingZ = [[-1, -8, None, None], autoTIMRP[3], ctrlArrayFingers[3], "rotateZ", ]
        spread_P10_PinkZ = [[-2, -15, None, None], autoTIMRP[4], ctrlArrayFingers[4], "rotateZ", ]

        spread_P10_Digits = [spread_P10_ThumbsX, spread_P10_ThumbsZ,
                             spread_P10_IndexZ,
                             spread_P10_MiddleZ,
                             spread_P10_RingZ,
                             spread_P10_PinkZ]
        self.setDigitVals(spread_P10_Digits, driverVal, ctrlFingers, fingerAttr[2])

        driverVal = -10

        spread_N10_ThumbsX = [[12, 12, None], autoTIMRP[0], ctrlArrayFingers[0], "rotateX", ]
        spread_N10_ThumbsZ = [[-14, -14, None], autoTIMRP[0], ctrlArrayFingers[0], "rotateZ", ]

        spread_N10_IndexZ = [[-5, -15, None, None], autoTIMRP[1], ctrlArrayFingers[1], "rotateZ", ]
        spread_N10_MiddleZ = [[-2, -4, None, None], autoTIMRP[2], ctrlArrayFingers[2], "rotateZ", ]
        spread_N10_RingZ = [[2, 5, None, None], autoTIMRP[3], ctrlArrayFingers[3], "rotateZ", ]
        spread_N10_PinkZ = [[5, 17, None, None], autoTIMRP[4], ctrlArrayFingers[4], "rotateZ", ]

        spread_N10_Digits = [spread_N10_ThumbsX, spread_N10_ThumbsZ,
                             spread_N10_IndexZ,
                             spread_N10_MiddleZ,
                             spread_N10_RingZ,
                             spread_N10_PinkZ]
        self.setDigitVals(spread_N10_Digits, driverVal, ctrlFingers, fingerAttr[2])

    def fingerRelaxSetup(self, ctrlArrayFingers, autoTIMRP, ctrlFingers, fingerAttr, *args):

        driverVal = 0

        relax_P0_Digits = []

        for i in range(len(autoTIMRP)):
            if i == 0:
                pass
            else:
                relax_P0_Digits.append([[0, 0, 0, 0], autoTIMRP[i], None, "rotateX", ])
                # relax_P0_Digits.append(fingersToAddX)

        self.setDigitVals(relax_P0_Digits, driverVal, ctrlFingers, fingerAttr[3])

        driverVal = 10

        relax_P10_IndexZ = [[2, 10, 20, 25], autoTIMRP[1], None, "rotateX", ]
        relax_P10_MiddleZ = [[4, 15, 25, 30], autoTIMRP[2], None, "rotateX", ]
        relax_P10_RingZ = [[6, 20, 30, 35], autoTIMRP[3], None, "rotateX", ]
        relax_P10_PinkZ = [[8, 25, 35, 40], autoTIMRP[4], None, "rotateX", ]

        relax_P10_Digits = [relax_P10_IndexZ,
                            relax_P10_MiddleZ,
                            relax_P10_RingZ,
                            relax_P10_PinkZ]
        self.setDigitVals(relax_P10_Digits, driverVal, ctrlFingers, fingerAttr[3])

        driverVal = -10

        relax_N10_IndexZ = [[8, 30, 40, 45], autoTIMRP[1], None, "rotateX", ]
        relax_N10_MiddleZ = [[6, 25, 35, 40], autoTIMRP[2], None, "rotateX", ]
        relax_N10_RingZ = [[4, 15, 25, 30], autoTIMRP[3], None, "rotateX", ]
        relax_N10_PinkZ = [[2, 10, 20, 25], autoTIMRP[4], None, "rotateX", ]

        relax_N10_Digits = [relax_N10_IndexZ,
                            relax_N10_MiddleZ,
                            relax_N10_RingZ,
                            relax_N10_PinkZ]

        self.setDigitVals(relax_N10_Digits, driverVal, ctrlFingers, fingerAttr[3])

    def setDigitVals(self, digit_drvnvls_autos_digitCtrl, driverVal, ctrlDigits, digitAttr, *args):
        for i in range(len(digit_drvnvls_autos_digitCtrl)):
            for j in range(len(digit_drvnvls_autos_digitCtrl[i][0])):
                # skip if the value is a None
                if digit_drvnvls_autos_digitCtrl[i][0][j] is not None:
                    CRU.setDriverDrivenValues(ctrlDigits, digitAttr,
                                              digit_drvnvls_autos_digitCtrl[i][1][j],
                                              digit_drvnvls_autos_digitCtrl[i][-1],
                                              driverVal, digit_drvnvls_autos_digitCtrl[i][0][j])
                    # skip if the digit Control is not there
                    if digit_drvnvls_autos_digitCtrl[i][2] is not None:
                        CRU.setDriverDrivenValues(digit_drvnvls_autos_digitCtrl[i][2], digitAttr,
                                                  digit_drvnvls_autos_digitCtrl[i][1][j],
                                                  digit_drvnvls_autos_digitCtrl[i][-1],
                                                  driverVal, digit_drvnvls_autos_digitCtrl[i][0][j])

    def tgpCreateMirror(self, ctrlFingers, leftRightReplace, leftRightReplaceMirror):

        # when you make a duplicate, the order of the duplicated children will get reversed. This reverses the reverse.
        ctrlFingersMirrorWork = mc.duplicate(ctrlFingers, rc=True)
        ctrlFingersMirrorWork[1:] = ctrlFingersMirrorWork[-1:0:-1]

        ctrlFingersMirror = []

        offsetCtrlStuffMirror = []
        for i in range(len(ctrlFingersMirrorWork)):
            # switch the l/r,
            toRename = ctrlFingersMirrorWork[i].replace(leftRightReplace, leftRightReplaceMirror)[:-1]
            mc.rename(ctrlFingersMirrorWork[i], toRename)
            ctrlFingersMirror.append(toRename)
        ctrlFingersMirrorTop = ctrlFingersMirror[0]
        # takes the initial offset value, duplicates it, flips the values around, then freezes the transformation
        # translates everything into place
        mirrorTrans = mc.xform(ctrlFingersMirrorTop, q=True, ws=True, rotatePivot=True)
        mirrorRot = mc.xform(ctrlFingersMirrorTop, q=True, ws=True, rotation=True)
        mirrorTransX = mirrorTrans[0] * -1
        mirrorTransY = mirrorTrans[1]
        mirrorTransZ = mirrorTrans[2]
        mirrorRotX = mirrorRot[0] * 1
        mirrorRotY = mirrorRot[1] * -1
        mirrorRotZ = mirrorRot[2] * -1

        mirrorXScal = mc.getAttr("{0}.sx".format(ctrlFingersMirrorTop)) * -1

        # mirrors the values

        mc.xform(ctrlFingersMirrorTop, translation=(mirrorTransX, mirrorTransY, mirrorTransZ))
        mc.xform(ctrlFingersMirrorTop, scale=(mirrorXScal, 1, 1))
        mc.xform(ctrlFingersMirrorTop, rotation=(mirrorRotX, mirrorRotY, mirrorRotZ))

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
            mc.warning("No control selected!")
            return

        ctrlsArray = self.ctrlsArray

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

            # CRU.createLocatorToDelete()
            if not (CRU.checkLeftRight(isLeft, fingerRoot)):
                # if the values are not lined up properly, break out
                mc.warning("You are selecting the incorrect side for the fingers control")
                return

            if not (CRU.checkLeftRight(isLeft, ctrlPalm)):
                # if the values are not lined up properly, break out
                mc.warning("You are selecting the incorrect side for the palm control")
                return

            if mirrorRig:
                # we want to get the finger control before we add anything to it. When doing this programmatically, it's easier
                # make sure the children are not locked
                ctrlsArrayMirror, ctrlFingerNames = self.tgpCreateMirror(ctrlFingerNames, leftRightReplace,
                                                                         leftRightReplaceMirror)

            self.makeFingers(ctrlPalm, ctrlsArray, leftRight, colourTU)

            if mirrorRig:
                print("Mirroring")

                isLeftMirror = not isLeft

                ctrlPalmMirror = ctrlPalm.replace(leftRightReplace, leftRightReplaceMirror)

                self.makeFingers(ctrlPalmMirror, ctrlsArrayMirror, leftRightMirror, colourTUMirror)
