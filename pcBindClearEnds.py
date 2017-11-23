import maya.cmds as mc

ends = mc.ls('*End')
print(ends)
mc.sets(ends, rm="bind_set")
mc.select(cl=True)