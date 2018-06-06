import maya.cmds as mc

import pcCreateRigAlt01SpineCode

reload(pcCreateRigAlt01SpineCode)

import pcCreateRigAlt02HeadCode

reload(pcCreateRigAlt02HeadCode)

import pcCreateRigAlt03LegsCode

reload(pcCreateRigAlt03LegsCode)

import pcCreateRigAlt04FeetCode

reload(pcCreateRigAlt04FeetCode)

import pcCreateRigAlt05ArmsCode

reload(pcCreateRigAlt05ArmsCode)

import pcCreateRigAlt06HandsCode

reload(pcCreateRigAlt06HandsCode)

from pcCreateRigAlt01SpineCode import pcCreateRigAlt01SpineCode as CRA1
from pcCreateRigAlt02HeadCode import pcCreateRigAlt02HeadCode as CRA2
from pcCreateRigAlt03LegsCode import pcCreateRigAlt03LegsCode as CRA3
from pcCreateRigAlt04FeetCode import pcCreateRigAlt04FeetCode as CRA4
from pcCreateRigAlt05ArmsCode import pcCreateRigAlt05ArmsCode as CRA5
from pcCreateRigAlt06HandsCode import pcCreateRigAlt06HandsCode as CRA6


class pcCreateRigAlt00ECreateRig(object):
    def __init__(self):
        self.runProgram()

    def runProgram(self):
        # runs the code to create a rig
        cra1 = CRA1()
        cra2 = CRA2()
        cra3 = CRA3()
        cra4 = CRA4()
        cra5 = CRA5()
        cra6 = CRA6()
