import maya.cmds as mc
import maya.mel as mel


class pcCreateRigAlt00HDeleteRight(object):
    def __init__(self, deleteRight=False):
        mshChar = 'GEO_woman'

        self.tgpMakeBC(mshChar, deleteRight)

    def tgpMakeBC(self, mshChar, deleteRight):

        history = mc.listHistory(mshChar)
        shape = history[0]
        blndName = mc.ls(history, typ='blendShape')[0]
        blndVals = mc.aliasAttr(blndName, q=True)
        print("-----")
        print("shape {0}".format(shape))
        print("history {0}".format(history))
        print("blndName {0}".format(blndName))
        print("blndVals {0}".format(blndVals))

        weightName = [x for x in blndVals if ("weight" in x.lower())]
        nonWeightName = [x for x in blndVals if ("weight" not in x.lower())]
        print("weightTotal: {0}".format(weightName))
        print("nonWeightName: {0}".format(nonWeightName))

        # we only want to delete if the copies is set to true
        if deleteRight:

            for i in range(len(nonWeightName)):
                # "d_" will stand for delete
                if "r_" in nonWeightName[i][:2] or "d_" in nonWeightName[i][:2]:
                    mc.aliasAttr("{0}.{1}".format(blndName, nonWeightName[i]), rm=True)

