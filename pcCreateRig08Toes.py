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
        self.winSize = (500, 375)

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

        mc.text(bgc=(0.85, 0.65, 0.25), l="Master Toes Joint: ")
        mc.textFieldButtonGrp("jntToesLoad_tf", cw=(1, 322), bl="  Load  ")
        mc.text(bgc=(0.85, 0.65, 0.25), l="Ball Joint: ")
        mc.textFieldButtonGrp("jntBallLoad_tf", cw=(1, 322), bl="  Load  ", tx="JNT_l_ball")
        mc.text(bgc=(0.85, 0.65, 0.25), l="AnkleTwist Joint: ")
        mc.textFieldButtonGrp("jntAnkleTwistLoad_tf", cw=(1, 322), bl="  Load  ", tx="JNT_l_ankleTwist")

        mc.text(bgc=(0.85, 0.65, 0.25), l="Toes Control: ")
        mc.textFieldButtonGrp("ctrlToesLoad_tfbg", cw=(1, 322), bl="  Load  ", tx="CTRL_l_toes")

        mc.text(bgc=(0.85, 0.65, 0.25), l="Leg Group: ")
        mc.textFieldButtonGrp("grpLegLoad_tfbg", cw=(1, 322), bl="  Load  ", tx="GRP_rig_l_leg")

        mc.setParent("..")

        mc.separator(st="in", h=20, w=500)

        mc.rowColumnLayout(nc=2, cw=[(1, 100), (2, 370)], cs=[1, 5], rs=[1, 3])
        mc.checkBox("selGeo_cb", l="Affect Geometry", en=True, v=True)

        mc.setParent("..")

        mc.separator(st="in", h=20, w=500)

        # load buttons
        #

        mc.textFieldButtonGrp("ctrlToesLoad_tfbg", e=True, bc=self.loadSrc1Btn)
        mc.textFieldButtonGrp("jntBallLoad_tf", e=True, bc=self.loadSrc2Btn)
        mc.textFieldButtonGrp("jntAnkleTwistLoad_tf", e=True, bc=self.loadSrc3Btn)
        mc.textFieldButtonGrp("jntToesLoad_tf", e=True, bc=self.loadSrc4Btn)
        mc.textFieldButtonGrp("grpLegLoad_tfbg", e=True, bc=self.loadSrc5Btn)

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

    def loadSrc2Btn(self):
        self.jntBallSel = self.loadJntBtn("jntBallLoad_tf", "ball")

    def loadSrc3Btn(self):
        self.jntAnkleTwistSel = self.loadJntBtn("jntAnkleTwistLoad_tf", "ankle twist")

    def loadSrc4Btn(self):
        self.jntMasterToesSel = self.loadJntBtn("jntToesLoad_tf", "master toes")

    def loadSrc5Btn(self):
        self.grpLegSel = self.loadGrpBtn("grpLegLoad_tfbg")

    def loadJntBtn(self, loadBtn, jntSel):
        self.selLoad = []
        # self.selLoad = mc.ls(sl=True, fl=True, type="nurbsCurve")
        self.selLoad = mc.ls(sl=True, fl=True, type="joint")

        if (len(self.selLoad) != 1):
            mc.warning("Select only the {0} joint".format(jntSel))
            return
        else:
            selName = self.selLoad[0]
            mc.textFieldButtonGrp(loadBtn, e=True, tx=selName)
            return selName

    def loadGrpBtn(self, loadBtn):
        self.selLoad = []
        # self.selLoad = mc.ls(sl=True, fl=True, type="nurbsCurve")
        self.selLoad = mc.ls(sl=True, fl=True, type="transform")

        if (len(self.selLoad) != 1):
            mc.warning("Select only the leg group")
            return
        else:

            if CRU.checkObjectType(self.selLoad[0]) != "transform":
                mc.warning("The Control should be a group")
                return
            selName = self.selLoad[0]
            mc.textFieldButtonGrp(loadBtn, e=True, tx=selName)
            return selName


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
            ctrlsArraySorted = []
            # sort the array
            for i in range(len(self.ctrlsArray)):
                sels = mc.listRelatives(self.ctrlsArray[i], c=True, s=True)
                if myType in mc.objectType(sels) or myType == mc.objectType(sels):
                    ctrlsArraySorted.append(self.ctrlsArray[i])

            self.ctrlsRoot = self.selLoad[0]
            self.ctrlsArray = ctrlsArraySorted

        return self.ctrlsArray

    def getToes(self, jntMasterToes, *args):
        allToes = []
        ballLess = [x for x in jntMasterToes if "ball" not in x]

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
                    theSize = .95
                elif "thumb" in temp:
                    theSize = 2
                elif "pink" in temp:
                    theSize = .85
                else:
                    theSize = 1.25
                fkToeOffsetCtrls.append(
                    CRU.createCTRLs(temp, size=theSize, ornt=True, colour=colourTU, orientVal=(0, 1, 0)))
                toeLength = mc.getAttr("{0}.ty".format(fkJnt[i + 1]))

                mc.select(fkToeOffsetCtrls[i][1] + ".cv[:]")
                if isLeft:
                    moveZ = -3
                else:
                    moveZ = 3
                if i == 0:
                    mc.move(0, 0, moveZ, r=True, ls=True)
                else:
                    mc.move(0, toeLength * 0.5, 0, r=True, ls=True)
            fkJntOffsetCtrls.append(fkToeOffsetCtrls)

        # parents the toes fks under each other
        # print(fkJntOffsetCtrls)
        for i in range(len(fkJntOffsetCtrls)):
            for j in range(len(fkJntOffsetCtrls[i]) - 1):
                mc.parent(fkJntOffsetCtrls[i][j + 1][0], fkJntOffsetCtrls[i][j][1])

        return fkJntOffsetCtrls

    def parentToes(self, jntBall, jntMasterToes, fkJntOffsetCtrls, leftRight, *args):
        # this assumes that the foot is already set up in the right place
        # mc.parent(mc.listRelatives(jntMasterToes, c=True), jntBall)
        theParent = None
        try:
            theParent = mc.listRelatives(jntMasterToes, p=True)[0]
        except:
            mc.warning("The Master Toes joint is already parented")
        if theParent is None:
            mc.parent(jntMasterToes, jntBall)

        # print(fkJntOffsetCtrls)
        grpCtrlFoot = mc.group(n="GRP_CTRL_{0}toes".format(leftRight), w=True, em=True)
        # parent constrain the initial toe offsets to the ball joint
        for i in range(len(fkJntOffsetCtrls)):
            # print(fkJntOffsetCtrls[i][0])
            mc.parentConstraint(jntBall, fkJntOffsetCtrls[i][0][0], mo=True)
            mc.parent(fkJntOffsetCtrls[i][0][0], grpCtrlFoot)

        return grpCtrlFoot

    def makeToes(self, jntBall, jntMasterToes, ctrlToes, grpLegs, jntAnkleTwist, leftRight, colourTU, isLeft, *args):

        toesJnts = mc.listRelatives(jntMasterToes, ad=True, s=False, type="joint")
        toesJnts.reverse()

        # Create the toe controls

        # TIMRP = Thumb, Index, Middle, Ring, Pinkie
        jntThumb = [x for x in toesJnts if ("thumb" in x.lower()) and "JNT" in x]
        jntIndex = [x for x in toesJnts if ("index" in x.lower()) and "JNT" in x]
        jntMiddle = [x for x in toesJnts if ("middle" in x.lower()) and "JNT" in x]
        jntRing = [x for x in toesJnts if ("ring" in x.lower()) and "JNT" in x]
        jntPink = [x for x in toesJnts if ("pink" in x.lower()) and "JNT" in x]
        JNTTIMRP = [jntThumb, jntIndex, jntMiddle, jntRing, jntPink]

        fkJntOffsetCtrls = self.createToeFKs(JNTTIMRP, colourTU, isLeft)

        # Organize the toes
        grpCtrlFoot = self.parentToes(jntBall, jntMasterToes, fkJntOffsetCtrls, leftRight)
        toesAutoCtrlSetup = mc.listRelatives(grpCtrlFoot, ad=True, s=False, type="transform")

        toesAutoCtrlSetup.reverse()

        ctrlToesKids = mc.listRelatives(ctrlToes, c=True, type="transform")
        ctrlArrayToes = [x for x in ctrlToesKids if ("toes" not in x.lower())]

        ctrlThumb = [x for x in ctrlToesKids if ("thumb" in x.lower())][0]
        ctrlIndex = [x for x in ctrlToesKids if ("index" in x.lower())][0]
        ctrlMiddle = [x for x in ctrlToesKids if ("middle" in x.lower())][0]
        ctrlRing = [x for x in ctrlToesKids if ("ring" in x.lower())][0]
        ctrlPink = [x for x in ctrlToesKids if ("pink" in x.lower())][0]

        ctrlTIMRP = [ctrlThumb, ctrlIndex, ctrlMiddle, ctrlRing, ctrlPink]

        autoThumb = [x for x in toesAutoCtrlSetup if ("thumb" in x.lower()) and "AUTO" in x]
        autoIndex = [x for x in toesAutoCtrlSetup if ("index" in x.lower()) and "AUTO" in x]
        autoMiddle = [x for x in toesAutoCtrlSetup if ("middle" in x.lower()) and "AUTO" in x]
        autoRing = [x for x in toesAutoCtrlSetup if ("ring" in x.lower()) and "AUTO" in x]
        autoPink = [x for x in toesAutoCtrlSetup if ("pink" in x.lower()) and "AUTO" in x]

        autoTIMRP = [autoThumb, autoIndex, autoMiddle, autoRing, autoPink]

        # print("bbbbbbb {0}".format(autoTIMRP))

        toeAttr = ["curl", "scrunch", "spread"]
        footAttr = list(toeAttr)

        footAttr.append("relax")
        valsMinMaxDef = [-10, 10, 0]

        # add the toes control attributes
        for i in range(len(footAttr)):
            mc.addAttr(ctrlToes, longName=footAttr[i], at="float", k=True, min=valsMinMaxDef[0],
                       max=valsMinMaxDef[1], dv=valsMinMaxDef[2])

        # add the toes control attributes for the individual toes
        for i in range(len(toeAttr)):
            for j in range(len(ctrlTIMRP)):
                mc.addAttr(ctrlTIMRP[j], longName=toeAttr[i], at="float", k=True, min=valsMinMaxDef[0],
                           max=valsMinMaxDef[1], dv=valsMinMaxDef[2])

        # creating the Toes Curl
        self.toeCurlsSetup(ctrlArrayToes, autoTIMRP, ctrlToes, footAttr)

        # creating the Toes scrunch
        self.toeScrunchSetup(ctrlArrayToes, autoTIMRP, ctrlToes, footAttr)

        # creating the Toes spread
        self.toeSpreadSetup(ctrlArrayToes, autoTIMRP, ctrlToes, footAttr)

        # creating the Toes relax
        self.toeRelaxSetup(ctrlArrayToes, autoTIMRP, ctrlToes, footAttr)

        # Cleaning up
        self.toesCleanup(ctrlToes, jntMasterToes, jntAnkleTwist, fkJntOffsetCtrls, grpCtrlFoot, grpLegs, colourTU)

        CRU.tgpSetGeo(toesJnts, setLayer=True)

    def toesCleanup(self, ctrlToes, jntMasterToes, jntAnkleTwist, fkJntOffsetCtrls, grpCtrlFoot, grpLegs, colourTU,
                    *args):

        mc.parent(ctrlToes, jntAnkleTwist)

        checkList = mc.listRelatives(ctrlToes)
        for i in range(len(checkList)):
            if mc.objectType(checkList[i]) == "transform":
                CRU.lockHideCtrls(checkList[i], translate=True, rotate=True, scale=True, toHide=True, visible=True,
                                  toLock=False)
        mc.makeIdentity(ctrlToes, apply=True, translate=True, rotate=True, scale=True)

        # get the non-shape values
        lockValues = mc.listRelatives(ctrlToes, c=True, s=False, type="transform")
        lockValues.append(ctrlToes)
        # print(lockValues)

        for i in range(len(lockValues)):
            CRU.lockHideCtrls(lockValues[i], translate=True, rotate=True, scale=True, visible=True)

            mc.setAttr('{0}.overrideEnabled'.format(lockValues[i]), 1)
            mc.setAttr("{0}.overrideColor".format(lockValues[i]), colourTU)

        # toeGrpName = "GRP_CTRL_{0}toes".format(leftRight)
        # toeGrp = mc.group(name=toeGrpName, w=True)
        for i in range(len(fkJntOffsetCtrls)):
            for j in range(len(fkJntOffsetCtrls[i])):
                CRU.lockHideCtrls(fkJntOffsetCtrls[i][j][1], translate=True, scale=True, visible=True)

                # print(fkJntOffsetCtrls[i][0][0])

        mc.parent(grpCtrlFoot, grpLegs)
        CRU.layerEdit(jntMasterToes, bndLayer=True, noRecurse=True)



    def toeCurlsSetup(self, ctrlArrayToes, autoTIMRP, ctrlToes, toeAttr, *args):

        # we need to create the toes first

        # set at 0 for curl and rotateX, and the thumb values
        driverVal = 0
        curl_P0_Digits = []
        for i in range(len(autoTIMRP)):
            if i == 0:
                toesToAddX = [[0, 0, 0], autoTIMRP[i], ctrlArrayToes[i], "rotateX", ]
            else:
                toesToAddX = [[0, 0, 0, 0], autoTIMRP[i], ctrlArrayToes[i], "rotateX", ]
            curl_P0_Digits.append(toesToAddX)

        self.setDigitVals(curl_P0_Digits, driverVal, ctrlToes, toeAttr[0])

        # set at 10 for curl and rotateX, and the thumb values
        driverVal = 10
        curl_P10_Other = [5, 55, 55, 55]
        curl_P10_ThumbsX = [[10, 45, 70], autoTIMRP[0], ctrlArrayToes[0], "rotateX", ]
        curl_P10_IndexX = [curl_P10_Other, autoTIMRP[1], ctrlArrayToes[1], "rotateX", ]
        curl_P10_MiddleX = [curl_P10_Other, autoTIMRP[2], ctrlArrayToes[2], "rotateX", ]
        curl_P10_RingX = [curl_P10_Other, autoTIMRP[3], ctrlArrayToes[3], "rotateX", ]
        curl_P10_PinkX = [curl_P10_Other, autoTIMRP[4], ctrlArrayToes[4], "rotateX", ]

        curl_P10_Digits = [curl_P10_ThumbsX, curl_P10_IndexX, curl_P10_MiddleX, curl_P10_RingX, curl_P10_PinkX]

        self.setDigitVals(curl_P10_Digits, driverVal, ctrlToes, toeAttr[0])

        # set at -10 for curl and rotateX, and the thumb values
        driverVal = -10
        curl_P10_DigitsIM = [-3, -25, -25, -25]
        curl_P10_DigitsRP = [-3, -25, -25, -25]

        curl_N10_ThumbsX = [[-10, -15, -10], autoTIMRP[0], ctrlArrayToes[0], "rotateX", ]
        curl_N10_IndexX = [curl_P10_DigitsIM, autoTIMRP[1], ctrlArrayToes[1], "rotateX", ]
        curl_N10_MiddleX = [curl_P10_DigitsIM, autoTIMRP[2], ctrlArrayToes[2], "rotateX", ]
        curl_N10_RingX = [curl_P10_DigitsRP, autoTIMRP[3], ctrlArrayToes[3], "rotateX", ]
        curl_N10_PinkX = [curl_P10_DigitsRP, autoTIMRP[4], ctrlArrayToes[4], "rotateX", ]

        curl_N10_Digits = [curl_N10_ThumbsX, curl_N10_IndexX, curl_N10_MiddleX, curl_N10_RingX, curl_N10_PinkX]

        self.setDigitVals(curl_N10_Digits, driverVal, ctrlToes, toeAttr[0])

    def toeScrunchSetup(self, ctrlArrayToes, autoTIMRP, ctrlToes, toeAttr, *args):

        driverVal = 0

        scrunch_P0_Digits = []
        for i in range(len(autoTIMRP)):
            if i == 0:
                toesToAddX = [[None, 0, 0], autoTIMRP[i], ctrlArrayToes[i], "rotateX", ]
            else:
                toesToAddX = [[None, 0, 0, 0], autoTIMRP[i], ctrlArrayToes[i], "rotateX", ]
            scrunch_P0_Digits.append(toesToAddX)

        self.setDigitVals(scrunch_P0_Digits, driverVal, ctrlToes, toeAttr[1])

        driverVal = 10
        scrunch_P10_Other = [None, -50, 50, 50]
        scrunch_P10_ThumbsX = [[None, -50, 70], autoTIMRP[0], ctrlArrayToes[0], "rotateX", ]
        scrunch_P10_IndexX = [scrunch_P10_Other, autoTIMRP[1], ctrlArrayToes[1], "rotateX", ]
        scrunch_P10_MiddleX = [scrunch_P10_Other, autoTIMRP[2], ctrlArrayToes[2], "rotateX", ]
        scrunch_P10_RingX = [scrunch_P10_Other, autoTIMRP[3], ctrlArrayToes[3], "rotateX", ]
        scrunch_P10_PinkX = [scrunch_P10_Other, autoTIMRP[4], ctrlArrayToes[4], "rotateX", ]

        scrunch_P10_Digits = [scrunch_P10_ThumbsX, scrunch_P10_IndexX, scrunch_P10_MiddleX, scrunch_P10_RingX,
                              scrunch_P10_PinkX]
        self.setDigitVals(scrunch_P10_Digits, driverVal, ctrlToes, toeAttr[1])

        driverVal = -10
        scrunch_N10_Other = [None, 15, -30, -40]

        scrunch_N10_ThumbsX = [[None, 20, -40], autoTIMRP[0], ctrlArrayToes[0], "rotateX", ]
        scrunch_N10_IndexX = [scrunch_N10_Other, autoTIMRP[1], ctrlArrayToes[1], "rotateX", ]
        scrunch_N10_MiddleX = [scrunch_N10_Other, autoTIMRP[2], ctrlArrayToes[2], "rotateX", ]
        scrunch_N10_RingX = [scrunch_N10_Other, autoTIMRP[3], ctrlArrayToes[3], "rotateX", ]
        scrunch_N10_PinkX = [scrunch_N10_Other, autoTIMRP[4], ctrlArrayToes[4], "rotateX", ]

        scrunch_N10_Digits = [scrunch_N10_ThumbsX, scrunch_N10_IndexX, scrunch_N10_MiddleX, scrunch_N10_RingX,
                              scrunch_N10_PinkX]
        self.setDigitVals(scrunch_N10_Digits, driverVal, ctrlToes, toeAttr[1])

    def toeSpreadSetup(self, ctrlArrayToes, autoTIMRP, ctrlToes, toeAttr, *args):

        driverVal = 0

        spread_P0_DigitThumbsX = [[0, 0, None], autoTIMRP[0], ctrlArrayToes[0], "rotateZ", ]

        spread_P0_Digits = []
        for i in range(len(autoTIMRP)):
            if i == 0:
                spread_P0_Digits.append(spread_P0_DigitThumbsX)
            else:
                toesToAddX = [[0, 0, None, None], autoTIMRP[i], ctrlArrayToes[i], "rotateX", ]
                toesToAddZ = [[0, 0, None, None], autoTIMRP[i], ctrlArrayToes[i], "rotateZ", ]

                spread_P0_Digits.append(toesToAddX)
                spread_P0_Digits.append(toesToAddZ)

        self.setDigitVals(spread_P0_Digits, driverVal, ctrlToes, toeAttr[2])

        driverVal = 10
        spread_P10_ThumbsZ = [[4, 4, None], autoTIMRP[0], ctrlArrayToes[0], "rotateZ", ]

        spread_P10_IndexX = [[-15, -22.5, None, None], autoTIMRP[1], ctrlArrayToes[1], "rotateX", ]
        spread_P10_IndexZ = [[-5, -15, None, None], autoTIMRP[1], ctrlArrayToes[1], "rotateZ", ]

        spread_P10_MiddleX = [[-10, -20, None, None], autoTIMRP[2], ctrlArrayToes[2], "rotateX", ]
        spread_P10_MiddleZ = [[-3, -15, None, None], autoTIMRP[2], ctrlArrayToes[2], "rotateZ", ]

        spread_P10_RingX = [[-7, -15, None, None], autoTIMRP[3], ctrlArrayToes[3], "rotateX", ]
        spread_P10_RingZ = [[-1, -15, None, None], autoTIMRP[3], ctrlArrayToes[3], "rotateZ", ]

        spread_P10_PinkX = [[-5, -7.5, None, None], autoTIMRP[4], ctrlArrayToes[4], "rotateX", ]
        spread_P10_PinkZ = [[-5, -25, None, None], autoTIMRP[4], ctrlArrayToes[4], "rotateZ", ]

        spread_P10_Digits = [spread_P10_ThumbsZ,
                             spread_P10_IndexZ, spread_P10_IndexX,
                             spread_P10_MiddleZ, spread_P10_MiddleX,
                             spread_P10_RingZ, spread_P10_RingX,
                             spread_P10_PinkZ, spread_P10_PinkX, ]

        self.setDigitVals(spread_P10_Digits, driverVal, ctrlToes, toeAttr[2])

        driverVal = -10
        spread_N10_ThumbsZ = [[-5, -10, None], autoTIMRP[0], ctrlArrayToes[0], "rotateZ", ]

        spread_N10_IndexX = [[0, 0, None, None], autoTIMRP[1], ctrlArrayToes[1], "rotateX", ]
        spread_N10_IndexZ = [[2, 2, None, None], autoTIMRP[1], ctrlArrayToes[1], "rotateZ", ]

        spread_N10_MiddleX = [[0, 0, None, None], autoTIMRP[2], ctrlArrayToes[2], "rotateX", ]
        spread_N10_MiddleZ = [[4, 9, None, None], autoTIMRP[2], ctrlArrayToes[2], "rotateZ", ]

        spread_N10_RingX = [[0, 0, None, None], autoTIMRP[3], ctrlArrayToes[3], "rotateX", ]
        spread_N10_RingZ = [[4, 11, None, None], autoTIMRP[3], ctrlArrayToes[3], "rotateZ", ]

        spread_N10_PinkX = [[0, 0, None, None], autoTIMRP[4], ctrlArrayToes[4], "rotateX", ]
        spread_N10_PinkZ = [[5, 17, None, None], autoTIMRP[4], ctrlArrayToes[4], "rotateZ", ]

        spread_N10_Digits = [spread_N10_ThumbsZ,
                             spread_N10_IndexZ, spread_N10_IndexX,
                             spread_N10_MiddleZ, spread_N10_MiddleX,
                             spread_N10_RingZ, spread_N10_RingX,
                             spread_N10_PinkZ, spread_N10_PinkX]

        self.setDigitVals(spread_N10_Digits, driverVal, ctrlToes, toeAttr[2])

    def toeRelaxSetup(self, ctrlArrayToes, autoTIMRP, ctrlToes, toeAttr, *args):

        driverVal = 0

        relax_P0_Digits = []
        for i in range(len(autoTIMRP)):
            if i == 0:
                toesToAddX = [[0, 0, 0], autoTIMRP[i], None, "rotateX", ]
            else:
                toesToAddX = [[0, 0, 0, 0], autoTIMRP[i], None, "rotateX", ]
            relax_P0_Digits.append(toesToAddX)

        self.setDigitVals(relax_P0_Digits, driverVal, ctrlToes, toeAttr[3])

        driverVal = 10
        relax_P10_ThumbsX = [[1, 5, 10], autoTIMRP[0], None, "rotateX", ]
        relax_P10_IndexX = [[2, 7.5, 12.5, 17.5], autoTIMRP[1], None, "rotateX", ]
        relax_P10_MiddleX = [[4, 10, 15, 20], autoTIMRP[2], None, "rotateX", ]
        relax_P10_RingX = [[6, 12.5, 17.5, 22.5], autoTIMRP[3], None, "rotateX", ]
        relax_P10_PinkX = [[8, 15, 20, 25], autoTIMRP[4], None, "rotateX", ]

        relax_P10_Digits = [relax_P10_ThumbsX,
                            relax_P10_IndexX,
                            relax_P10_MiddleX,
                            relax_P10_RingX,
                            relax_P10_PinkX]

        self.setDigitVals(relax_P10_Digits, driverVal, ctrlToes, toeAttr[3])

        driverVal = -10

        relax_N10_ThumbsX = [[10, 20, 25], autoTIMRP[0], None, "rotateX", ]
        relax_N10_IndexX = [[8, 17.5, 22.5, 27.5], autoTIMRP[1], None, "rotateX", ]
        relax_N10_MiddleX = [[6, 15, 20, 25], autoTIMRP[2], None, "rotateX", ]
        relax_N10_RingX = [[4, 12.5, 17.5, 22.5], autoTIMRP[3], None, "rotateX", ]
        relax_N10_PinkX = [[2, 10, 15, 20], autoTIMRP[4], None, "rotateX", ]

        relax_N10_Digits = [relax_N10_ThumbsX, relax_N10_IndexX, relax_N10_MiddleX, relax_N10_RingX,
                            relax_N10_PinkX]

        self.setDigitVals(relax_N10_Digits, driverVal, ctrlToes, toeAttr[3])

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

    def tgpCreateMirrorToes(self, jntMasterToes, leftRightReplace, leftRightReplaceMirror):
        # just reflects it
        parentOfJnt = None
        parentOfJntMirror = None
        try:
            # in case the joint is already parented
            parentOfJnt = mc.listRelatives(jntMasterToes, p=True)[0]
            parentOfJntMirror = parentOfJnt.replace(leftRightReplace, leftRightReplaceMirror)
        except:
            mc.warning("Master Toes joint already at world")

        if parentOfJnt is not None:
            # if there is a parent, place at world
            mc.parent(jntMasterToes, w=True)

        jntMasterToesMirrorWork = mc.mirrorJoint(jntMasterToes, mirrorYZ=True, mirrorBehavior=True,
                                                 searchReplace=[leftRightReplace, leftRightReplaceMirror])
        jntMasterToesMirrorTop = jntMasterToesMirrorWork[0]

        if parentOfJnt is not None:
            # return to the top
            mc.parent(jntMasterToes, parentOfJnt)
            mc.parent(jntMasterToesMirrorTop, parentOfJntMirror)

        return jntMasterToesMirrorTop

    def tgpCreateMirrorCtrl(self, ctrlToes, leftRightReplace, leftRightReplaceMirror):
        ctrlToesMirrorWork = mc.duplicate(ctrlToes, rc=True)
        # we want this to be at the world
        try:
            mc.parent(ctrlToesMirrorWork[0], w=True)
        except:
            pass

        ctrlToesMirror = []

        offsetCtrlStuffMirror = []
        for i in range(len(ctrlToesMirrorWork)):
            # switch the l/r,
            toRename = ctrlToesMirrorWork[i].replace(leftRightReplace, leftRightReplaceMirror)[:-1]
            mc.rename(ctrlToesMirrorWork[i], toRename)
            ctrlToesMirror.append(toRename)
        ctrlToesMirrorTop = ctrlToesMirror[0]
        # takes the initial offset value, duplicates it, flips the values around, then freezes the transformation
        # translates everything into place
        mirrorTrans = mc.xform(ctrlToesMirrorTop, q=True, ws=True, t=True, a=True)
        mirrorRot = mc.xform(ctrlToesMirrorTop, q=True, ws=True, rotation=True)
        # print("MirrorTrans = {0}".format(mirrorTrans))
        # print("MirrorAxis = {0}".format(mirrorRot))
        mirrorTransX = mirrorTrans[0] * -1
        mirrorTransY = mirrorTrans[1]
        mirrorTransZ = mirrorTrans[2]
        mirrorRotX = mirrorRot[0] * 1
        mirrorRotY = mirrorRot[1] * -1
        mirrorRotZ = mirrorRot[2] * -1

        mirrorXScal = mc.getAttr("{0}.sx".format(ctrlToesMirrorTop)) * -1
        # print(mirrorTrans)
        # print(mirrorXScal)

        # mirrors the values
        '''mc.setAttr("{0}.tx".format(ctrlToesMirrorTop), mirrorTransX)
        mc.setAttr("{0}.sx".format(ctrlToesMirrorTop), mirrorXScal)
        mc.setAttr("{0}.rx".format(ctrlToesMirrorTop), mirrorRotX)
        mc.setAttr("{0}.ry".format(ctrlToesMirrorTop), mirrorRotY)
        mc.setAttr("{0}.rz".format(ctrlToesMirrorTop), mirrorRotZ)'''

        mc.xform(ctrlToesMirrorTop, translation=(mirrorTransX, mirrorTransY, mirrorTransZ), ws=True, a=True)
        mc.xform(ctrlToesMirrorTop, scale=(mirrorXScal, 1, 1))
        mc.xform(ctrlToesMirrorTop, rotation=(mirrorRotX, mirrorRotY, mirrorRotZ))

        checkList = mc.listRelatives(ctrlToesMirrorTop)
        for i in range(len(checkList)):
            if mc.objectType(checkList[i]) == "transform":
                CRU.lockHideCtrls(checkList[i], translate=True, rotate=True, scale=True, toHide=True, visible=True,
                                  toLock=False)
        # mc.scale(-1, ctrlToesMirrorTop, x=True, pivot=(0,0,0), a=True)
        # mc.makeIdentity(ctrlToesMirrorTop, apply=True, translate=True, scale=True)

        return ctrlToesMirrorTop

    def tgpMakeBC(self, *args):

        checkSelLeft = mc.radioButtonGrp("selToesType_rbg", q=True, select=True)
        mirrorSel = mc.radioButtonGrp("selToesMirrorType_rbg", q=True, select=True)
        ctrlToes = mc.textFieldButtonGrp("ctrlToesLoad_tfbg", q=True, text=True)
        jntMasterToes = mc.textFieldButtonGrp("jntToesLoad_tf", q=True, text=True)
        grpLegs = mc.textFieldButtonGrp("grpLegLoad_tfbg", q=True, text=True)

        print(ctrlToes)

        jntAnkleTwist = mc.textFieldButtonGrp("jntAnkleTwistLoad_tf", q=True, text=True)

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

        checkList = jntMasterToes
        # note: the isCopy is not applicable due to the differences between the leg and arm joint setup.
        # However, editing them out is too much hassle,  it's easier just to leave them both false
        if ((checkList[0] == "")):
            mc.warning("You are missing a selection!")
            return
        else:
            if not (CRU.checkLeftRight(isLeft, jntMasterToes)):
                # if the values are not lined up properly, break out
                mc.warning("You are selecting the incorrect side")
                return

            # CRU.createLocatorToDelete()

            if mirrorRig:
                # we want to get the toe control before we add anything to it. When doing this programmatically, it's easier
                # make sure the children are not locked
                jntMasterToesMirror = self.tgpCreateMirrorToes(jntMasterToes, leftRightReplace,
                                                               leftRightReplaceMirror)

                jntBallMirror = jntBall.replace(leftRightReplace, leftRightReplaceMirror)
                ctrlToesMirror = self.tgpCreateMirrorCtrl(ctrlToes, leftRightReplace,
                                                          leftRightReplaceMirror)
                jntAnkleTwistMirror = jntAnkleTwist.replace(leftRightReplace, leftRightReplaceMirror)
                grpLegsMirror = grpLegs.replace(leftRightReplace, leftRightReplaceMirror)

            self.makeToes(jntBall, jntMasterToes, ctrlToes, grpLegs, jntAnkleTwist, leftRight, colourTU, isLeft)

            if mirrorRig:
                print("Mirroring")

                isLeftMirror = not isLeft

                self.makeToes(jntBallMirror, jntMasterToesMirror, ctrlToesMirror, grpLegsMirror, jntAnkleTwistMirror,
                              leftRightMirror, colourTUMirror, isLeftMirror)
