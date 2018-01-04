import maya.cmds as mc

jointsTU = mc.ls(sl=True, type='joint')

for i in range(len(jointsTU)):
    jointName = jointsTU[i]
    if "JNT_" in jointName [:4]:
        toRename = jointName.replace("JNT_", "GRP_")
        autoName = jointName.replace("JNT_", "AUTO_")
        if not mc.objExists(toRename):
            mc.group(n=autoName, w=True, em=True)
            mc.group(autoName, n=toRename)
            toDelete = mc.parentConstraint(jointName, toRename)
            mc.delete(toDelete)
            mc.parent(jointName, autoName)
