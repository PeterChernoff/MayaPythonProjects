import maya.cmds as mc

class pcCreateRigUtilities:
    @staticmethod
    def createCTRLs(s, size=3, prnt = False, ornt = False, pnt=False, orientVal=(1, 0, 0), colour=5, sectionsTU=None, addPrefix=False, boxDimensionsLWH=None):
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
        if boxDimensionsLWH:
            x = boxDimensionsLWH[0]
            y = boxDimensionsLWH[1]
            z = boxDimensionsLWH[2]

            toPass = [(x, y, z), (-x, y, z), (-x, y, -z), (x, y, -z), (x, y, z),
                      (x, -y, z), (-x, -y, z), (-x, y, z), (-x, -y, z),
                      (-x, -y, -z), (-x, y, -z), (-x, -y, -z), (x, -y, -z),
                      (x, y, -z), (x, -y, -z), (x, -y, z), ]
            try:
                ctrl = mc.curve(ctrlName, r=True, d=1, p=toPass,)
            except:
                ctrl = mc.curve(name=ctrlName, d=1, p=toPass,)
            #ctrl = mc.curve(name=ctrlName, p=toPass, d=1)
        else:
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

    @staticmethod

    def lockHideCtrls(s, translate=False, rotate=False, scale=False, theVals = [], toHide = False, visible=False, toLock = True):
        myVals = list(theVals) #need to reset it every time
        if translate:
            myVals.extend(["tx", "ty", "tz"])
        if rotate:
            myVals.extend(["rx", "ry", "rz"])
        if scale:
            myVals.extend(["sx", "sy", "sz"])
        if visible:
            myVals.extend(["v"])


        for i in range(len(myVals)):
            mc.setAttr("{0}.{1}".format(s, myVals[i]),k=toHide, l=toLock)
            # to delete this next part
            if "_IK_" in s:
                print("{0}.{1}".format(s, myVals[i]))





    @staticmethod
    def setDriverDrivenValues(driver, driverAttribute, driven, drivenAttribute, driverValue, drivenValue, modifyInOut=None, modifyBoth=None):
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

    @staticmethod
    def createLocatorToDelete(createLocator=True):
        #This is little more than a signal to tell me I need to undo what I've done
        if createLocator:
            toDelete = mc.spaceLocator(p=(0, 0, 0))[0]
            mc.setAttr('{0}.overrideEnabled'.format(toDelete), 1)
            mc.setAttr("{0}.overrideColor".format(toDelete), 13)

    @staticmethod
    def tgpSetGeo(geoJntArray, setter="JNT_", *args):
        print(geoJntArray)
        for i in range(len(geoJntArray)):
            try:
                #print("------")
                theParent = geoJntArray[i]
                #print(theParent)
                geoName = theParent.replace(setter, "GEO_")
                #print(geoName)
                mc.parent(geoName, theParent)
                #print("parent successful")
                pivotTranslate = mc.xform(theParent, q=True, ws=True, rotatePivot=True)
                #print("pivotTranslate Successful")
                mc.makeIdentity(geoName, a=True, t=True, r=True, s=True)
                #print("make identity Successful")
                mc.xform(geoName, ws=True, pivots=pivotTranslate)
                #print("xform Successful")

            except:
                mc.warning("Geo for {0} properly named or available".format(geoJntArray[i]))
                mc.warning("===========")





