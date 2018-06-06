import maya.cmds as mc

class pcCreateRigUtilities:
    clrBodyFK = 17
    clrBodyIK = 28
    clrBodyMain = 13
    clrLeftFK = [0, 0.75, 1]
    clrLeftIK = [0, 0.5, 1]

    clrRightFK = [1, 0.75, 0]
    clrRightIK = [1, 0.5, 0]

    clrSettings = [.75, 0.5, 1]

    clrHandCtrl = [0.65, 0.8, 0]

    valLeft = "l_"
    valRight = "r_"

    @staticmethod
    def setupCtrl(s, size=3, orientVal=(1, 0, 0), colourTU=5, sectionsTU=None,
                  addPrefix=False, boxDimensionsLWH=None, override=True, ):
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
        if override:
            if colourTU is not None:
                if isinstance(colourTU, int):
                    mc.setAttr("{0}.overrideColor".format(ctrlName), colourTU)
                else:
                    mc.setAttr("{0}.overrideColorRGB".format(ctrlName), colourTU[0], colourTU[1], colourTU[2])
                    mc.setAttr("{0}.overrideRGBColors".format(ctrlName), 1)
        return ctrl, ctrlName

    @staticmethod
    def createCTRLs(s, size=3, prnt=False, ornt=False, pnt=False, orientVal=(1, 0, 0), colourTU=5, sectionsTU=None,
                    addPrefix=False, boxDimensionsLWH=None, ):
        ctrl, ctrlName = pcCreateRigUtilities.setupCtrl(s, size, orientVal, colourTU, sectionsTU,
                                                        addPrefix, boxDimensionsLWH)

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
    def createCTRLsNoOffset(s, size=3, prnt=False, ornt=False, pnt=False, orientVal=(1, 0, 0), colourTU=5,
                            sectionsTU=None,
                            addPrefix=False, boxDimensionsLWH=None, ):

        ctrl, ctrlName = pcCreateRigUtilities.setupCtrl(s, size, orientVal, colourTU, sectionsTU,
                                                        addPrefix, boxDimensionsLWH)

        mc.parentConstraint(s, ctrl, mo=0)
        mc.delete(mc.parentConstraint(s, ctrl))
        mc.makeIdentity(ctrl, apply=True, t=True, r=True, s=True)

        # parent and orient/point are not inclusive
        if prnt:
            mc.parentConstraint(ctrl, s, mo=0)
        else:
            if ornt:
                mc.orientConstraint(ctrl, s, mo=0)
            if pnt:
                mc.pointConstraint(ctrl, s, mo=0)
        return ctrl

    @staticmethod
    def createCTRLsFKDirect(s, size=3, orientVal=(1, 0, 0), colourTU=5,
                            sectionsTU=None,
                            addPrefix=False, boxDimensionsLWH=None, override=True):

        ctrl, ctrlName = pcCreateRigUtilities.setupCtrl(s, size, orientVal, colourTU, sectionsTU,
                                                        addPrefix, boxDimensionsLWH, override=override)

        fkShape = mc.listRelatives(ctrl)[0]

        mc.parent(fkShape, s, s=True, r=True)
        mc.delete(ctrlName)
        mc.rename(s, ctrlName)

        try:
            if override:
                mc.setAttr('{0}.overrideEnabled'.format(ctrl), 1)
                mc.setAttr("{0}.overrideColor".format(ctrl), colourTU)
        except:
            mc.warning('{0}.overrideEnabled is locked'.format(ctrl))
        return ctrl, fkShape

    @staticmethod
    def lockHideCtrls(s, translate=False, rotate=False, scale=False, visibility=False, theVals=[], attrVisible=False,
                      toLock=True, channelBox=None):

        # can be used to lock or unlock
        myVals = list(theVals)  # need to reset it every time
        if translate:
            myVals.extend(["tx", "ty", "tz"])
        if rotate:
            myVals.extend(["rx", "ry", "rz"])
        if scale:
            myVals.extend(["sx", "sy", "sz"])
        if visibility:
            myVals.extend(["v"])

        for i in range(len(myVals)):
            mc.setAttr("{0}.{1}".format(s, myVals[i]), k=attrVisible, l=toLock)
            if channelBox is not None:
                mc.setAttr("{0}.{1}".format(s, myVals[i]), channelBox=channelBox)

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
            returnVal = mc.setDrivenKeyframe('{0}.{1}'.format(driven, drivenAttribute),
                                             cd='{0}.{1}'.format(driver, driverAttribute),
                                             dv=driverValue, v=drivenValue, itt=modifyIn, ott=modifyOut)
        else:
            returnVal = mc.setDrivenKeyframe('{0}.{1}'.format(driven, drivenAttribute),
                                             cd='{0}.{1}'.format(driver, driverAttribute),
                                             dv=driverValue, v=drivenValue)

    @staticmethod
    def createLocatorToDelete(createLocator=True):
        # This is little more than a signal to tell me I need to undo what I've done
        if createLocator:
            toDelete = mc.spaceLocator(n="deleteMe", p=(0, 0, 0))[0]
            mc.setAttr('{0}.overrideEnabled'.format(toDelete), 1)
            mc.setAttr("{0}.overrideColor".format(toDelete), 13)

    @staticmethod
    def tgpSetGeo(geoJntArray, setter="JNT_BND_", setLayer=False, printOut=False, *args):
        if printOut:
            print(geoJntArray)

        for i in range(len(geoJntArray)):
            try:
                if printOut:
                    print("Setting {0}".format(geoJntArray[i]))

                theParent = geoJntArray[i]

                geoName = theParent.replace(setter, "GEO_")
                if printOut:
                    print("geoName: {0}".format(geoName))
                mc.parent(geoName, theParent)
                if printOut:
                    print("Parenting complete")
                pivotTranslate = mc.xform(theParent, q=True, ws=True, rotatePivot=True)
                mc.makeIdentity(geoName, a=True, t=True, r=True, s=True)
                mc.xform(geoName, ws=True, pivots=pivotTranslate)
                if setLayer:
                    pcCreateRigUtilities.layerEdit(geoName, geoLayer=True, noRecurse=True)

                if printOut:
                    print("Pivot Complete")

            except:
                if printOut:
                    mc.warning("Geo for {0} not properly named or available".format(geoJntArray[i]))
                    mc.warning("===========")

    @staticmethod
    def tgpSetGeoManualStretch(geoJntArray, setter="JNT_BND_", setLayer=False, printOut=False, keyWord=None, *args):

        for i in range(len(geoJntArray)):
            try:
                if printOut:
                    print("^^^^^^")
                    print("Setting {0}".format(geoJntArray[i]))

                theParent = geoJntArray[i]

                if keyWord in geoJntArray[i]:
                    # if the keyword is in here, we need to get the bone parent
                    grandparent = mc.listRelatives(geoJntArray[i], type="joint", p=True)[0]
                    parents = mc.listRelatives(grandparent, type="joint")
                    theChild = [x for x in parents if keyWord not in x][0]

                else:
                    theChild = mc.listRelatives(geoJntArray[i], type="joint")[0]

                geoName = theParent.replace(setter, "GEO_")
                if printOut:
                    print("geoName: {0}".format(geoName))

                if printOut:
                    print("Parenting complete")
                pcCreateRigUtilities.tgpCreateStretchMultNode(theChild, geoName, theParent,
                                                              printOut, )
            except:
                if printOut:
                    mc.warning("Geo for {0} not properly named or available".format(geoJntArray[i]))
                    mc.warning("===========")

    @staticmethod
    def tgpCreateStretchMultNode(theChild, geoName, theParent,
                                 printOut, ):
        # takes the joint, the connects it to the geometry, and uses theChild for length

        rotateOrder = mc.getAttr("{0}.rotateOrder".format(theParent))
        mc.setAttr("{0}.rotateOrder".format(geoName), rotateOrder)

        mdLimbSetup = geoName
        mdLimb = "{0}_normalize_DIV".format(mdLimbSetup)
        if printOut:
            print("mdLimb: {0}".format(mdLimb))
        mc.shadingNode("multiplyDivide", n=mdLimb, au=True)
        mc.connectAttr("{0}.translateX".format(theChild), "{0}.input1X".format(mdLimb))
        getLen = mc.getAttr("{0}.translateX".format(theChild))
        mc.setAttr("{0}.input2X".format(mdLimb), getLen)

        mc.setAttr("{0}.operation".format(mdLimb), 2)  # set the operation to divide
        mc.connectAttr("{0}.outputX".format(mdLimb), "{0}.scaleX".format(geoName))

    @staticmethod
    def tgpSetGeoSpecial(geoJntArray, setter="JNT_BND_", setLayer=False, printOut=False, keyWord=None, stretch=False,
                         *args):
        if printOut:
            print(geoJntArray)

        for i in range(len(geoJntArray)):

            try:

                if printOut:
                    print("Setting {0}".format(geoJntArray[i]))
                # get the joint we will be working with
                theParent = geoJntArray[i]
                # get the immediate joint child we will be working with
                theChild = mc.listRelatives(geoJntArray[i], type="joint")[0]
                # get the name of the object we want
                geoName = theParent.replace(setter, "GEO_")
                geoNameSpecial = "{0}{1}".format(geoName, keyWord)
                listNames = mc.ls("{0}*".format(geoNameSpecial), type="transform")
                # listNames.append(geoName)
                if printOut:
                    print("geoName: {0}".format(geoName))
                # parent geometries of similar types under the joint (for when we have twist geos but no twist joints to go with them
                mc.parent(listNames, theParent)
                if printOut:
                    print("Parenting complete")
                pivotTranslate = mc.xform(theParent, q=True, ws=True, rotatePivot=True)

                if printOut:
                    print("pivotTranslate: {0}".format(pivotTranslate))

                if printOut:
                    print("Making Identity: {0}".format(geoName))

                if printOut:
                    print("make Identity complete")
                mc.xform(geoName, ws=True, pivots=pivotTranslate)
                mc.makeIdentity(geoName, a=True, t=True, r=True)  # the scale should be locked already at this point
                for j in range(len(listNames)):
                    print("listName[{0}]: {1}".format(j, listNames[j]))
                    mc.xform(listNames[j], ws=True, pivots=pivotTranslate)
                    mc.makeIdentity(listNames[j], a=True, t=True, r=True, s=True)
                    if stretch:
                        pcCreateRigUtilities.tgpCreateStretchMultNode(theChild, listNames[j], theParent,
                                                                      printOut)

                if setLayer:
                    pcCreateRigUtilities.layerEdit(listNames, geoLayer=True, noRecurse=True)

            except:
                if printOut:
                    mc.warning("Geo for {0} not properly named or available".format(geoJntArray[i]))
                    mc.warning("===========")

    @staticmethod
    def changeRotateOrder(rotateChangeList, getRotOrder, *args):

        if not isinstance(rotateChangeList, list):
            rotateChangeList = [rotateChangeList]

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
    def layerEdit(objectsToLoad, ikLayer=False, fkLayer=False, ikdriveLayer=False, bndLayer=False, bndAltLayer=False,
                  geoLayer=False,
                  bodyLayer=False, layerVis=True, layerState=0, noRecurse=False, colourTU=None, newLayerName=None,
                  printout=False,
                  *args):

        if not isinstance(objectsToLoad, list):
            objectsToLoad = [objectsToLoad]
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
        elif bodyLayer:
            layerName = "body_LYR"
        elif bndAltLayer:
            layerName = "jnt_bnd_extras_LYR"
        elif newLayerName is not None:
            layerName = newLayerName

        # creates the layer if it doesn't already exist
        if not mc.objExists(layerName):
            mc.createDisplayLayer(n=layerName, e=True)
        # adds the objects to the layer
        if printout:
            print("objectsToLoad: {0}".format(objectsToLoad))
        mc.editDisplayLayerMembers(layerName, objectsToLoad, nr=noRecurse)

        # sets the layer to the state we want
        mc.setAttr("{0}.displayType".format(layerName), layerState)
        mc.setAttr("{0}.visibility".format(layerName), visVal)
        '''
        0 None, 1 black, 2 dark grey, 3 light gray, 4 red
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
        if colourTU is not None:
            if isinstance(colourTU, int):
                mc.setAttr("{0}.color".format(layerName), colourTU)
            else:
                mc.setAttr("{0}.overrideColorRGB".format(layerName), colourTU[0], colourTU[1], colourTU[2])
                mc.setAttr("{0}.overrideRGBColors".format(layerName), 1)

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
    def createNail(s, isLeft, name=None, bodySize=3, headSize=1, colourTU=5, override=True, *args):
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
        if override:
            if colourTU is not None:
                if isinstance(colourTU, int):
                    mc.setAttr("{0}.overrideColor".format(ctrlName), colourTU)
                else:
                    mc.setAttr("{0}.overrideColorRGB".format(ctrlName), colourTU[0], colourTU[1], colourTU[2])
                    mc.setAttr("{0}.overrideRGBColors".format(ctrlName), 1)
                mc.setAttr("{0}.overrideColor".format(ctrlName), colourTU)

        auto = mc.group(ctrl, n="AUTO_" + ctrl)
        offset = mc.group(auto, n="OFFSET_" + ctrl)

        mc.parentConstraint(s, offset, mo=0)
        mc.delete(mc.parentConstraint(s, offset))

        # parent the nail to the bone
        mc.parentConstraint(selname, ctrl, mo=0)

        offsetCtrl = [offset, ctrl, auto]
        return offsetCtrl

    @staticmethod
    def createNailNoOffset(s, isLeft, name=None, bodySize=3, headSize=1, colourTU=5, prnt=True, pnt=False,
                           override=True,
                           *args):
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
        if isLeft:
            bodySize = bodySize * -1
            headSize = headSize * -1
        toPass = [(0, 0, 0), (0, 0, bodySize), (0, headSize, bodySize + headSize), (0, 0, bodySize + 2 * headSize),
                  (0, -headSize, bodySize + headSize), (0, 0, bodySize)]
        try:
            ctrl = mc.curve(ctrlName, r=True, d=1, p=toPass, )
        except:
            ctrl = mc.curve(name=ctrlName, d=1, p=toPass, )
            # ctrl = mc.curve(name=ctrlName, p=toPass, d=1)

        if override:
            mc.setAttr('{0}.overrideEnabled'.format(ctrlName), 1)
            if colourTU is not None:
                if isinstance(colourTU, int):
                    mc.setAttr("{0}.overrideColor".format(ctrlName), colourTU)
                else:
                    mc.setAttr("{0}.overrideColorRGB".format(ctrlName), colourTU[0], colourTU[1], colourTU[2])
                    mc.setAttr("{0}.overrideRGBColors".format(ctrlName), 1)

        if pnt:
            todelete = mc.pointConstraint(s, ctrl)
            mc.delete(todelete)
        elif prnt:
            todelete = mc.parentConstraint(s, ctrl)
            mc.delete(todelete)
        # parent the nail to the bone

        mc.parentConstraint(selname, ctrl, mo=True)

        return ctrl

    @staticmethod
    def makeLimbSwitch(ctrlLimb, locLimbFollowArray, listParents, enumName, enumVals, colourTU, override=True, *args):

        # get the auto_ctrl of the limb
        autoCtrlLimb = mc.listRelatives(ctrlLimb, p=True, c=False)[0]

        for i in range(len(locLimbFollowArray)):
            # creates locator, then moves to upperArm FK control
            locName = locLimbFollowArray[i]

            mc.spaceLocator(p=(0, 0, 0), name=locName)
            locShape = mc.listRelatives(locName, s=True)[0]

            mc.setAttr("{0}.localScaleX".format(locShape), 15)

            mc.setAttr("{0}.localScaleY".format(locShape), 15)
            mc.setAttr("{0}.localScaleZ".format(locShape), 15)

            if override:
                mc.setAttr('{0}.overrideEnabled'.format(locName), 1)

                if colourTU is not None:
                    if isinstance(colourTU, int):
                        mc.setAttr("{0}.overrideColor".format(locName), colourTU)
                    else:
                        mc.setAttr("{0}.overrideColorRGB".format(locName), colourTU[0], colourTU[1], colourTU[2])
                        mc.setAttr("{0}.overrideRGBColors".format(locName), 1)

            toDelete = mc.parentConstraint(ctrlLimb, locName)[0]
            mc.delete(toDelete)
            mc.parent(locName, listParents[i])

        mc.addAttr(ctrlLimb, longName=enumName, at="enum", k=True, en=enumVals)
        # create oreient constraints for the arm locators
        limbFollowOrntConstr = mc.orientConstraint(locLimbFollowArray, autoCtrlLimb, mo=True)[0]

        limbSpaceFollow = mc.listAttr(limbFollowOrntConstr)[-4:]
        for i in range(len(limbSpaceFollow)):
            # set the driven key to 1 and the undriven keys to 0

            pcCreateRigUtilities.setDriverDrivenValues(ctrlLimb, enumName, limbFollowOrntConstr, limbSpaceFollow[i], i,
                                                       1)
            for i2 in range(len(limbSpaceFollow)):
                if i2 != i:
                    # need to have the second to last value be i, not i2
                    pcCreateRigUtilities.setDriverDrivenValues(ctrlLimb, enumName, limbFollowOrntConstr,
                                                               limbSpaceFollow[i2], i, 0)

        for i in range(len(locLimbFollowArray)):
            mc.setAttr("{0}.visibility".format(locLimbFollowArray[i]), False)
            pcCreateRigUtilities.lockHideCtrls(locLimbFollowArray[i], scale=True, visibility=True)

    @staticmethod
    def makeLimbSwitchNoAutoLocsInPosition(ctrlLimb, locLimbFollowArray, limbFollowOrntConstr, enumVals, enumName,
                                           *args):
        num = len(enumVals.split(":"))

        alreadySet = mc.attributeQuery(enumName, node=ctrlLimb, ex=True)
        if not alreadySet:
            # If we've already set this, we can skip this step
            mc.addAttr(ctrlLimb, longName=enumName, at="enum", k=True, en=enumVals)

        # get the values for the orient
        negNum = -1 * num
        limbSpaceFollow = mc.listAttr(limbFollowOrntConstr)[negNum:]
        for i in range(len(limbSpaceFollow)):
            # set the driven key to 1 and the undriven keys to 0

            pcCreateRigUtilities.setDriverDrivenValues(ctrlLimb, enumName, limbFollowOrntConstr, limbSpaceFollow[i], i,
                                                       1)
            for i2 in range(len(limbSpaceFollow)):
                if i2 != i:
                    # need to have the second to last value be i, not i2
                    pcCreateRigUtilities.setDriverDrivenValues(ctrlLimb, enumName, limbFollowOrntConstr,
                                                               limbSpaceFollow[i2], i, 0)
        if not alreadySet:
            for i in range(len(locLimbFollowArray)):
                mc.setAttr("{0}.visibility".format(locLimbFollowArray[i]), False)
                pcCreateRigUtilities.lockHideCtrls(locLimbFollowArray[i], scale=True, visibility=True)

    @staticmethod
    def createParentGroup(objToGrp, grpName, point=False, orient=False, parent=False):
        mc.group(n=grpName, em=True, w=True)
        if parent:
            todelete = mc.parentConstraint(objToGrp, grpName)
            mc.delete(todelete)
        else:
            if point:
                todelete = mc.pointConstraint(objToGrp, grpName)
                mc.delete(todelete)
            if orient:
                todelete = mc.orientConstraint(objToGrp, grpName)
                mc.delete(todelete)
        parentObj = mc.listRelatives(objToGrp, p=True)
        if parentObj is not None:
            # if there is a parent, do something
            mc.parent(grpName, parentObj[0])

        mc.parent(objToGrp, grpName)

    @staticmethod
    def makeBlendBasic(jntsSrc1, jntsSrc2, jntsTgt, ctrl, ctrlAttr, rotate, translate, override=False, *args):

        blndNodeTrans = []
        blndNodeRot = []
        # colour2 is at 0, colour1 is at 1

        for i in range(len(jntsSrc1)):
            name = jntsTgt[i]
            if translate:
                val = ".translate"
                blndNodeTrans.append(mc.shadingNode("blendColors", au=True, name="{0}_trans_BCN###".format(name)))
                mc.connectAttr(jntsSrc1[i] + val + "X", blndNodeTrans[i] + ".color2R")
                mc.connectAttr(jntsSrc1[i] + val + "Y", blndNodeTrans[i] + ".color2G")
                mc.connectAttr(jntsSrc1[i] + val + "Z", blndNodeTrans[i] + ".color2B")

                mc.connectAttr(jntsSrc2[i] + val + "X", blndNodeTrans[i] + ".color1R")
                mc.connectAttr(jntsSrc2[i] + val + "Y", blndNodeTrans[i] + ".color1G")
                mc.connectAttr(jntsSrc2[i] + val + "Z", blndNodeTrans[i] + ".color1B")

                mc.connectAttr(blndNodeTrans[i] + ".outputR", jntsTgt[i] + "{0}".format(val + "X"))
                mc.connectAttr(blndNodeTrans[i] + ".outputG", jntsTgt[i] + "{0}".format(val + "Y"))
                mc.connectAttr(blndNodeTrans[i] + ".outputB", jntsTgt[i] + "{0}".format(val + "Z"))
                blndName = "{0}.{1}".format(ctrl, ctrlAttr)
                mc.connectAttr(blndName, blndNodeTrans[i] + ".blender", f=True)

            if rotate:
                val = ".rotate"
                blndNodeRot.append(mc.shadingNode("blendColors", au=True, name="{0}_rot_BCN###".format(name)))

                mc.connectAttr(jntsSrc1[i] + val + "X", blndNodeRot[i] + ".color2R")
                mc.connectAttr(jntsSrc1[i] + val + "Y", blndNodeRot[i] + ".color2G")
                mc.connectAttr(jntsSrc1[i] + val + "Z", blndNodeRot[i] + ".color2B")

                mc.connectAttr(jntsSrc2[i] + val + "X", blndNodeRot[i] + ".color1R")
                mc.connectAttr(jntsSrc2[i] + val + "Y", blndNodeRot[i] + ".color1G")
                mc.connectAttr(jntsSrc2[i] + val + "Z", blndNodeRot[i] + ".color1B")

                '''mc.connectAttr(jntsSrc1[i] + val, blndNodeRot[i] + ".color2")
                mc.connectAttr(jntsSrc2[i] + val, blndNodeRot[i] + ".color1")'''

                mc.connectAttr(blndNodeRot[i] + ".outputR", jntsTgt[i] + "{0}".format(val + "X"))
                mc.connectAttr(blndNodeRot[i] + ".outputG", jntsTgt[i] + "{0}".format(val + "Y"))
                mc.connectAttr(blndNodeRot[i] + ".outputB", jntsTgt[i] + "{0}".format(val + "Z"))
                blndName = "{0}.{1}".format(ctrl, ctrlAttr)
                mc.connectAttr(blndName, blndNodeRot[i] + ".blender", f=True)

        return

    @staticmethod
    def createDistanceDimensionNode(startLoc, endLoc, lenNodeName, toHide=False):

        distDimShape = mc.distanceDimension(sp=(0, 0, 0), ep=(0, 0, 0))
        mc.connectAttr("{0}.worldPosition".format(startLoc), "{0}.startPoint".format(distDimShape), f=True)
        mc.connectAttr("{0}.worldPosition".format(endLoc), "{0}.endPoint".format(distDimShape), f=True)
        distDimParent = mc.listRelatives(distDimShape, p=True)
        mc.rename(distDimParent, lenNodeName)
        lenNodeNameShape = mc.listRelatives(lenNodeName, s=True)[0]
        if toHide:
            mc.setAttr("{0}.visibility".format(startLoc), False)
            mc.setAttr("{0}.visibility".format(endLoc), False)
            mc.setAttr("{0}.visibility".format(lenNodeName), False)
        return lenNodeNameShape

    @staticmethod
    def constrainMove(driver, driven, point=False, orient=False, parent=False):
        if not point and not orient and not parent:
            mc.error("Remember to include a point/orient/parent")
        if point:
            toDelete = mc.pointConstraint(driver, driven)
            mc.delete(toDelete)
        if orient:
            toDelete = mc.orientConstraint(driver, driven)
            mc.delete(toDelete)
        if parent:
            toDelete = mc.parentConstraint(driver, driven)
            mc.delete(toDelete)

    @staticmethod
    def getDistance(startObj, endObj):

        startLoc = "toDeleteStart"
        endLoc = "toDeleteEnd"

        mc.spaceLocator(n=startLoc, p=(0, 0, 0))
        mc.spaceLocator(n=endLoc, p=(0, 0, 0))

        mc.matchTransform(startLoc, startObj, pos=True)
        mc.matchTransform(endLoc, endObj, pos=True)

        lenNodeName = "toDelete"
        distDimShape = mc.distanceDimension(sp=(0, 0, 0), ep=(0, 0, 0))
        mc.connectAttr("{0}.worldPosition".format(startLoc), "{0}.startPoint".format(distDimShape), f=True)
        mc.connectAttr("{0}.worldPosition".format(endLoc), "{0}.endPoint".format(distDimShape), f=True)
        distDimParent = mc.listRelatives(distDimShape, p=True)
        mc.rename(distDimParent, lenNodeName)
        lenNodeNameShape = mc.listRelatives(lenNodeName, s=True)[0]
        dist = mc.getAttr("{0}.distance".format(lenNodeNameShape))
        mc.delete(lenNodeName, startLoc, endLoc)
        return dist

    @staticmethod
    def createIKVal(ikStartJoint, ikEndJoint, leftRight, ikSuffix, ikSolver, *args):
        ikSide = leftRight + ikSuffix

        ikHdlName = "HDL_" + ikSide
        effName = "EFF_" + ikSide
        ikVals = mc.ikHandle(n=ikHdlName, sj=ikStartJoint, ee=ikEndJoint, sol=ikSolver)
        mc.rename(ikVals[1], effName)
        ikVals[1] = effName

        # we are going to hide this eventually anyways
        mc.setAttr("{0}.v".format(ikHdlName), False)
        mc.setAttr("{0}.v".format(effName), False)

        return ikVals

    @staticmethod
    def setVisibility(driver, driverAttr, driven, drivenAttr, visMin, tangentToUse, val1, val2, val3, *args):
        # set the FK to visible when not ctrlFKIK not 1 for arm attribute
        pcCreateRigUtilities.setDriverDrivenValues(driver, driverAttr, driven, drivenAttr, drivenValue=val1,
                                                   driverValue=0, modifyInOut=tangentToUse)
        pcCreateRigUtilities.setDriverDrivenValues(driver, driverAttr, driven, drivenAttr, drivenValue=val2,
                                                   driverValue=1 - visMin, modifyInOut=tangentToUse)
        pcCreateRigUtilities.setDriverDrivenValues(driver, driverAttr, driven, drivenAttr, drivenValue=val3,
                                                   driverValue=1, modifyInOut=tangentToUse)

    @staticmethod
    def checkSymmetry(*args):
        # checks if symmetry is on
        symmetry = mc.symmetricModelling(query=True, symmetry=True)
        if symmetry != 0:
            mc.symmetricModelling(symmetry=0)
        return symmetry


    @staticmethod
    def tgpGetJnts(selName, loadBtn, objectType, objectDesc, keywords, objectNickname=None, ):
        if objectNickname is None:
            objectNickname = objectType

        if pcCreateRigUtilities.checkObjectType(selName) != objectType:
            mc.warning("{0} should be a {1}".format(objectDesc, objectNickname))
            return

        if not all(word.lower() in selName.lower() for word in keywords):
            mc.warning("That is the wrong {0}. Select the {1}".format(objectNickname, objectDesc))
            return

        if loadBtn is not None:
            mc.textFieldButtonGrp(loadBtn, e=True, tx=selName)

        # get the children joints
        parent = selName
        child = mc.listRelatives(selName, ad=True, type="joint")
        # collect the joints in an array
        jointArray = [parent]
        # reverse the order of the children joints
        child.reverse()

        # add to the current list
        jointArray.extend(child)

        return jointArray

    @staticmethod
    def tgpGetTx(selName, loadBtn, objectType, objectDesc, keywords, objectNickname=None, ):

        if pcCreateRigUtilities.checkObjectType(selName) != objectType:
            mc.warning("{0} should be a {1}".format(objectDesc, objectNickname))
            return

        if not all(word.lower() in selName.lower() for word in keywords):
            mc.warning("That is the wrong {0}. Select the {1}".format(objectNickname, objectDesc))
            return
        mc.textFieldButtonGrp(loadBtn, e=True, tx=selName)
        return selName

    @staticmethod
    def tgpLoadTxBtn(loadBtn, objectType, objectDesc, keywords, objectNickname=None):
        if objectNickname is None:
            objectNickname = objectType

        selLoad = []
        selLoad = mc.ls(sl=True, fl=True, type="transform")

        if (len(selLoad) != 1):
            mc.warning("Select only the {0}".format(objectDesc))
            return
        else:
            if pcCreateRigUtilities.checkObjectType(selLoad[0]) != objectType:
                mc.warning("{0} should be a {1}".format(objectDesc, objectNickname))
                return
            selName = selLoad[0]

            selName = pcCreateRigUtilities.tgpGetTx(selName, loadBtn, objectType, objectDesc, keywords, objectNickname)

            return selName

    @staticmethod
    def tgpLoadJntsBtn(loadBtn, objectType, objectDesc, keywords, objectNickname=None):
        if objectNickname is None:
            objectNickname = objectType
        # hierarchy
        selLoad = []
        selLoad = mc.ls(sl=True, fl=True, type=objectType)
        if (len(selLoad) != 1):
            mc.warning("Select only the {0}".format(objectDesc))
            return
        else:

            selName = selLoad[0]

            returner = pcCreateRigUtilities.tgpGetJnts(selName, loadBtn, objectType, objectDesc, keywords, objectNickname)

            if returner is None:
                return None

        return returner

    @staticmethod
    def tgpGetLocs(selName, loadBtn, objectType, objectDesc, keywords, objectNickname=None, ):
        if objectNickname is None:
            objectNickname = objectType

        if pcCreateRigUtilities.checkObjectType(selName) != objectType:
            mc.warning("{0} should be a {1}".format(objectDesc, objectNickname))
            return

        if not all(word.lower() in selName.lower() for word in keywords):
            mc.warning("That is the wrong {0}. Select the {1}".format(objectNickname, objectDesc))
            return
        if loadBtn is not None:
            mc.textFieldButtonGrp(loadBtn, e=True, tx=selName)

        # get the children joints
        parent = selName
        child = mc.listRelatives(selName, ad=True, type="transform")
        # collect the joints in an array
        locArray = [parent]
        # reverse the order of the children joints
        child.reverse()

        # add to the current list
        locArray.extend(child)
        locArraySorted = []
        for i in range(len(locArray)):
            sels = mc.listRelatives(locArray[i], c=True, s=True)
            if objectType in mc.objectType(sels) or objectType == mc.objectType(sels):
                locArraySorted.append(locArray[i])

        locRoot = selName
        locArray = locArraySorted
        return locArray

    @staticmethod
    def tgpLoadLocsBtn(loadBtn, objectType, objectDesc, keywords, objectNickname=None):
        if objectNickname is None:
            objectNickname = objectType
        # hierarchy
        selLoad = []
        selLoad = mc.ls(sl=True, fl=True, type="transform")

        if (len(selLoad) != 1):
            mc.warning("Select only the {0}".format(objectDesc))
            return
        else:
            selName = selLoad[0]
            # get the children joints
            returner = pcCreateRigUtilities.tgpGetLocs(selName, loadBtn, objectType, objectDesc, keywords, objectNickname)
            if returner is None:
                return None

        return returner