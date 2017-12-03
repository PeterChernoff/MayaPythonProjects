import maya.cmds as mc

import pcCreateRig00AUtilities
from pcCreateRig00AUtilities import pcCreateRigUtilities as CRU

reload(pcCreateRig00AUtilities)

nameSet = "myCorrectivesSet"

myVals = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "v"]


sels = mc.ls(sl=True)
sel = sels[0]
print(sel)
if len(sels) == 1:
    if CRU.checkObjectType(sel) == "mesh":
        print("I got here")

        dupMesh = mc.duplicate(sel, rc=True)[0]

        try:
            mc.parent(dupMesh, w=True)
        except:
            pass
        mc.select(dupMesh)
        CRU.lockHideCtrls(dupMesh, translate=True, rotate=True, scale=True, toHide=True, visible=True, toLock=False)
        if mc.objExists(nameSet):
            mc.sets(dupMesh, include=nameSet)
        else:
            mc.sets(dupMesh, n=nameSet)
        mc.move(0, 0, -100, dupMesh)


    else:
        print("Please select a geometry")
else:
    print("Please select a single object")
