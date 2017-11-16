import maya.cmds as mc

initSel = mc.ls(sl=True, fl=True, type="joint")
family = mc.listRelatives(initSel, ad=True)
family.extend(initSel)
print(family)
for i in range(len(family)):
    mc.setAttr("{0}.jointOrientX".format(family[i]), 0)
    mc.setAttr("{0}.jointOrientY".format(family[i]), 0)
    mc.setAttr("{0}.jointOrientZ".format(family[i]), 0)
