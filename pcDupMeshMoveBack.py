import maya.cmds as mc

import pcCreateRig00AUtilities
from pcCreateRig00AUtilities import pcCreateRigUtilities as CRU

reload(pcCreateRig00AUtilities)


sels = mc.ls(sl=True)
sel = sels[0]

if len(sels) == 1:
    if CRU.checkObjectType(sel) == "mesh":
        print("I got here")

        dupMesh = mc.duplicate(sel, rc=True)[0]
        print(sel[:2])
        if sel[:2] == "l_":
            print("Dude!")
        elif sel[:2] == "r_":
            print("Dudette!")



    else:
        print("Please select a geometry")
else:
    print("Please select a single object")
