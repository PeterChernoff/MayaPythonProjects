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

from pcCreateRigAlt00AUtilities import pcCreateRigUtilities as CRU

reload(pcCreateRigAlt00AUtilities)


class pcCreateRigAlt02HeadSpecialGeo(object):
    def __init__(self, jntHead = "JNT_BND_head", jntJaw = "JNT_BND_jaw2", jntEyeGeo="GEO", jntEyeBND="JNT_BND", createAlerts=True):

        jntEyeReplace=[jntEyeGeo, jntEyeBND]
        self.tgpMakeBC(jntHead, jntJaw, jntEyeReplace, createAlerts)



    def tgpMakeBC(self, jntHead, jntJaw, jntEyeReplace, createAlerts, *args):

        specialGeosHead = ["GEO_l_gland", "GEO_r_gland", "GEO_teethLower", "GEO_teethUpper" ]
        specialGeosEyes = ["GEO_l_eye", "GEO_r_eye", ]
        specialGeosJaw = ["GEO_teethLower"]

        for i in range(len(specialGeosHead)):
            try:
                mc.parent(specialGeosHead[i], jntHead)
            except:
                if createAlerts:
                    mc.warning("Head object {0} could not be parented to {1}".format(specialGeosHead[i],jntHead))

        for i in range(len(specialGeosJaw)):
            try:
                mc.parent(specialGeosJaw[i], jntJaw)
            except:
                if createAlerts:
                    mc.warning("Jaw object {0} could not be parented to {1}".format(specialGeosJaw[i],jntJaw))

        for i in range(len(specialGeosEyes)):
            toParent = specialGeosEyes[i].replace(jntEyeReplace[0], jntEyeReplace[1])
            try:
                mc.parent(specialGeosEyes[i], toParent)
            except:
                if createAlerts:
                    mc.warning("Eye object {0} could not be parented to {1}".format(specialGeosEyes[i],toParent))