import maya.cmds as mc

import pcCreateRig00AUtilities
from pcCreateRig00AUtilities import pcCreateRigUtilities as CRU

reload(pcCreateRig00AUtilities)


sels = mc.ls(sl=True)
sel = sels[0]

if len(sels) == 1:
    if CRU.checkObjectType(sel) == "mesh":
        if sel[:2] == "l_":
            toReplace = "l_"
            replaceWith = "r_"
        elif sel[:2] == "r_":
            toReplace = "r_"
            replaceWith = "l_"
        replaceName = sel.replace(toReplace, replaceWith)
        dupMesh = mc.duplicate(sel, n = replaceName, rc=True)[0]
        mc.move(0, 0, -50, replaceName, r=True)







    else:
        print("Please select a geometry")
else:
    print("Please select a single object")
