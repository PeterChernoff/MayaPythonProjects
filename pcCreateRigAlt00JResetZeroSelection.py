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
        toDelete = mc.listAttr(mySels[0], k=True, sn=True)
        print(toDelete)

        records = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz']
        for x in range(len(mySels)):
            mySel=  mySels[x]
            for i in range(len(records)):
                try:
                    mc.setAttr("{0}.{1}".format(mySel, records[i]), 0)
                except:
                    print("{0}.{1} could not be set".format(mySel, records[i]))

        mc.currentUnit(a=currentUnitAngle)

