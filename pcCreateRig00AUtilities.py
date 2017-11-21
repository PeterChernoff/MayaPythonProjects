import maya.cmds as mc


class pcCreateRigUtilities:
    @staticmethod
    def createCTRLs(s, size=3, prnt=False, ornt=False, pnt=False, orientVal=(1, 0, 0), colour=5, sectionsTU=None,
                    addPrefix=False, boxDimensionsLWH=None):
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
                ctrl = mc.curve(ctrlName, r=True, d=1, p=toPass, )
            except:
                ctrl = mc.curve(name=ctrlName, d=1, p=toPass, )
                # ctrl = mc.curve(name=ctrlName, p=toPass, d=1)
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
    def lockHideCtrls(s, translate=False, rotate=False, scale=False, theVals=[], toHide=False, visible=False,
                      toLock=True):
        # can be used to lock or unlock
        myVals = list(theVals)  # need to reset it every time
        if translate:
            myVals.extend(["tx", "ty", "tz"])
        if rotate:
            myVals.extend(["rx", "ry", "rz"])
        if scale:
            myVals.extend(["sx", "sy", "sz"])
        if visible:
            myVals.extend(["v"])

        for i in range(len(myVals)):
            mc.setAttr("{0}.{1}".format(s, myVals[i]), k=toHide, l=toLock)

    @staticmethod
    def setDriverDrivenValues(driver, driverAttribute, driven, drivenAttribute, driverValue, drivenValue,
                              modifyInOut=None, modifyBoth=None):
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
                                 dv=driverValue, v=drivenValue, itt=modifyIn, ott=modifyOut)
        else:
            mc.setDrivenKeyframe('{0}.{1}'.format(driven, drivenAttribute),
                                 cd='{0}.{1}'.format(driver, driverAttribute),
                                 dv=driverValue, v=drivenValue)

    @staticmethod
    def createLocatorToDelete(createLocator=True):
        # This is little more than a signal to tell me I need to undo what I've done
        if createLocator:
            toDelete = mc.spaceLocator(p=(0, 0, 0))[0]
            mc.setAttr('{0}.overrideEnabled'.format(toDelete), 1)
            mc.setAttr("{0}.overrideColor".format(toDelete), 13)

    @staticmethod
    def tgpSetGeo(geoJntArray, setter="JNT_", setLayer=False, *args):
        print(geoJntArray)

        for i in range(len(geoJntArray)):
            try:
                # print("------")
                theParent = geoJntArray[i]
                geoName = theParent.replace(setter, "GEO_")
                mc.parent(geoName, theParent)
                pivotTranslate = mc.xform(theParent, q=True, ws=True, rotatePivot=True)
                mc.makeIdentity(geoName, a=True, t=True, r=True, s=True)
                mc.xform(geoName, ws=True, pivots=pivotTranslate)
                if setLayer:
                    pcCreateRigUtilities.layerEdit([geoName], geoLayer=True, noRecurse=True)

            except:
                mc.warning("Geo for {0} not properly named or available".format(geoJntArray[i]))
                mc.warning("===========")

    @staticmethod
    def changeRotateOrder(rotateChangeList, getRotOrder, *args):

        for rotateChange in rotateChangeList:
            if (getRotOrder == "XYZ"):
                mc.setAttr(rotateChange + ".rotateOrder", 0)
            elif (getRotOrder == "YZX"):
                mc.setAttr(rotateChange + ".rotateOrder", 1)
            elif (getRotOrder == "ZXY"):
                mc.setAttr(rotateChange + ".rotateOrder", 2)
            elif (getRotOrder == "XZY"):
                mc.setAttr(rotateChange + ".rotateOrder", 3)
            elif (getRotOrder == "YXZ"):
                mc.setAttr(rotateChange + ".rotateOrder", 4)
            elif (getRotOrder == "ZYX"):
                mc.setAttr(rotateChange + ".rotateOrder", 5)

                # print ("Changed Rotate Order for {0} to {1}".format(rotateChange, getRotOrder))

    @staticmethod
    def checkLeftRight(isLeft, initVal, *args):
        if isLeft:
            leftRightCheck = "_l_"
            leftRightText = "left"
        else:
            leftRightCheck = "_r_"
            leftRightText = "right"

        if leftRightCheck not in initVal:
            mc.warning("Please select the {0} side".format(leftRightText))
            return False
        return True

    @staticmethod
    def layerEdit(objectsToLoad, ikLayer=False, fkLayer=False, ikdriveLayer=False, bndLayer=False, geoLayer=False,
                  layerVis=True, layerState=2, noRecurse=False, *args):
        if layerVis:
            visVal = 1
        else:
            visVal = 0
        # layerState
        # 0 = normal
        # 1 = template
        # 2 = reference
        if ikLayer:
            layerName = "jnt_IK_LYR"
        elif fkLayer:
            layerName = "jnt_FK_LYR"
        elif ikdriveLayer:
            layerName = "jnt_IKDrive_LYR"
        elif bndLayer:
            layerName = "jnt_bnd_LYR"
        elif geoLayer:
            layerName = "geo_LYR"

        # creates the layer if it doesn't already exist
        if not mc.objExists(layerName):
            mc.createDisplayLayer(n=layerName, e=True)
        # adds the objects to the layer
        mc.editDisplayLayerMembers(layerName, objectsToLoad, nr=noRecurse)
        # sets the layer to the state we want

        mc.setAttr("{0}.displayType".format(layerName), layerState)
        mc.setAttr("{0}.visibility".format(layerName), visVal)

    @staticmethod
    def checkObjectType(val, *args):
        sels = mc.listRelatives(val, children=True, shapes=True, f=True)
        if "transform" in mc.objectType(val) and sels != None:
            # if there are children, it's not just a transform
            return mc.objectType(sels[0])
        else:
            # has no shape children, so probably a transform or joint
            return mc.objectType(val)

    @staticmethod
    def createNail(s, isLeft, name=None, bodySize=3, headSize=1, colour=5, *args):
        selname = str(s)
        # creates a nail at the location
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
        ctrlName = "CTRL_" + name
        if not isLeft:
            bodySize = bodySize * -1
            headSize = headSize * -1
        toPass = [(0, 0, 0), (0, 0, bodySize), (0, headSize, bodySize + headSize), (0, 0, bodySize + 2 * headSize),
                  (0, -headSize, bodySize + headSize), (0, 0, bodySize)]
        try:
            ctrl = mc.curve(ctrlName, r=True, d=1, p=toPass, )
        except:
            ctrl = mc.curve(name=ctrlName, d=1, p=toPass, )
            # ctrl = mc.curve(name=ctrlName, p=toPass, d=1)

        mc.setAttr('{0}.overrideEnabled'.format(ctrlName), 1)
        mc.setAttr("{0}.overrideColor".format(ctrlName), colour)

        auto = mc.group(ctrl, n="AUTO_" + ctrl)
        offset = mc.group(auto, n="OFFSET_" + ctrl)

        mc.parentConstraint(s, offset, mo=0)
        mc.delete(mc.parentConstraint(s, offset))

        # parent the nail to the bone
        mc.parentConstraint(selname, ctrl, mo=0)

        offsetCtrl = [offset, ctrl, auto]
        return offsetCtrl
