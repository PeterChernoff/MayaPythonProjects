import maya.cmds as mc
import pymel.core.runtime as pyml


# thanks to http://www.scatena.tv/blog/2016/06/03/maya-tips--tricks---mouse-capture/
class pcCreateRigAlt00KResetZeroSelectionHands(object):
    def __init__(self, deleteRight=False):
        mshChar = 'GEO_woman'

        self.tgpMakeBC(mshChar, deleteRight)

    def tgpMakeBC(self, mshChar, deleteRight):


        mySels = mc.ls(sl=True)  # my current selections

        print(mySels)
        handIndex = ["hand", "thumb", "pointer", "middle", "ring", "pink"]

        # records = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', ]
        for x in range(len(mySels)):
            print("----")
            mySel = mySels[x]
            if "CTRL" in mySel and any(handInx in mySel for handInx in handIndex) and "FK_" not in mySel:
                cont = True
            else:
                print("{0} does not have the value".format(mySel))
                cont = False

            if cont:
                records = mc.listAttr(mySels[x], k=True, sn=True)
                print(records)
                for i in range(len(records)):
                    try:
                        if 'length' not in records[i]:
                            mc.setAttr("{0}.{1}".format(mySel, records[i]), 0)
                        else:
                            mc.setAttr("{0}.{1}".format(mySel, records[i]), 1)
                    except:
                        print("{0}.{1} could not be set".format(mySel, records[i]))