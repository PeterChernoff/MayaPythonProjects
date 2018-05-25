import maya.cmds as cmds

class pcCreateRigAlt08RenameBlendshapeCopies():
    def __init__(self):
        mshChar = 'emma_body_GEO'

        self.tgpMakeBC(mshChar)

    def tgpMakeBC(self, mshChar):

        history = cmds.listHistory(mshChar)
        # print("history {0}".format(history))
        blndName = cmds.ls(history, typ='blendShape')[0]
        # print("blndName {0}".format(blndName))
        blndVals = cmds.aliasAttr(blndName, q=True)
        # print("blndVals {0}".format(blndVals))

        for i in range(len(blndVals)):
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
                cmds.aliasAttr(toRename1, '{0}.{1}'.format(blndName, blndVals[i]))

                # cmds.renameAttr( '{0}.{1}'.format(blndName, blndVals[i]), toRename1 )

        blndVals = cmds.aliasAttr(blndName, q=True)
        print("blndVals {0}".format(blndVals))

