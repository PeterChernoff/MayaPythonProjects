import maya.cmds as mc
import pymel.core.runtime as pyml


# thanks to http://www.scatena.tv/blog/2016/06/03/maya-tips--tricks---mouse-capture/
class pcCreateRigAlt00JResetZeroSelection(object):
    def __init__(self, deleteRight=False):
        mshChar = 'GEO_woman'

        self.tgpMakeBC(mshChar, deleteRight)

    def tgpMakeBC(self, mshChar, deleteRight):

        currentUnitAngle = mc.currentUnit(q=True, a=True)
        mc.currentUnit(a="degree")
        mySels = mc.ls(sl=True)  # my current selections
        if mySels is None:
            return
        print(mySels)

        records = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', ]
        for x in range(len(mySels)):
            mySel = mySels[x]
            for i in range(len(records)):
                try:
                    if 's' not in records[i][:1]:
                        mc.setAttr("{0}.{1}".format(mySel, records[i]), 0)
                    else:
                        mc.setAttr("{0}.{1}".format(mySel, records[i]), 1)
                except:
                    print("{0}.{1} could not be set".format(mySel, records[i]))


            attrList = mc.listAttr(mySel, k=True, sn=True)

            if "length" in attrList:
                mc.setAttr("{0}.{1}".format(mySel, "length"), 1)

        mc.currentUnit(a=currentUnitAngle)
