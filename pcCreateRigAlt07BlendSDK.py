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
import pcCreateRig00AUtilities
from pcCreateRig00AUtilities import pcCreateRigUtilities as CRU

reload(pcCreateRig00AUtilities)


class pcCreateRig10BlendSDK(UI):
    def __init__(self):

        self.window = "bcWindow"
        self.title = "pcRigBlendSDK"
        self.winSize = (500, 200)

        self.createUI()

    def createCustom(self, *args):
        '''
        #
        #
        #
        #
        #
        '''

        mc.rowColumnLayout(nc=2, cw=[(1, 500), (2, 500)], cs=[1, 5], rs=[1, 3])

        mc.text(l="Select the Mesh")

        mc.text(l="")

        mc.setParent("..")
        mc.separator(st="in", h=15, w=500)

        # sources

        mc.rowColumnLayout(nc=2, cw=[(1, 100), (2, 380)], cs=[1, 5], rs=[1, 3])

        mc.text(bgc=(0.85, 0.65, 0.25), l="Geometry: ")
        mc.textFieldButtonGrp("mshCharLoad_tf", cw=(1, 322), bl="  Load  ", tx="male_geo")

        mc.setParent("..")
        mc.separator(st="in", h=15, w=500)
        # load buttons
        #

        mc.textFieldButtonGrp("mshCharLoad_tf", e=True, bc=self.loadSrc1Btn)

        self.selLoad = []
        self.ctrlsArray = []
        mc.showWindow(self.window)

    def createButtonCmd(self, *args):
        self.tgpMakeBC()

    def loadSrc1Btn(self):
        self.selSrc1 = self.tgpLoadTxBtn("mshCharLoad_tf", "mesh", "Body mesh", ["geo"])
        print(self.selSrc1)

    def tgpLoadTxBtn(self, loadBtn, objectType, objectDesc, keywords, objectNickname=None):
        if objectNickname is None:
            objectNickname = objectType

        self.selLoad = []
        self.selLoad = mc.ls(sl=True, fl=True)

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

    def tgpMakeBC(self, *args):

        mc.textFieldButtonGrp("mshCharLoad_tf", e=True, bc=self.loadSrc1Btn)

        mshChar = mc.textFieldButtonGrp("mshCharLoad_tf", q=True, text=True)

        # print(mshChar)
        history = mc.listHistory(mshChar)
        print("history {0}".format(history))
        blndName = mc.ls(history, typ='blendShape')[0]
        print("blndName {0}".format(blndName))
        blndVals = mc.aliasAttr(blndName, q=True)
        print("blndVals {0}".format(blndVals))
        blndValNames = []
        blndValWeights = []

        skip = False
        for i in range(len(blndVals)):
            if skip:
                skip = False
                continue  # skip to the next value. Only if Copy was the previous value
            if "Copy" in blndVals[i][-4:]:
                # If 'copy' is in there, it's probably badly named
                skip = True
                continue
            if "base" in blndVals[i][-4:]:
                # If 'base' is in there, it's referring to the basic shape
                skip = True
                continue
            if "combo" in blndVals[i][:5]:
                # If 'combo' is in there, it's referring to the basic shape
                skip = True
                continue
            if "tempAlias" in blndVals[i]:
                # If 'tempAlias' is in there, it's referring to the basic shape
                skip = True
                continue
            if 'weight' in blndVals[i][:6]:
                # These are typically
                blndValWeights.append(blndVals[i])
                theVals = mc.getAttr("{0}.{1}".format(blndName, blndVals[i]))
                print(theVals)
            else:
                blndValNames.append(blndVals[i])

        print(blndValWeights)
        print(blndValNames)

        for i in range(len(blndValNames)):
            try:
                driver, driverAttrDrvnVal = blndValNames[i].split("__", 1)
            except:
                print ("Error! {0}".format(blndValNames[i]))
            if "FK_" in driver[:3]:

                driver = "CTRL_" + driver

            else:
                driver = "JNT_" + driver
            print(driver)
            print(driverAttrDrvnVal)
            driverAttr, driverValNum = self.getDriverAttrDrivenVals(driverAttrDrvnVal)
            print("driverAttr {0}".format(driverAttr))
            print("drivenValue {0}".format(driverValNum))

            CRU.setDriverDrivenValues(driver, driverAttr, blndName, blndValWeights[i], drivenValue=0, driverValue=0,
                                      modifyBoth="linear")

            CRU.setDriverDrivenValues(driver, driverAttr, blndName, blndValWeights[i], drivenValue=1,
                                      driverValue=driverValNum,
                                      modifyBoth="linear")
            # CRU.setDriverDrivenValues(driver, driverAttr, driven, w0w1Attr[0], drivenValue=0, driverValue=1,
            #                         modifyBoth="linear")

        # CRU.createLocatorToDelete()

        '''

        vals = cmds.listAttr("correctives.w")
        print(vals)
        history = cmds.listHistory("male_geo")
        print(history)
        test = cmds.ls(history, typ='blendShape')
        print(test)
        
        vals = cmds.aliasAttr("correctives", q=True)
        print(vals)'''

    def getDriverAttrDrivenVals(self, driverAttrDrvnVal, *args):
        driverAttr, drivenVal = driverAttrDrvnVal.split("_", 1)
        driverAttr = driverAttr.lower()
        # print(driverAttr)
        # print(drivenVal)
        if drivenVal[0].lower() == 'p':
            mult = 1
        elif drivenVal[0].lower() == 'm':
            mult = -1
        driverValNum = int(drivenVal[1:])
        # print(drivenValNum)
        return driverAttr, driverValNum * mult
