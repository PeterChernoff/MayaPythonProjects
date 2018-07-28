'''
Created on May 30, 2014
for Tin Girl Book and game project

@author: Eyal Assaf
'''
import maya.cmds as mc
# import tgpUtils as ut
from functools import partial

import pcCreateRigAlt00AUtilities
from pcCreateRigAlt00AUtilities import pcCreateRigUtilities as CRU

reload(pcCreateRigAlt00AUtilities)


class pcCreateRigAlt01SpineCodeExtras(object):
    def __init__(self, addChestBones=True, bndJnt="JNT_BND_spine5", ):

        # default passes these values
        self.tgpMakeBC(addChestBones, bndJnt, )

    def tgpMakeBC(self, addBreasts=None, bndJnt=None, *args):
        breastJoints = ["JNT_BND_l_breast", "JNT_BND_r_breast"]
        if addBreasts:

            for i in range(len(breastJoints)):

                try:
                    mc.parent(breastJoints[i], bndJnt)
                except:
                    mc.warning("Error in adding form joints")
        # reset the symmetry to the default because otherwise we might get wonky results
        # mc.symmetricModelling(symmetry=symmetry)
