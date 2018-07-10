import maya.cmds as mc

class pcCreateRigAlt00DRenameBlendshapeCopies(object):
    def __init__(self, mshChar = 'GEO_woman'):


        self.tgpMakeBC(mshChar)

    def tgpMakeBC(self, mshChar):


        history = mc.listHistory(mshChar)
        # print("history {0}".format(history))
        blndName = mc.ls(history, typ='blendShape')[0]
        # print("blndName {0}".format(blndName))
        blndVals = mc.aliasAttr(blndName, q=True)
        # print("blndVals {0}".format(blndVals))

        # takes a value that is labelled as copy and renames it to its opposite
        for i in range(len(blndVals)):
            if "_Copy" in blndVals[i][-5:]:
                toRename = blndVals[i][:-5]
                if "l_" in toRename[:2]:
                    toRename1 = toRename.replace("l_", "r_")
                    # print("l to r {0}".format(toRename1))
                elif "r_" in toRename[:2]:
                    toRename1 = toRename.replace("r_", "l_")
                    # print("r to l {0}".format(toRename1))
                elif "combo" in toRename[:5]:
                    if "_l_" in toRename:
                        toRename1 = toRename.replace("_l_", "_r_")
                        # print("l to r {0}".format(toRename1))
                    elif "_r_" in toRename:
                        toRename1 = toRename.replace("_r_", "_l_")
                        # print("r to l {0}".format(toRename1))
                    else:
                        toRename1 = toRename
                        # print("No renaming")
                # print(" --- c ---")
                # print (toRename1)
                # print ("{0}.{1}".format(blndName, blndVals[i]))
                if mc.objExists('{0}.{1}'.format(blndName, toRename1)):
                    mc.aliasAttr('{0}.{1}'.format(blndName, toRename1), rm=True)
                mc.aliasAttr(toRename1, '{0}.{1}'.format(blndName, blndVals[i]))

                # mc.renameAttr( '{0}.{1}'.format(blndName, blndVals[i]), toRename1 )

        # this lets us rename any groups
        for i in range(200):
            getName = mc.getAttr("{0}.{1}".format(blndName, "targetDirectory[{0}].directoryName".format(i)))
            if "Group" in getName:
                continue
            print(getName)


            if "l_" in getName[:2] and "_Copy" in getName[-5:]:
                renameVal = "r_{0}".format(getName[2:-5])
                mc.setAttr("{0}.{1}".format(blndName, "targetDirectory[{0}].directoryName".format(i)), renameVal,
                           type='string')
            elif "_Copy" in getName[-5:]:
                renameVal = "{0}".format(getName[:-5])
                mc.setAttr("{0}.{1}".format(blndName, "targetDirectory[{0}].directoryName".format(i)), renameVal,
                           type='string')

        blndVals = mc.aliasAttr(blndName, q=True)
        # print("blndVals {0}".format(blndVals))



