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

import pcCreateRigAlt00DRenameBlendshapeCopies

reload(pcCreateRigAlt00DRenameBlendshapeCopies)
from pcCreateRigAlt00DRenameBlendshapeCopies import pcCreateRigAlt00DRenameBlendshapeCopies as CRAd


class pcCreateRigAlt00CBlendSDKCode(object):
    def __init__(self, mshChar="GEO_woman", renameVals=False):

        self.tgpMakeBC(mshChar, renameVals)

    def tgpMakeBC(self, mshChar, renameVals, *args):
        # print(mshChar)

        if renameVals:
            CRAd(mshChar=mshChar)

        history = mc.listHistory(mshChar)
        # print("history {0}".format(history))
        blndName = mc.ls(history, typ='blendShape')[0]
        # print("blndName {0}".format(blndName))
        blndVals = mc.aliasAttr(blndName, q=True)
        # print("blndVals {0}".format(blndVals))
        blndValNames = []
        blndValWeights = []

        weightName = [x for x in blndVals if ("weight" in x.lower())]
        nonWeightName = [x for x in blndVals if ("weight" not in x.lower())]

        for i in range(len(nonWeightName)):
            # "d_" will stand for delete
            if "d_" in nonWeightName[i][:2]:
                mc.aliasAttr("{0}.{1}".format(blndName, nonWeightName[i]), rm=True)

        skip = False
        for i in range(len(blndVals)):
            if skip:
                skip = False
                continue  # skip to the next value. Only if Copy was the previous value
            if "Copy" in blndVals[i][-4:]:
                # If 'copy' is in there, it's probably badly named
                skip = True
                continue
            if "GEO_" in blndVals[i][:3]:
                # If 'GEO' is in there, it's probably badly named
                skip = True
                continue
            if "base" in blndVals[i][-4:]:
                # If 'base' is in there, it's referring to the basic shape
                skip = True
                continue
            if "d_" in blndVals[i][:2]:
                # If 'd_' is in there, it's referring to something to delete
                skip = True
                continue
            if "w[" in blndVals[i][:2]:
                # If 'w[' is in there, it's likely referring to something that has been deleted
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
                # print(theVals)
            else:
                blndValNames.append(blndVals[i])

        # print(blndValWeights)
        # print(blndValNames)

        # delete the preexisting blendshape animations
        test = mc.ls("blendShape1_*", type="animCurveUU")
        print("{0}".format(test))
        # deletes pre-existing lists
        if len(test) != 0:
            mc.delete(test)

        for i in range(len(blndValNames)):
            custVal = False
            try:
                driver, driverAttrDrvnVal = blndValNames[i].split("__", 1)
            except:
                print ("Error! {0}".format(blndValNames[i]))
            if "FK_" in driver[:3]:

                driver = "CTRL_" + driver
            elif "CTRL_" in driver[:5]:
                custVal = True

            else:
                driver = "JNT_BND_" + driver
            # print(driver)
            # print(driverAttrDrvnVal)
            driverAttr, driverValNum = self.getDriverAttrDrivenVals(driverAttrDrvnVal, custVal)
            # print("driverAttr {0}".format(driverAttr))
            # print("drivenValue {0}".format(driverValNum))

            CRU.setDriverDrivenValues(driver, driverAttr, blndName, blndValWeights[i], drivenValue=0, driverValue=0,
                                      modifyBoth="linear")

            CRU.setDriverDrivenValues(driver, driverAttr, blndName, blndValWeights[i], drivenValue=1,
                                      driverValue=driverValNum,
                                      modifyBoth="linear")
            # CRU.setDriverDrivenValues(driver, driverAttr, driven, w0w1Attr[0], drivenValue=0, driverValue=1,
            #                         modifyBoth="linear")

        # CRU.createLocatorToDelete()

    def getDriverAttrDrivenVals(self, driverAttrDrvnVal, custVal, *args):
        driverAttr, drivenVal = driverAttrDrvnVal.split("_", 1)
        # if the last character is 'e', remove the last letter
        if drivenVal[-1:]=="e":
            drivenVal =drivenVal[:-1]

        if not custVal:
            driverAttr = driverAttr.lower()

        # determines if the value is positive or negative
        if drivenVal[0].lower() == 'p':
            mult = 1
        elif drivenVal[0].lower() == 'm':
            mult = -1
        driverValNum = int(drivenVal[1:])
        # print(drivenValNum)
        return driverAttr, driverValNum * mult
