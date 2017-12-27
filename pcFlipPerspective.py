import maya.cmds as mc

perspVal = mc.ls('persp')[0]
print(perspVal)
perspVal1 = 'persp1'

mirrorTrans = mc.xform(perspVal, q=True, ws=True, t=True, a=True)
mirrorRot = mc.xform(perspVal, q=True, ws=True, rotation=True)
mirrorTransX = mirrorTrans[0] * -1
mirrorTransY = mirrorTrans[1]
mirrorTransZ = mirrorTrans[2]
mirrorRotX = mirrorRot[0] * 1
mirrorRotY = mirrorRot[1] * -1
mirrorRotZ = mirrorRot[2] * -1

mc.xform(perspVal1, translation=(mirrorTransX, mirrorTransY, mirrorTransZ), ws=True, a=True)
# mc.xform(perspVal1, scale=(mirrorXScal, 1, 1))
mc.xform(perspVal1, rotation=(mirrorRotX, mirrorRotY, mirrorRotZ))
