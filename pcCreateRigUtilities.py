import maya.cmds as mc

class pcCreateRigUtilities(object):

    def createCTRLs(self, s, size=3, prnt = False, ornt = False, pnt=False, orientVal=(1, 0, 0), colour=5, sectionsTU=None, addPrefix=False):
        selname = str(s)
        '''
        0 gray, 1 black, 2 dark grey, 3 light gray, 4 red
        5 dark blue, 6 blue, 7 dark green, 8 darker purple, 9 pink
        10 brown, 11 dark brown, 12 brownish red, 13 light red, 14 green
        15 darkish blue, 16 white, 17 yellow, 18 cyan, 19 pale green
        20 light pink, 21 peach, 22 other yellow, 23 turquoise, 24 light brown/orange
        25 puke yellow, 26 puke green. 27 lightish green, 28 light blue, 29 darkish blue
        30 dark purple, 31 magenta
        
        0 gray, 1 black, 2 dark grey, 3 light gray, 16 white, 
        4 red, 12 brownish red, 13 light red, 
        5 dark blue, 6 blue, 15 darkish blue, 18 cyan, 28 light blue, 29 darkish blue
        7 dark green, 14 green, 19 pale green, 23 turquoise, 26 puke green. 27 lightish green,
        8 darker purple, 30 dark purple, 
        9 pink, 20 light pink, 21 peach, 31 magenta
        10 brown, 11 dark brown, 24 light brown/orange
        17 yellow, 22 other yellow, 25 puke yellow,
        '''

        if addPrefix:
            ctrlName = "CTRL_" + selname
        else:
            ctrlName = selname.replace("JNT_", "CTRL_")

        if sectionsTU:
            ctrl = mc.circle(nr=orientVal, r=size, n=ctrlName, degree=1, sections=sectionsTU)[0]
        else:
            ctrl = mc.circle(nr=orientVal, r=size, n=ctrlName)[0]

        mc.setAttr('{0}.overrideEnabled'.format(ctrlName), 1)
        mc.setAttr("{0}.overrideColor".format(ctrlName), colour)
        auto = mc.group(ctrl, n="AUTO_" + ctrl)
        offset = mc.group(auto, n="OFFSET_" + ctrl)

        mc.parentConstraint(s, offset, mo=0)
        mc.delete(mc.parentConstraint(s, offset))
        # parent and orient/point are not inclusive
        if prnt:
            mc.parentConstraint(ctrl, s, mo=0)
        else:
            if ornt:
                mc.orientConstraint(ctrl, s, mo=0)
            if pnt:
                mc.pointConstraint(ctrl, s, mo=0)
        # we normally don't include auto
        offsetCtrl = [offset, ctrl, auto]
        return offsetCtrl

    def lockHideCtrls(self, s, translate=False, rotate=False, scale=False, theVals = [], toHide = False, toLock = True):

        if translate:
            theVals.extend(["tx", "ty", "tz"])
        if rotate:

            theVals.extend(["rx", "ry", "rz"])
        if scale:
            theVals.extend(["sx", "sy", "sz"])

        for i in range(len(theVals)):
            mc.setAttr("{0}.{1}".format(s, theVals[i]),k=toHide, l=toLock)




    def setDriverDrivenValues(self, driver, driverAttribute, driven, drivenAttribute, driverValue, drivenValue, modifyInOut=None, modifyBoth=None):
        # the way it's written, the setDrivenKeyframe is driven-> driver, not the other way around. My custom value does the more intuitive manner
        # modify tanget is determining if the tanget goes in or out
        if modifyInOut or modifyBoth:

            if modifyBoth:
                modifyIn = modifyBoth
                modifyOut = modifyBoth
            else:
                modifyIn = modifyInOut[0]
                modifyOut = modifyInOut[1]
            mc.setDrivenKeyframe('{0}.{1}'.format(driven, drivenAttribute),
                                 cd='{0}.{1}'.format(driver, driverAttribute),
                                 dv=driverValue, v=drivenValue, itt = modifyIn, ott = modifyOut)
        else:
            mc.setDrivenKeyframe('{0}.{1}'.format(driven, drivenAttribute), cd='{0}.{1}'.format(driver, driverAttribute),
                             dv=driverValue, v=drivenValue)


