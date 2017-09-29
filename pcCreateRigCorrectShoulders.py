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


class pcCorrectShoulders(UI):
    def __init__(self):

        self.window = "bcWindow"
        self.title = "pcCorrectShoulders"
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
        mc.rowColumnLayout(nc=3, cw=[(1, 125), (2, 150), (3, 150)], cs=[1, 5], rs=[1, 3], cal=([1,"left"],[2,"left"],[3,"left"],))

        mc.text(l="Mirror As Well?")
        #mc.setParent("..")
        mc.radioButtonGrp("selArmMirrorType_rbg", la2=["No", "Yes"], nrb=2, sl=2, cw2=[50, 50],)
        mc.setParent("..")
        mc.separator(st="in", h=20, w=500)

        mc.rowColumnLayout(nc=3, cw=[(1, 100), (2, 200), (3, 150)], cs=[1, 5], rs=[1, 3],cal=([1,"left"],[2,"left"],[3,"left"],))
        mc.text(l="Initial Limb: ")
        mc.radioButtonGrp("selArmType_rbg", la2=["Left", "Right"], nrb=2, sl=1, cw2=[50, 50],)
        mc.setParent("..")
        mc.separator(st="in", h=20, w=500)

        # sources
        mc.rowColumnLayout(nc=2, cw=[(1, 100), (2, 370)], cs=[1, 5], rs=[1, 3])
        mc.text(bgc=(0.85, 0.65, 0.25), l="IK Spine: ")
        mc.textFieldButtonGrp("jointLoad_tfbg", cw=(1, 322), bl="  Load  ")


        #mc.text(bgc=(0.85, 0.65, 0.25), l="COG: ")
        #mc.textFieldButtonGrp("cog_tfbg", cw=(1, 322), bl="  Load  ", tx="CTRL_COG")

        mc.text(bgc=(0.85, 0.65, 0.25), l="Shoulder CTRL: ")
        mc.textFieldButtonGrp("ctrlShoulderLoad_tf", cw=(1, 322), bl="  Load  ", tx="CTRL_l_shoulder")

        mc.setParent("..")


        mc.separator(st="in", h=20, w=500)

        # load buttons
        #

        mc.textFieldButtonGrp("jointLoad_tfbg", e=True, bc=self.loadSrc1Btn)
        mc.textFieldButtonGrp("ctrlShoulderLoad_tf", e=True, bc=self.loadSrc2Btn)

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
        '''self.src1Sel = self.tgpLoadTxBtn("jointLoad_tfbg", "selType_rbg", "selGeo_cb")'''
        self.jntSel = self.loadCtrlBtn("ctrlShoulderLoad_tf", "transform")

    def loadCtrlBtn(self, loadBtn, myType):
        self.selLoad = []
        #self.selLoad = mc.ls(sl=True, fl=True, type="nurbsCurve")
        self.selLoad = mc.ls(sl=True, fl=True, type=myType)

        if (len(self.selLoad) != 1):
            mc.warning("Select only the Control")
            return
        else:
            selName = self.selLoad[0]
            mc.textFieldButtonGrp(loadBtn, e=True, tx=selName)
            print(selName)




    def tgpLoadTxBtn(self, loadBtn, myType):
        # hierarchy
        self.selLoad = []
        self.selLoad = mc.ls(sl=True, fl=True, type=myType)


        if (len(self.selLoad) != 1):
            mc.warning("Select only the spine joint")
            return
        else:

            selName = ', '.join(self.selLoad)

            # get the children joints
            self.parent = self.selLoad[0]
            self.child = mc.listRelatives(self.selLoad, ad=True, type="joint")
            # collect the joints in an array
            self.jointArray = [self.parent]
            # reverse the order of the children joints
            self.child.reverse()

            # add to the current list
            self.jointArray.extend(self.child)


            self.jointEndArray = [x for x in self.jointArray if "End" in x[-3:]]

            self.jointUnderSpineEnd = mc.listRelatives(self.jointEndArray[0], p=True)[0]
            mc.textFieldButtonGrp(loadBtn, e=True, tx=self.jointUnderSpineEnd)



        return self.jointArray

    def createCTRLs(self, s, size=3, prnt = False, ornt = False, pnt=False, orientVal=(1, 0, 0), colour=5, sectionsTU=None, addPrefix=False):
        selname = str(s)
        '''
        0 gray, 1 black, 2 dark grey, 3 light gray, 4 red
        5 dark blue, 6 blue, 7 dark green, 8 dark purple, 9 pink
        10 brown, 11 dark brown, 12 brownish red, 13 light red, 14 green
        darkish blue
        white
        yellow
        cyan
        greenish blue
        light pink
        peach
        other yellow
        turquoise
        light brown
        puke yellow
        puke green
        lightish green
        light blue
        darkish blue
        purple
        magenta
        '''

        if addPrefix:
            ctrlName = "CTRL_" + selname
        else:
            ctrlName = selname.replace("JNT_", "CTRL_")

        if sectionsTU:
            ctrl = mc.circle(nr=orientVal, r=size, n=ctrlName, degree=1, sections=sectionsTU)[0]
        else:
            ctrl = mc.circle(nr=orientVal, r=size, n=ctrlName)[0]

        mc.setAttr('{0}.overrideEnabled'.format(ctrlName), 1)
        mc.setAttr("{0}.overrideColor".format(ctrlName), colour)
        auto = mc.group(ctrl, n="AUTO_" + ctrl)
        offset = mc.group(auto, n="OFFSET_" + ctrl)

        mc.parentConstraint(s, offset, mo=0)
        mc.delete(mc.parentConstraint(s, offset))
        # parent and orient/point are not inclusive
        if prnt:
            mc.parentConstraint(ctrl, s, mo=0)
        else:
            if ornt:
                mc.orientConstraint(ctrl, s, mo=0)
            if pnt:
                mc.pointConstraint(ctrl, s, mo=0)
        # we normally don't include auto
        offsetCtrl = [offset, ctrl, auto]
        return offsetCtrl

    def lockHideCtrls(self, s, translate=False, rotate=False, scale=False):
        if translate:

            mc.setAttr("{0}.tx".format(s),k=False, l=True)
            mc.setAttr("{0}.ty".format(s), k=False, l=True)
            mc.setAttr("{0}.tz".format(s), k=False, l=True)
        if rotate:

            mc.setAttr("{0}.rx".format(s),k=False, l=True)
            mc.setAttr("{0}.ry".format(s), k=False, l=True)
            mc.setAttr("{0}.rz".format(s), k=False, l=True)
        if scale:

            mc.setAttr("{0}.sx".format(s),k=False, l=True)
            mc.setAttr("{0}.sy".format(s), k=False, l=True)
            mc.setAttr("{0}.sz".format(s), k=False, l=True)

    def setDriverDrivenValues(self, driver, driverAttribute, driven, drivenAttribute, driverValue, drivenValue, modifyInOut=None, modifyBoth=None):
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
                                 dv=driverValue, v=drivenValue, itt = modifyIn, ott = modifyOut)
        else:
            mc.setDrivenKeyframe('{0}.{1}'.format(driven, drivenAttribute), cd='{0}.{1}'.format(driver, driverAttribute),
                             dv=driverValue, v=drivenValue)




    def tgpSetDriverArmFKIKSwitch(self, driver, driverAttr, driven, *args):
        w0w1Attr = mc.listAttr(driven)[-2:]
        self.setDriverDrivenValues(driver, driverAttr, driven, w0w1Attr[0], drivenValue=0, driverValue=1, modifyBoth="linear")
        self.setDriverDrivenValues(driver, driverAttr, driven, w0w1Attr[0], drivenValue=1, driverValue=0, modifyBoth="linear")
        self.setDriverDrivenValues(driver, driverAttr, driven, w0w1Attr[1], drivenValue=0, driverValue=0, modifyBoth="linear")
        self.setDriverDrivenValues(driver, driverAttr, driven, w0w1Attr[1], drivenValue=1, driverValue=1, modifyBoth="linear")


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
                ctrlFKIK, ctrlFKIKAttr, ctrlIKChest, checkboxTwists, makeExpression, makeTwistJnts, isCopy,
                checkboxSpine, toReplace="", toReplaceWith="", *args):
        pass

    def tgpMakeBC(self, *args):

        checkSelLeft = mc.radioButtonGrp("selArmType_rbg", q=True, select=True)
        mirrorSel = mc.radioButtonGrp("selArmMirrorType_rbg", q=True, select=True)

        self.jntNames = mc.textFieldButtonGrp("jointLoad_tfbg", q=True, text=True)

        shoulderCtrl = mc.textFieldButtonGrp("ctrlShoulderLoad_tf", q=True, text=True)
        toDelete = mc.listRelatives(shoulderCtrl, p=True)
        shoulderOffsetCtrlGrp = mc.listRelatives(toDelete [0], p=True)[0]

        geoJntArray = self.jointArray

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

        if checkSelLeft == 1:
            isLeft = True
            leftRight = "_l_"
            leftRightReverse="_r_"
            colourTU = 14
            colourTUReverse = 13
        else:
            isLeft = False
            leftRight = "_r_"
            leftRightReverse = "_l_"
            colourTU = 13
            colourTUReverse = 14

        print(self.jointUnderSpineEnd)
        print(shoulderOffsetCtrlGrp)


        # make sure the selections are not empty
        checkList = [self.jntNames]

        if ((checkList[0] == "")):
            mc.warning("You are missing a selection!")
            return
        else:
            if isLeft:
                if leftRight not in shoulderOffsetCtrlGrp:
                    mc.warning("Please select the left side")
            else:
                if leftRight not in shoulderOffsetCtrlGrp:
                    mc.warning("Please select the right side")
            try:
                mc.parent(shoulderOffsetCtrlGrp, w=True)
            except:
                mc.warning("The shoulder is already a child of the world")

            mc.parentConstraint(self.jointUnderSpineEnd, shoulderOffsetCtrlGrp, mo=True)
            if mirrorRig:
                mirrorSOCG = shoulderOffsetCtrlGrp.replace(leftRight, leftRightReverse)

                try:
                    mc.parent(mirrorSOCG, w=True)
                except:
                    mc.warning("The shoulder is already a child of the world")

                mc.parentConstraint(self.jointUnderSpineEnd, mirrorSOCG, mo=True)
























