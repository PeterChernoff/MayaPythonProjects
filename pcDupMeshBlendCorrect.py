import maya.cmds as mc
nameSet = "correctivesSet"

myVals = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "v"]


s1 = mc.ls(sl=True, type="joint")

for i in range(len(myVals)):
    mc.setAttr("{0}.{1}".format(s, myVals[i]), k=toHide, l=toLock)