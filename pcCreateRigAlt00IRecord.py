import maya.cmds as mc
import pymel.core.runtime as pyml
# thanks to http://www.scatena.tv/blog/2016/06/03/maya-tips--tricks---mouse-capture/
class pcCreateRigAlt00IRecord(object):
    def __init__(self, deleteRight=False):
        mshChar = 'GEO_woman'

        self.tgpMakeBC(mshChar, deleteRight)

    def tgpMakeBC(self, mshChar, deleteRight):
        startFrame = mc.playbackOptions(query=True, minTime=True)

        mc.currentTime(startFrame)
        mySel = mc.ls(sl=True)[0]  # my current selection

        mc.cutKey(mySel, s=True)  # delete key command
        # return
        records = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz']
        for i in range(len(records)):
            name = "record{0}".format(i + 1)
            if mc.objExists(name):
                mc.delete(name)
            try:
                mc.setAttr("{0}.{1}".format(mySel, records[i]), 0)
            except:
                print("{0}.{1} could not be set".format(mySel, records[i]))

        # pyml.SetKeyTranslate()
        pyml.SetKey()
        currentUnitAngle = mc.currentUnit(q=True, a=True)
        mc.currentUnit(a="rad")

        mc.recordAttr(at=records)
        mc.play(record=True)
        mc.currentUnit(a=currentUnitAngle)
