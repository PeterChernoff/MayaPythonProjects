import maya.cmds as mc
nameSet = "bind_set"

s1 = mc.ls('JNT*', type="joint")
s2 = ['_FK_', '_IK_', 'End', 'masterToes', 'ankleTwist'] #consider adding jaw1 and ball
s3 = []
for i in range(len(s1)):
    if not any(word in s1[i] for word in s2):
        s3.append((s1[i]))
    if "IK_spine" in s1[i] and "End" not in s1[i]:
        s3.append(s1[i])
    if "FK_hip" in s1[i] and "End" not in s1[i]:
        s3.append(s1[i])

print(s1)
print(s3)
if mc.objExists(nameSet):

    mc.sets(s3, include=nameSet)
else:
    mc.sets(s3, n=nameSet)
mc.select(cl=True)