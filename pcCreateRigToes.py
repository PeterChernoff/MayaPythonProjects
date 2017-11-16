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
# This program assumes there are no toes in the original.
import pcCreateRigUtilities
from pcCreateRigUtilities import pcCreateRigUtilities as CRU

reload(pcCreateRigUtilities)


class pcCreateRigToes(UI):
    def __init__(self):


        self.window = "bcWindow"
        self.title = "pcRigToes"
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

        mc.text(l="Mirror Toes As Well?")
        # mc.setParent("..")
        mc.radioButtonGrp("selToesMirrorType_rbg", la2=["No", "Yes"], nrb=2, sl=2, cw2=[50, 50], )
        mc.text(l="")
        mc.setParent("..")
        mc.separator(st="in", h=20, w=500)

        mc.rowColumnLayout(nc=3, cw=[(1, 100), (2, 200), (3, 150)], cs=[1, 5], rs=[1, 3],
                           cal=([1, "left"], [2, "left"], [3, "left"],))
        mc.text(l="Initial Limb: ")
        mc.radioButtonGrp("selToesType_rbg", la2=["Left", "Right"], nrb=2, sl=1, cw2=[50, 50], )
        mc.setParent("..")
        mc.separator(st="in", h=20, w=500)

        # sources
        mc.rowColumnLayout(nc=2, cw=[(1, 100), (2, 370)], cs=[1, 5], rs=[1, 3])


        mc.text(bgc=(0.85, 0.65, 0.25), l="Toes Locator: ")
        mc.textFieldButtonGrp("locToesLoad_tf", cw=(1, 322), bl="  Load  ")
        mc.text(bgc=(0.85, 0.65, 0.25), l="Ball Joint: ")
        mc.textFieldButtonGrp("jntBallLoad_tf", cw=(1, 322), bl="  Load  ", tx="JNT_l_ball")

        mc.text(bgc=(0.85, 0.65, 0.25), l="Toes Control: ")
        mc.textFieldButtonGrp("ctrlToesLoad_tfbg", cw=(1, 322), bl="  Load  ", tx="CTRL_l_toes")

        mc.text(bgc=(0.85, 0.65, 0.25), l="Leg Group: ")
        mc.textFieldButtonGrp("grpLegLoad_tfbg", cw=(1, 322), bl="  Load  ", tx="GRP_rig_l_leg")


        mc.setParent("..")

        mc.separator(st="in", h=20, w=500)

        # load buttons
        #

        mc.textFieldButtonGrp("ctrlToesLoad_tfbg", e=True, bc=self.loadSrc1Btn)
        mc.textFieldButtonGrp("jntBallLoad_tf", e=True, bc=self.loadSrc2Btn)
        mc.textFieldButtonGrp("locToesLoad_tf", e=True, bc=self.loadSrc3Btn)
        mc.textFieldButtonGrp("grpLegLoad_tfbg", e=True, bc=self.loadSrc4Btn)

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
        self.ctrlsSel = self.tgpLoadTxBtn("ctrlToesLoad_tfbg", "nurbsCurve")
        print(self.ctrlsSel)

    def loadSrc2Btn(self):
        self.jntBallSel = self.loadJntBtn("jntBallLoad_tf")
        print(self.jntBallSel)

    def loadSrc3Btn(self):
        self.locToesSel = self.loadLocBtn("locToesLoad_tf")
        print(self.locToesSel)

    def loadSrc4Btn(self):
        self.grpLegSel = self.loadGrpBtn("grpLegLoad_tfbg")
        print(self.locToesSel)

    def loadJntBtn(self, loadBtn):
        self.selLoad = []
        # self.selLoad = mc.ls(sl=True, fl=True, type="nurbsCurve")
        self.selLoad = mc.ls(sl=True, fl=True, type="joint")

        if (len(self.selLoad) != 1):
            mc.warning("Select only the ball joint")
            return
        else:
            selName = self.selLoad[0]
            mc.textFieldButtonGrp(loadBtn, e=True, tx=selName)
            return selName

            # print(selName)
    def loadGrpBtn(self, loadBtn):
        self.selLoad = []
        # self.selLoad = mc.ls(sl=True, fl=True, type="nurbsCurve")
        self.selLoad = mc.ls(sl=True, fl=True, type="transform")

        if (len(self.selLoad) != 1):
            mc.warning("Select only the ball joint")
            return
        else:

            if CRU.checkObjectType(self.selLoad[0]) != "transform":
                mc.warning("The Control should be a group")
                return
            selName = self.selLoad[0]
            mc.textFieldButtonGrp(loadBtn, e=True, tx=selName)
            return selName

            # print(selName)

    def loadLocBtn(self, loadBtn):
        self.selLoad = []
        # self.selLoad = mc.ls(sl=True, fl=True, type="nurbsCurve")
        self.selLoad = mc.ls(sl=True, fl=True)

        if (len(self.selLoad) != 1):
            mc.warning("Select only the toes locator")
            return
        else:
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

    def getToes(self, locToes, *args):
        allToes = []
        ballLess = [x for x in locToes if "ball" not in x]

        indexOfToes = ["index", "middle", "ring", "pinky", "thumb"]

        for toe in indexOfToes:
            allToes.append([x for x in ballLess if toe in x])

        return allToes

    def createToeFKs(self, fkJnts, colourTU, isLeft, *args):

        fkJntOffsetCtrls = []
        for fkJnt in fkJnts:
            fkToeOffsetCtrls = []
            # we want to create FK controls for the toes except the end
            for i in range(len(fkJnt[:-1])):
                temp = fkJnt[i]
                if i == 0:
                    theSize = 1
                elif "thumb" in temp:
                    theSize = 2
                else:
                    theSize = 1.5
                fkToeOffsetCtrls.append(
                    CRU.createCTRLs(temp, size=theSize, ornt=True, colour=colourTU, orientVal=(0, 1, 0)))
                toeLength = mc.getAttr("{0}.ty".format(fkJnt[i + 1]))
                mc.select(fkToeOffsetCtrls[i][1] + ".cv[:]")
                if isLeft:
                    moveZ = -3
                else:
                    moveZ = 3
                if i == 0:
                    mc.move(0, toeLength * 0.9, moveZ, r=True, ls=True)
                else:
                    mc.move(0, toeLength * 0.5, 0, r=True, ls=True)
            fkJntOffsetCtrls.append(fkToeOffsetCtrls)

        # parents the toes fks under each other
        # print(fkJntOffsetCtrls)
        for i in range(len(fkJntOffsetCtrls)):
            for j in range(len(fkJntOffsetCtrls[i]) - 1):
                mc.parent(fkJntOffsetCtrls[i][j + 1][0], fkJntOffsetCtrls[i][j][1])

        return fkJntOffsetCtrls

    def makeToes(self, jntBall, locToes, ctrlToesNames, grpLegs, leftRight, colourTU, isLeft, *args):

        toesJnts = mc.listRelatives(locToes, ad=True, s=False, type="joint")
        toesJnts.reverse()



        # Create the toe controls

        print(toesJnts)

        fkJntOffsetCtrls = self.createToeFKs(toesJnts, colourTU, isLeft)
        return

        jntThumbs = [x for x in toesJnts if ("thumb" in x.lower()) and "JNT" in x]
        jntIndex = [x for x in toesJnts if ("index" in x.lower()) and "JNT" in x]
        jntMiddle = [x for x in toesJnts if ("middle" in x.lower()) and "JNT" in x]
        jntRing = [x for x in toesJnts if ("ring" in x.lower()) and "JNT" in x]
        jntPink = [x for x in toesJnts if ("pink" in x.lower()) and "JNT" in x]

        # TIMRP = Thumb, Index, Middle, Ring, Pinkie
        JNTTIMRP = [jntThumbs, jntIndex, jntMiddle, jntRing, jntPink]

        ctrlTIMRP = [ctrlThumb, ctrlIndex, ctrlMiddle, ctrlRing, ctrlPink]

        fingerAttr = ["curl", "scrunch", "spread"]
        footAttr = list(fingerAttr)

        footAttr.append("relax")
        valsMinMaxDef = [-10, 10, 0]

        # add the toes control attributes
        for i in range(len(footAttr)):
            mc.addAttr(ctrlToes, longName=footAttr[i], at="float", k=True, min=valsMinMaxDef[0],
                       max=valsMinMaxDef[1], dv=valsMinMaxDef[2])

        # add the toes control attributes for the individual toes
        for i in range(len(fingerAttr)):
            for j in range(len(ctrlTIMRP)):
                mc.addAttr(ctrlTIMRP[j], longName=fingerAttr[i], at="float", k=True, min=valsMinMaxDef[0],
                           max=valsMinMaxDef[1], dv=valsMinMaxDef[2])

        # creating the Toes Curl
        self.fingerCurlsSetup(ctrlArrayToes, autoTIMRP, ctrlToes, footAttr)

        # creating the Toes scrunch
        self.toescrunchSetup(ctrlArrayToes, autoTIMRP, ctrlToes, footAttr)

        # creating the Toes spread
        self.toespreadSetup(ctrlArrayToes, autoTIMRP, ctrlToes, footAttr)

        # creating the Toes relax
        self.fingerRelaxSetup(ctrlArrayToes, autoTIMRP, ctrlToes, footAttr)

        # Cleaning up
        self.toesCleanup(ctrlToes, jntBall, colourTU)

    def toesCleanup(self, ctrlToes, jntBall, colourTU, *args):

        mc.parent(ctrlToes, jntBall)

        checkList = mc.listRelatives(ctrlToes)
        for i in range(len(checkList)):
            if mc.objectType(checkList[i]) == "transform":
                CRU.lockHideCtrls(checkList[i], translate=True, rotate=True, scale=True, toHide=True, visible=True,
                                  toLock=False)
        mc.makeIdentity(ctrlToes, apply=True, translate=True, rotate=True, scale=True)

        # get the non-shape values
        lockValues = mc.listRelatives(ctrlToes, c=True, s=False, type="transform")
        lockValues.append(ctrlToes)
        print(lockValues)

        for i in range(len(lockValues)):
            CRU.lockHideCtrls(lockValues[i], translate=True, rotate=True, scale=True, visible=True)

            mc.setAttr('{0}.overrideEnabled'.format(lockValues[i]), 1)
            mc.setAttr("{0}.overrideColor".format(lockValues[i]), colourTU)

    def fingerCurlsSetup(self, ctrlArrayToes, autoTIMRP, ctrlToes, fingerAttr, *args):

        # we need to create the toes first
        return

        # set at 0 for curl and rotateX, and the thumb values
        driverVal = 0
        self.fingerCurls(ctrlArrayToes, autoTIMRP, ctrlToes, fingerAttr, driverVal, toesAttrArray=0,
                         thumbsAttrArrayDriven=0, )

        # self.fingerCurlsIndividual(ctrlArrayToes, autoTIMRP, fingerAttr, driverVal, toesCurlArray=0, thumbsCurlArrayDriven=0)

        # set at 10 for curl and rotateX, and the thumb values

        thumbCurlsXP10 = [10, 45, 70]
        thumbCurlsZP10 = [20, 0]

        curlsToes1XP10 = 5

        indexCurlP10 = 70
        indexCurlsP10 = [curlsToes1XP10, indexCurlP10, indexCurlP10, indexCurlP10]

        middleCurlP10 = 76
        middleCurlsP10 = [curlsToes1XP10, middleCurlP10, middleCurlP10, middleCurlP10]

        ringCurlP10 = 67
        ringCurlsP10 = [curlsToes1XP10, ringCurlP10, ringCurlP10, ringCurlP10]

        pinkCurlP10 = 67
        pinkCurlsP10 = [curlsToes1XP10, pinkCurlP10, pinkCurlP10, pinkCurlP10]
        toesCurlXP10 = [thumbCurlsXP10, indexCurlsP10, middleCurlsP10, ringCurlsP10, pinkCurlsP10]

        driverVal = 10
        self.fingerCurls(ctrlArrayToes, autoTIMRP, ctrlToes, fingerAttr, driverVal, toesCurlXP10,
                         thumbCurlsZP10, )
        # self.fingerCurlsIndividual(ctrlArrayToes, autoTIMRP, fingerAttr, driverVal, toesCurlXP10, thumbCurlsZP10)

        # set at -10 for curl and rotateX, and the thumb values

        toesCurlXN10 = []

        thumbCurlsXN10 = [-10, -15, -10]
        thumbCurlsZN10 = [-10, -10]

        toesCurlXN10.append(thumbCurlsXN10)
        # index middle
        curls_IMX1_N10 = -3
        # ring pinkie
        curls_RPX1_N10 = -4
        curlsRestN10 = -25

        indexCurlsN10 = [curls_IMX1_N10, curlsRestN10, curlsRestN10, curlsRestN10]

        middleCurlsN10 = [curls_IMX1_N10, curlsRestN10, curlsRestN10, curlsRestN10]

        ringCurlsN10 = [curls_RPX1_N10, curlsRestN10, curlsRestN10, curlsRestN10]

        pinkCurlsN10 = [curls_RPX1_N10, curlsRestN10, curlsRestN10, curlsRestN10]
        toesCurlXN10 = [thumbCurlsXN10, indexCurlsN10, middleCurlsN10, ringCurlsN10, pinkCurlsN10]

        driverVal = -10
        self.fingerCurls(ctrlArrayToes, autoTIMRP, ctrlToes, fingerAttr, driverVal, toesCurlXN10,
                         thumbCurlsZN10, )

    def fingerCurls(self, ctrlArrayToes, autoTIMRP, ctrlToes, fingerAttr, driverVal, toesAttrArray=0,
                    thumbsAttrArrayDriven=0, *args):
        # sets the value for the finger curls, and the individual finger curls
        fingerAttrVal = fingerAttr[0]

        for i in range(len(ctrlArrayToes)):
            for j in range(len(autoTIMRP[i])):
                # setDriverDrivenValues(driver, driverAttribute, driven, drivenAttribute, driverValue, drivenValue,):
                # set all the x values in curl to 0
                if isinstance(toesAttrArray, int):
                    valToUse = toesAttrArray

                else:

                    valToUse = toesAttrArray[i][j]
                CRU.setDriverDrivenValues(ctrlToes, fingerAttrVal, autoTIMRP[i][j], "rotateX", driverVal,
                                          valToUse)
                CRU.setDriverDrivenValues(ctrlArrayToes[i], fingerAttrVal, autoTIMRP[i][j], "rotateX",
                                          driverVal, valToUse)

        if isinstance(thumbsAttrArrayDriven, int):
            # if the value is an integer, we use the integer, if the value is a list, we use the list
            valToUse = [thumbsAttrArrayDriven, thumbsAttrArrayDriven]
        else:
            valToUse = [thumbsAttrArrayDriven[0], thumbsAttrArrayDriven[1]]

        CRU.setDriverDrivenValues(ctrlToes, fingerAttr[0], autoTIMRP[0][0], "rotateZ", driverVal, valToUse[0])
        CRU.setDriverDrivenValues(ctrlToes, fingerAttr[0], autoTIMRP[0][1], "rotateZ", driverVal, valToUse[1])

        CRU.setDriverDrivenValues(ctrlArrayToes[0], fingerAttrVal, autoTIMRP[0][0], "rotateZ", driverVal,
                                  valToUse[0])
        CRU.setDriverDrivenValues(ctrlArrayToes[0], fingerAttrVal, autoTIMRP[0][1], "rotateZ", driverVal,
                                  valToUse[1])

    def toescrunchSetup(self, ctrlArrayToes, autoTIMRP, ctrlToes, fingerAttr, *args):

        driverVal = 0

        self.toescrunch(ctrlArrayToes, autoTIMRP, ctrlToes, fingerAttr, driverVal, 0, 0)

        driverVal = 10
        scrunchToes_2XP10 = -50
        scrunchToes_3XP10 = 50
        scrunchToes_4XP10 = 50
        scrunchToes_234XP10 = [0, scrunchToes_2XP10, scrunchToes_3XP10, scrunchToes_4XP10]

        scrunchThumb_2XP10 = -30
        scrunchThumb_3XP10 = 80
        scrunchThumb_23XP10 = [0, scrunchThumb_2XP10, scrunchThumb_3XP10]

        self.toescrunch(ctrlArrayToes, autoTIMRP, ctrlToes, fingerAttr, driverVal, scrunchToes_234XP10,
                           scrunchThumb_23XP10)

        driverVal = -10
        scrunchToes_2XN10 = 15
        scrunchToes_3XN10 = -30
        scrunchToes_4XN10 = -40
        scrunchToes_234XN10 = [0, scrunchToes_2XN10, scrunchToes_3XN10, scrunchToes_4XN10]

        scrunchThumb_2XN10 = 20
        scrunchThumb_3XN10 = -40
        scrunchThumb_23XN10 = [0, scrunchThumb_2XN10, scrunchThumb_3XN10]
        self.toescrunch(ctrlArrayToes, autoTIMRP, ctrlToes, fingerAttr, driverVal, scrunchToes_234XN10,
                           scrunchThumb_23XN10)

    def toescrunch(self, ctrlArrayToes, autoTIMRP, ctrlToes, fingerAttr, driverVal, toesAttrArray=0,
                      thumbsAttrArrayDriven=0, *args):
        # sets the value for the finger scrunch, and the individual finger scrunches
        fingerAttrVal = fingerAttr[1]

        for i in range(len(ctrlArrayToes)):
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
                        # sets the thumb as a toes control
                        CRU.setDriverDrivenValues(ctrlToes, fingerAttrVal, autoTIMRP[i][j], "rotateX", driverVal,
                                                  valToUse)
                        # sets the thumb individual control
                        CRU.setDriverDrivenValues(ctrlArrayToes[i], fingerAttrVal, autoTIMRP[i][j], "rotateX",
                                                  driverVal, valToUse)
                    else:
                        # the rest are the other toes
                        if isinstance(toesAttrArray, int):
                            valToUse = toesAttrArray
                        else:
                            valToUse = toesAttrArray[j]
                        # sets the toes as a whole

                        CRU.setDriverDrivenValues(ctrlToes, fingerAttrVal, autoTIMRP[i][j], "rotateX", driverVal,
                                                  valToUse)
                        # sets the toes individually
                        CRU.setDriverDrivenValues(ctrlArrayToes[i], fingerAttrVal, autoTIMRP[i][j], "rotateX",
                                                  driverVal, valToUse)

    def toespreadSetup(self, ctrlArrayToes, autoTIMRP, ctrlToes, fingerAttr, *args):

        driverVal = 0

        self.toespread(ctrlArrayToes, autoTIMRP, ctrlToes, fingerAttr, driverVal, 0, 0)

        driverVal = 10

        spreadX_P10_ToeThumb = [-12, -12]
        spreadZ_P10_ToeThumb = [4, 4]
        spread_P10_ToeThumb = [spreadX_P10_ToeThumb, spreadZ_P10_ToeThumb]

        spreadZ_P10_ToeIndex = [2, 15]
        spreadZ_P10_ToeMiddle = [1, 7]
        spreadZ_P10_ToeRing = [-1, -8]
        spreadZ_P10_ToePink = [-2, -15]
        spreadZ_P10_Toes = [0, spreadZ_P10_ToeIndex, spreadZ_P10_ToeMiddle, spreadZ_P10_ToeRing, spreadZ_P10_ToePink]

        self.toespread(ctrlArrayToes, autoTIMRP, ctrlToes, fingerAttr, driverVal, spreadZ_P10_Toes,
                          spread_P10_ToeThumb)

        driverVal = -10
        spreadX_N10_ToeThumb = [12, 12]
        spreadZ_N10_ToeThumb = [-14, -14]
        spread_N10Thumb = [spreadX_N10_ToeThumb, spreadZ_N10_ToeThumb]

        spreadZ_N10_ToeIndex = [-5, -15]
        spreadZ_N10_ToeMiddle = [-2, -4]
        spreadZ_N10_ToeRing = [2, 5]
        spreadZ_N10_ToePink = [5, 17]
        spreadZ_N10_Toes = [0, spreadZ_N10_ToeIndex, spreadZ_N10_ToeMiddle, spreadZ_N10_ToeRing, spreadZ_N10_ToePink]
        self.toespread(ctrlArrayToes, autoTIMRP, ctrlToes, fingerAttr, driverVal, spreadZ_N10_Toes,
                          spread_N10Thumb)

    def toespread(self, ctrlArrayToes, autoTIMRP, ctrlToes, fingerAttr, driverVal, toesAttrArray=0,
                     thumbsAttrArrayDriven=0, *args):
        # sets the value for the finger scrunch, and the individual finger scrunches
        fingerAttrVal = fingerAttr[2]
        for i in range(len(ctrlArrayToes)):
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
                        # sets the thumb as a toes control
                        CRU.setDriverDrivenValues(ctrlToes, fingerAttrVal, autoTIMRP[i][j], "rotateX", driverVal,
                                                  valToUseX)
                        CRU.setDriverDrivenValues(ctrlToes, fingerAttrVal, autoTIMRP[i][j], "rotateZ", driverVal,
                                                  valToUseZ)

                        # sets the thumb individual control
                        CRU.setDriverDrivenValues(ctrlArrayToes[i], fingerAttrVal, autoTIMRP[i][j], "rotateX",
                                                  driverVal, valToUseX)
                        CRU.setDriverDrivenValues(ctrlArrayToes[i], fingerAttrVal, autoTIMRP[i][j], "rotateZ",
                                                  driverVal, valToUseZ)
                    else:

                        if isinstance(toesAttrArray, int):
                            valToUse = toesAttrArray
                        else:
                            valToUse = toesAttrArray[i][j]
                        # sets the thumb as a toes control
                        CRU.setDriverDrivenValues(ctrlToes, fingerAttrVal, autoTIMRP[i][j], "rotateZ", driverVal,
                                                  valToUse)

                        # sets the thumb individual control
                        CRU.setDriverDrivenValues(ctrlArrayToes[i], fingerAttrVal, autoTIMRP[i][j], "rotateZ",
                                                  driverVal, valToUse)

    def fingerRelaxSetup(self, ctrlArrayToes, autoTIMRP, ctrlToes, fingerAttr, *args):

        driverVal = 0

        self.fingerRelax(ctrlArrayToes, autoTIMRP, ctrlToes, fingerAttr, driverVal, 0, 0)

        driverVal = 10

        relaxX_P10_ToeIndex = [2, 10, 20, 25]
        relaxX_P10_ToeMiddle = [4, 15, 25, 30]
        relaxX_P10_ToeRing = [6, 20, 30, 35]
        relaxX_P10_ToePink = [8, 25, 35, 40]
        relaxX_P10_Toes = [0, relaxX_P10_ToeIndex, relaxX_P10_ToeMiddle, relaxX_P10_ToeRing, relaxX_P10_ToePink]

        self.fingerRelax(ctrlArrayToes, autoTIMRP, ctrlToes, fingerAttr, driverVal, relaxX_P10_Toes)

        driverVal = -10

        relaxX_N10_ToeIndex = [8, 30, 40, 45]
        relaxX_N10_ToeMiddle = [6, 25, 35, 40]
        relaxX_N10_ToeRing = [4, 15, 25, 30]
        relaxX_N10_ToePink = [2, 10, 20, 25]
        relaxX_N10_Toes = [0, relaxX_N10_ToeIndex, relaxX_N10_ToeMiddle, relaxX_N10_ToeRing, relaxX_N10_ToePink]
        self.fingerRelax(ctrlArrayToes, autoTIMRP, ctrlToes, fingerAttr, driverVal, relaxX_N10_Toes)

    def fingerRelax(self, ctrlArrayToes, autoTIMRP, ctrlToes, fingerAttr, driverVal, toesAttrArray=0, *args):
        # sets the value for the finger scrunch, and the individual finger scrunches
        fingerAttrVal = fingerAttr[3]
        for i in range(len(ctrlArrayToes)):
            # skip the thumb
            if i != 0:
                for j in range(len(autoTIMRP[i])):
                    # setDriverDrivenValues(driver, driverAttribute, driven, drivenAttribute, driverValue, drivenValue,):
                    # set all the x values in curl to 0
                    # we skip the thumb
                    if isinstance(toesAttrArray, int):
                        valToUse = toesAttrArray
                    else:
                        valToUse = toesAttrArray[i][j]
                    # sets the toes as a whole
                    # we don't work with the toes individually
                    CRU.setDriverDrivenValues(ctrlToes, fingerAttrVal, autoTIMRP[i][j], "rotateX", driverVal,
                                              valToUse)

    def tgpCreateMirror(self, locToes, leftRightReplace, leftRightReplaceMirror):
        print("I got here mirror")
        locToesMirrorWork = mc.duplicate(locToes, rc=True)

        locToesMirror = []

        for i in range(len(locToesMirrorWork)):
            # switch the l/r,
            print("--------")
            print(locToesMirrorWork[i])
            toRename = locToesMirrorWork[i].replace(leftRightReplace, leftRightReplaceMirror)[:-1]
            print(toRename)
            mc.rename(locToesMirrorWork[i], toRename)
            locToesMirror.append(toRename)
        locToesMirrorTop = locToesMirror[0]
        # takes the initial offset value, duplicates it, flips the values around, then freezes the transformation
        # translates everything into place
        mirrorTrans = mc.xform(locToesMirrorTop, q=True, ws=True, rotatePivot=True)
        mirrorRot = mc.xform(locToesMirrorTop, q=True, ws=True, rotation=True)
        print("MirrorTrans = {0}".format(mirrorTrans))
        print("MirrorAxis = {0}".format(mirrorRot))
        mirrorTransX = mirrorTrans[0] * -1
        mirrorTransY = mirrorTrans[1]
        mirrorTransZ = mirrorTrans[2]
        mirrorRotX = mirrorRot[0] * 1
        mirrorRotY = mirrorRot[1] * -1
        mirrorRotZ = mirrorRot[2] * -1

        mirrorXScal = mc.getAttr("{0}.sx".format(locToesMirrorTop)) * -1
        print(mirrorTrans)
        print(mirrorXScal)

        # mirrors the values
        mc.xform(locToesMirrorTop, translation=(mirrorTransX, mirrorTransY, mirrorTransZ))
        mc.xform(locToesMirrorTop, scale=( mirrorXScal, 1, 1) )
        mc.xform(locToesMirrorTop, rotation = (mirrorRotX, mirrorRotY, mirrorRotZ))

        # mc.scale(-1, ctrlToesMirrorTop, x=True, pivot=(0,0,0), a=True)
        mc.makeIdentity(locToesMirrorTop, apply=True, translate=True, scale=True)

        return locToesMirrorTop

    def tgpMakeBC(self, *args):

        checkSelLeft = mc.radioButtonGrp("selToesType_rbg", q=True, select=True)
        mirrorSel = mc.radioButtonGrp("selToesMirrorType_rbg", q=True, select=True)
        ctrlToesNames = mc.textFieldButtonGrp("ctrlToesLoad_tfbg", q=True, text=True)
        locToes = mc.textFieldButtonGrp("locToesLoad_tf", q=True, text=True)
        grpLegs = mc.textFieldButtonGrp("grpLegLoad_tfbg", q=True, text=True)
        
        jntBall = mc.textFieldButtonGrp("jntBallLoad_tf", q=True, text=True)



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

        checkList = locToes
        # note: the isCopy is not applicable due to the differences between the leg and arm joint setup.
        # However, editing them out is too much hassle,  it's easier just to leave them both false
        if ((checkList[0] == "")):
            mc.warning("You are missing a selection!")
            return
        else:
            if not (CRU.checkLeftRight(isLeft, locToes)):
                # if the values are not lined up properly, break out
                mc.warning("You are selecting the incorrect side")
                return

            CRU.createLocatorToDelete()

            print(locToes)


            if mirrorRig:
                # we want to get the finger control before we add anything to it. When doing this programmatically, it's easier
                # make sure the children are not locked
                locToesMirror = self.tgpCreateMirror(locToes, leftRightReplace,
                                                                         leftRightReplaceMirror)
                jntBallMirror = jntBall.replace(leftRightReplace,leftRightReplaceMirror )
                ctrlToesNamesMirror = ctrlToesNames.replace(leftRightReplace,leftRightReplaceMirror )
                grpLegs = grpLegs.replace(leftRightReplace, leftRightReplaceMirror)


            self.makeToes(jntBall, locToes, ctrlToesNames, grpLegs, leftRight, colourTU, isLeft)

            print(mirrorRig)
            if mirrorRig:
                print("I got here!")

                isLeftMirror = not isLeft

                return

                print(ctrlsArray)

                #self.makeToes(jntBallMirror, locToesMirror, ctrlToesNamesMirror, grpLegsMirror, leftRightMirror, colourTUMirror, isLeftMirror)
