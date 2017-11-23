import maya.cmds as mc
nameSet = "bind_set"

s1 = mc.ls('JNT*', type="joint")
s2 = ['_FK_', '_IK_', 'End']
s3 = []
for i in range(len(s1)):
    if not any(word in s1[i] for word in s2):
        s3.append((s1[i]))
print(s1)
print(s3)
mc.sets(s3, n="bind_set")
mc.select(cl=True)