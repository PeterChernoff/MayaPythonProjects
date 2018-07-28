import maya.cmds as mc

import pcCreateRigAlt00AUtilities

reload(pcCreateRigAlt00AUtilities)

import pcCreateRigAlt01SpineCode

reload(pcCreateRigAlt01SpineCode)

import pcCreateRigAlt01SpineCodeExtras

reload(pcCreateRigAlt01SpineCodeExtras)

import pcCreateRigAlt02HeadCode

reload(pcCreateRigAlt02HeadCode)

import pcCreateRigAlt02HeadSpecialGeo

reload(pcCreateRigAlt02HeadSpecialGeo)

import pcCreateRigAlt03LegsCode

reload(pcCreateRigAlt03LegsCode)

import pcCreateRigAlt04FeetCode

reload(pcCreateRigAlt04FeetCode)

import pcCreateRigAlt05ArmsCode

reload(pcCreateRigAlt05ArmsCode)

import pcCreateRigAlt06HandsCode

reload(pcCreateRigAlt06HandsCode)

import pcCreateRigAlt06HandsCodeAdjust

reload(pcCreateRigAlt06HandsCodeAdjust)

from pcCreateRigAlt01SpineCode import pcCreateRigAlt01SpineCode as CRA1
from pcCreateRigAlt01SpineCodeExtras import pcCreateRigAlt01SpineCodeExtras as CRA1A
from pcCreateRigAlt02HeadCode import pcCreateRigAlt02HeadCode as CRA2
from pcCreateRigAlt02HeadSpecialGeo import pcCreateRigAlt02HeadSpecialGeo as CRA2A
from pcCreateRigAlt03LegsCode import pcCreateRigAlt03LegsCode as CRA3
from pcCreateRigAlt04FeetCode import pcCreateRigAlt04FeetCode as CRA4
from pcCreateRigAlt05ArmsCode import pcCreateRigAlt05ArmsCode as CRA5
from pcCreateRigAlt06HandsCode import pcCreateRigAlt06HandsCode as CRA6
from pcCreateRigAlt06HandsCodeAdjust import pcCreateRigAlt06HandsCodeAdjust as CRA6A


class pcCreateRigAlt00ECreateRig(object):
    def __init__(self, cbGeo=True):
        self.runProgram(cbGeo)

    def runProgram(self, cbGeo):
        # runs the code to create a rig
        CRA1(cbGeo=cbGeo)
        CRA1A(addChestBones=True)
        CRA2(cbGeo=cbGeo)
        CRA2A(createAlerts=cbGeo)
        CRA3(cbGeo=cbGeo)

        CRA4()

        CRA5(cbGeo=cbGeo)
        CRA6(cbGeo=cbGeo)
        CRA6A()

        mc.select(cl=True)
