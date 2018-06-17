import maya.cmds as mc
import maya.mel as mel

class pcCreateRigAlt00GMakeBlendShapeCopies():
    def __init__(self):
        mshChar = 'GEO_woman'

        self.tgpMakeBC(mshChar)

    def tgpMakeBC(self, mshChar):

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
        nonWeightName = [x for x in blndVals if ("weight" in x.lower())]
        print("weightTotal: {0}".format(weightName))
        print("nonWeightName: {0}".format(nonWeightName))



        lenBnld = len(blndVals)

        increment = lenBnld

        for i in range(lenBnld):

            blVlI = blndVals[i]
            if "weight" in blVlI[6:]:
                pass
            else:

                print("blndVals[{1}]: {0}".format(blndVals[i], i))
                newName = blVlI
                if "GEO" in blVlI:
                    newName = "{0}_copy".format(blVlI)
                elif "l_" in  blVlI[:2]:
                    newName = blVlI.replace("l_", "r_")
                mel.eval('blendShapeEditorDuplicateTargets;')
            """
            blendShape -e -tc on -t |GEO_woman|GEO_womanShape 22 GEO_woman1 1 -w 22 1  blendShape1;
            blendShape -e -rtd 0 22 blendShape1;
            aliasAttr GEO_woman_base_Copy blendShape1.w[22];
            """
            '''
            if "_Copy" in blndVals[i][-5:]:
                toRename = blndVals[i][:-5]
                if "l_" in toRename[:2]:
                    toRename1 = toRename.replace("l_", "r_")
                    print("l to r {0}".format(toRename1))
                elif "r_" in toRename[:2]:
                    toRename1 = toRename.replace("r_", "l_")
                    print("r to l {0}".format(toRename1))
                print(" --- c ---")
                # print (toRename1)
                print ("{0}.{1}".format(blndName, blndVals[i]))
                if cmds.objExists('{0}.{1}'.format(blndName, toRename1)):
                    cmds.aliasAttr('{0}.{1}'.format(blndName, toRename1), rm=True)
                cmds.aliasAttr(toRename1, '{0}.{1}'.format(blndName, blndVals[i]))'''

                # cmds.renameAttr( '{0}.{1}'.format(blndName, blndVals[i]), toRename1 )

        blndVals = mc.aliasAttr(blndName, q=True)
        print("blndVals {0}".format(blndVals))

