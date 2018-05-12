import maya.cmds as mc


class pcCreateRigAltFKIKSwitching():
    def __init__(self):
        self.window = "bcWindow"
        self.title = "pcRigHands"
        self.winSize = (500, 100)

        self.createUI()

    def arm_FKtoResult(self, leftRight, *args):
        # left FK to IK
        default_upperArm_length = mc.getAttr(
            "{0}upperArm_normalize_DIV.input2X".format(leftRight))  # default_upperArm_length = 23.508
        default_lowerArm_length = mc.getAttr(
            "{0}lowerArm_normalize_DIV.input2X".format(leftRight))  # default_upperArm_length = 27.351
        # current values
        curr_upperArm_length = mc.getAttr("JNT_BND_{0}lowerArm.translateX".format(leftRight))
        curr_lowerArm_length = mc.getAttr("JNT_BND_{0}hand.translateX".format(leftRight))

        upperArm_length_factor = curr_upperArm_length / default_upperArm_length
        lowerArm_length_factor = curr_lowerArm_length / default_lowerArm_length

        mc.setAttr("CTRL_FK_{0}upperArm.length".format(leftRight), upperArm_length_factor)
        mc.setAttr("CTRL_FK_{0}lowerArm.length".format(leftRight), lowerArm_length_factor)

        mc.setAttr("{0}.rotate".format("CTRL_gimbalCorr_{0}arm".format(leftRight)), 0, 0, 0)

        mc.matchTransform("CTRL_FK_{0}upperArm".format(leftRight), "JNT_FKsnap_{0}upperArm".format(leftRight), rot=True)
        mc.matchTransform("CTRL_FK_{0}lowerArm".format(leftRight), "JNT_FKsnap_{0}lowerArm".format(leftRight), rot=True)
        mc.matchTransform("CTRL_FK_{0}hand".format(leftRight), "JNT_FKsnap_{0}hand".format(leftRight), rot=True)
        mc.setAttr("CTRL_settings_{0}arm.fkik_blend".format(leftRight),
                   0)  # now that we have the FK in place, we want to switch to it

    def arm_IKtoResult(self, forearm_mode, leftRight, *args):
        # IK to FK
        default_upperArm_length = mc.getAttr(
            "{0}upperArm_normalize_DIV.input2X".format(leftRight))  # default_upperArm_length = 23.508
        default_lowerArm_length = mc.getAttr(
            "{0}lowerArm_normalize_DIV.input2X".format(leftRight))  # default_upperArm_length = 27.351
        # current values
        curr_upperArm_length = mc.getAttr("JNT_BND_{0}lowerArm.translateX".format(leftRight))
        curr_lowerArm_length = mc.getAttr("JNT_BND_{0}hand.translateX".format(leftRight))

        tolerance = 0.001

        if forearm_mode == 1:

            if ((abs(curr_upperArm_length - default_upperArm_length) > tolerance) or (
                    abs(curr_lowerArm_length - default_lowerArm_length) > tolerance)):
                mc.setAttr("CTRL_{0}elbow.elbowSnap".format(leftRight), 1)
                mc.setAttr("CTRL_settings_{0}arm.IK_stretch".format(leftRight), 0)

            mc.matchTransform("CTRL_{0}arm".format(leftRight), "GRP_IKsnap_{0}arm".format(leftRight), rotation=True)
            mc.matchTransform("CTRL_{0}arm".format(leftRight), "GRP_IKsnap_{0}arm".format(leftRight), position=True)
            mc.matchTransform("CTRL_{0}elbow".format(leftRight), "JNT_BND_{0}lowerArm".format(leftRight), position=True)

            mc.setAttr("CTRL_{0}elbow.FKIK_lowerArmBlend".format(leftRight), 1)

        else:  # if forearm 2/IK FKelbow is selected
            lowerArm_length_factor = abs(curr_lowerArm_length / default_lowerArm_length)

            mc.matchTransform("CTRL_{0}elbow".format(leftRight), "JNT_BND_{0}lowerArm".format(leftRight), position=True)
            mc.matchTransform("CTRL_FK_{0}lowerArmElbow".format(leftRight), "JNT_BND_{0}lowerArm".format(leftRight),
                              rotation=True)
            mc.matchTransform("CTRL_FK_{0}handElbow".format(leftRight), "JNT_FKsnap_{0}hand".format(leftRight),
                              rotation=True)

            mc.setAttr("CTRL_{0}elbow.elbowSnap".format(leftRight), 1)
            mc.setAttr("CTRL_{0}elbow.FKIK_lowerArmBlend".format(leftRight), 0)

            mc.setAttr("CTRL_FK_{0}lowerArmElbow.length".format(leftRight), lowerArm_length_factor)

        mc.setAttr("CTRL_settings_{0}arm.fkik_blend".format(leftRight),
                   1)  # now that we have the FIK in place, we want to switch to it

    def leg_FKtoResult(self, leftRight, *args):
        # FK to IK
        try:
            default_upperLeg_length = mc.getAttr(
                "GEO_{0}upperLeg_normalize_DIV.input2X".format(leftRight))  # default_upperLeg_length = 31.855
        except:
            default_upperLeg_length = 31.855
        try:
            default_lowerLeg_length = mc.getAttr(
                "GEO_{0}lowerLeg_normalize_DIV.input2X".format(leftRight))  # default_lowerLeg_length = 44.037
        except:
            default_lowerLeg_length = 44.037

        # current values
        curr_upperLeg_length = mc.getAttr("JNT_BND_{0}lowerLeg.translateX".format(leftRight))
        curr_lowerLeg_length = mc.getAttr("JNT_BND_{0}legEnd.translateX".format(leftRight))

        upperLeg_length_factor = curr_upperLeg_length / default_upperLeg_length
        lowerLeg_length_factor = curr_lowerLeg_length / default_lowerLeg_length

        mc.setAttr("CTRL_FK_{0}upperLeg.length".format(leftRight), upperLeg_length_factor)
        mc.setAttr("CTRL_FK_{0}lowerLeg.length".format(leftRight), lowerLeg_length_factor)

        mc.matchTransform("CTRL_FK_{0}upperLeg".format(leftRight), "JNT_FKsnap_{0}upperLeg".format(leftRight), rot=True)
        mc.matchTransform("CTRL_FK_{0}lowerLeg".format(leftRight), "JNT_FKsnap_{0}lowerLeg".format(leftRight), rot=True)
        mc.matchTransform("JNT_FK_{0}legEnd".format(leftRight), "JNT_FKsnap_{0}legEnd".format(leftRight), rot=True)
        mc.matchTransform("CTRL_FK_{0}ankleTwist".format(leftRight), "JNT_FKsnap_{0}ankleTwist".format(leftRight),
                          rot=True)

        # mc.matchTransform("JNT_FK_{0}foot".format(leftRight), "JNT_FKsnap_{0}foot".format(leftRight), rot=True) # we do NOT snap this one
        mc.matchTransform("CTRL_FK_{0}ball".format(leftRight), "JNT_FKsnap_{0}ball".format(leftRight), rot=True)
        mc.setAttr("CTRL_settings_{0}leg.fkik_blend".format(leftRight),
                   0)  # now that we have the FK in place, we want to switch to it

    def leg_IKtoResult(self, leftRight, lowerLegMode, *args):

        # IK to FK
        try:
            default_upperLeg_length = mc.getAttr(
                "GEO_{0}upperLeg_normalize_DIV.input2X".format(leftRight))  # default_upperLeg_length = 31.855
        except:
            default_upperLeg_length = 31.855
        try:
            default_lowerLeg_length = mc.getAttr(
                "GEO_{0}lowerLeg_normalize_DIV.input2X".format(leftRight))  # default_lowerLeg_length = 44.037
        except:
            default_lowerLeg_length = 44.037

        # current values
        curr_upperLeg_length = mc.getAttr("JNT_BND_{0}lowerLeg.translateX".format(leftRight))
        curr_lowerLeg_length = mc.getAttr("JNT_BND_{0}legEnd.translateX".format(leftRight))

        tolerance = 0.01

        if ((abs(curr_upperLeg_length - default_upperLeg_length) > tolerance) or (
                abs(curr_lowerLeg_length - default_lowerLeg_length) > tolerance)):
            mc.setAttr("CTRL_{0}knee.kneeSnap".format(leftRight), 1)
            mc.setAttr("CTRL_settings_{0}leg.IK_stretch".format(leftRight), 0)

        mc.matchTransform("CTRL_{0}foot".format(leftRight), "GRP_IKsnap_{0}foot".format(leftRight), rotation=True)
        mc.matchTransform("CTRL_{0}foot".format(leftRight), "GRP_IKsnap_{0}foot".format(leftRight), position=True)

        # match the toe
        toeVal = mc.getAttr("JNT_BND_{0}ball.rotateY".format(leftRight))
        mc.setAttr("CTRL_{0}foot.toeWiggle".format(leftRight), toeVal)

        if lowerLegMode == 2:
            mc.matchTransform("CTRL_{0}knee".format(leftRight), "JNT_BND_{0}lowerLeg".format(leftRight), position=True)
            mc.setAttr("CTRL_{0}foot.autoManualKneeBlend".format(leftRight), 1)  # set the knee to manual
        else:
            leg_length_factor = mc.getAttr(
                "JNT_IK_noFlip_{0}lowerLeg_translateX.output".format(leftRight)) / default_upperLeg_length
            upperLeg_length_factor = curr_upperLeg_length / (
                    default_upperLeg_length * leg_length_factor)  # get the current thigh length. This will get us a normal sized leg
            lowerLeg_length_factor = curr_lowerLeg_length / (
                    default_lowerLeg_length * leg_length_factor)  # get the current shin length. This will get us a normal sized leg

            # We have set the leg length
            mc.setAttr("CTRL_{0}foot.autoKneeUpperLegLength".format(leftRight), upperLeg_length_factor)
            mc.setAttr("CTRL_{0}foot.autoKneeLowerLegLength".format(leftRight), lowerLeg_length_factor)

            mc.setAttr("CTRL_{0}foot.kneeTwist".format(leftRight), 0)

            noFlipLowerLegPos = mc.xform("JNT_IK_noFlip_{0}lowerLeg".format(leftRight), q=True, ws=True, t=True)
            bndLowerLegPos = mc.xform("JNT_BND_{0}lowerLeg".format(leftRight), q=True, ws=True, t=True)
            # we are creating a common origin around which to measure our angles
            center_shin_pos = mc.xform("JNT_IK_noFlip_{0}legEnd".format(leftRight), q=True, ws=True, t=True)
            # once we have an origin and two points in space, we need to find actual vectors that move from that origin to each point

            # we can do this by assigning a pair of variables between the noFlip shin position in position and center point shin position
            centerToNoFlip = []
            centerToBND = []
            for i in range(len(noFlipLowerLegPos)):
                # getting the difference
                addVal = noFlipLowerLegPos[i] - center_shin_pos[i]
                centerToNoFlip.append(addVal)
                addVal2 = bndLowerLegPos[i] - center_shin_pos[i]
                centerToBND.append(addVal2)
            # now we can use the angleBetween command to find the angle between them.
            # We'll use the -v1 and -v2 flags to assign our centerTo result and centerToNoFlip vectors

            deltaAngle = mc.angleBetween(v1=centerToNoFlip, v2=centerToBND)
            # the angleBetween command stores 4 values, the first three represent the axis on which the angle is
            # measured, while the last represents the angle itself
            # we don't need to be concerned too much on the axis, because the other angles we'll compare it to
            # will be on the same axis, we just want the angle itself

            # now we have an axis on which to compare this to
            sourceNode = "JNT_IK_noFlip_{0}lowerLeg".format(leftRight)
            driverAttr = "CTRL_{0}foot.kneeTwist".format(leftRight)
            # start at 90 degrees at 0ths try
            # print("deltaAngle: \t{0}".format(deltaAngle))
            # self.iterateToMatchRecursive(sourceNode, center_shin_pos, driverAttr, centerToNoFlip, deltaAngle[3], 90, 0)
            maxCount = 5000
            kneeTwistValue = 180.0  # we need this to be a float
            maxVal = 360.0  # we need this to be a float
            minVal = 0  # we need this to be a float
            repeat = True
            for i in range(maxCount):
                print("attempt #: {0}".format(i))
                # python doesn't really like recursion
                if repeat:
                    kneeTwistValue, repeat, minVal, maxVal  = self.iterToMatchSeq(sourceNode, center_shin_pos, driverAttr, centerToNoFlip,
                                                        deltaAngle[3], kneeTwistValue, maxVal, minVal)
                else:
                    print("value found")
                    break

            if repeat:
                print("Sequence failed")

            shinIK = "JNT_IK_noFlip_{0}lowerLeg".format(leftRight)
            curr_shin_pos = mc.xform(shinIK, q=True, ws=True, t=True)

            tolerance = 0.1
            print("kneeTwist: {0}".format(kneeTwistValue))
            if ((abs(curr_shin_pos[0] - bndLowerLegPos[0]) > tolerance) or
                    (abs(curr_shin_pos[1] - bndLowerLegPos[1]) > tolerance) or
                    (abs(curr_shin_pos[2] - bndLowerLegPos[2]) > tolerance)):
                kneeTwistValue = kneeTwistValue*-1
                mc.setAttr(driverAttr, kneeTwistValue)
                print("new kneeTwist: {0}".format(kneeTwistValue))
            print("centerToNoFlip: {0}".format(centerToNoFlip))

            mc.setAttr("CTRL_{0}foot.autoManualKneeBlend".format(leftRight), 0)  # set the knee to manual

        mc.setAttr("CTRL_settings_{0}leg.fkik_blend".format(leftRight),
                   1)  # now that we have the FIK in place, we want to switch to it

    def iterToMatchSeq(self, sourceNode, centerPos, driverAttr, zeroVector, targetAngle, value, maxVal, minVal, altMode = False):
        # source node is JNT_IK_noFlip_l_lowerLeg
        # next we need the center position
        # after that, we need the driveAttr (kneeTwist)
        # the zeroVector is our default position
        # lastly, we need the targetAngle to know the match
        # value is the iteration
        # count is how many times we've done this

        # this will return a float
        mc.setAttr("{0}".format(driverAttr), value)
        print("-----")

        # we then need to calculate the vector form the noFlip shin's current position to the center point, so we can its value
        curr_pos = mc.xform(sourceNode, q=True, ws=True, translation=True)
        # subtract the zeroPosVector from it
        centerToCurr = [curr_pos[0] - centerPos[0], curr_pos[1] - centerPos[1], curr_pos[2] - centerPos[2], ]
        currAngle = mc.angleBetween(v1=centerToCurr, v2=zeroVector)
        # now we have an angle to compare with and an angle to compare to
        # however, we are dealing with precision values
        # we'll have a tolerance value instead
        tolerance = 0.01

        print("targetAngle: {0}".format(targetAngle))
        print("currAngle: {0}".format(currAngle))
        print("value: {0}".format(value))
        print("maxVal: {0}".format(maxVal))
        print("minVal: {0}".format(minVal))
        # we return success but we don't want to keep goin if we keep failing as to avoid a system crash
        if (abs(currAngle[3] - targetAngle) < tolerance):
            return value, False, minVal, maxVal,
        else:
            # if we haven't found the angle, we need to compare the current value to the target value
            if currAngle[3] > targetAngle:
                # if the angle is greater, we need to decrement the knee value by half the value we previously tried
                # I am making some adjustments to make this less bouncy
                if altMode:

                    value = value - value / 2;
                else:
                    minVal = value # the min value is at least the current value
                    value = (maxVal + value)/2 # get the average of the max value and the current value

            else:
                # if we are coming in under our target angle, then we increase it by half the previous value

                if altMode:

                    value = value + value / 2;
                else:
                    # I am making some adjustments to make this less bouncy
                    maxVal = value # the min value is at least the current value
                    value = (minVal + value)/2 # get the average of the max value and the current value
            # use recursion
            value = value % 360
            return value, True, minVal, maxVal # adjust

    def createUI(self):
        if mc.window("matchApp", exists=True):
            mc.deleteUI("matchApp", window=True)

        mc.window("matchApp", widthHeight=self.winSize, sizeable=True, menuBar=True,
                  mnb=True, mxb=False)

        mc.frameLayout(l="IK/FK Matching")

        mc.columnLayout(w=self.winSize[0])

        mc.text(align="center", l="Go to matching...")
        mc.separator(horizontal=True)

        mc.rowColumnLayout(numberOfColumns=2, w=self.winSize[0])

        mc.button(l="Left Arm FK to Arm BND", c=self.callLButtonArmFK)
        mc.button(l="Right Arm FK to Arm BND", c=self.callRButtonArmFK)

        mc.rowColumnLayout(numberOfColumns=2)
        mc.button(l="Left Arm IK to ArmBND", c=self.callLButtonArmIK)  # Match left IK arm to result arm
        mc.radioButtonGrp("leftForeArmMode", vr=True, numberOfRadioButtons=2, labelArray2=["IK forearm", "FK forearm"],
                          select=1)
        mc.setParent("..")

        mc.rowColumnLayout(numberOfColumns=2)
        mc.button(l="Right Arm IK to Arm BND", c=self.callRButtonArmIK)  # Match left IK arm to result arm
        mc.radioButtonGrp("rightForeArmMode", vr=True, numberOfRadioButtons=2, labelArray2=["IK forearm", "FK forearm"],
                          select=1)
        mc.setParent("..")

        # mc.separator(st="in", h=17, w=self.winSize[0])
        mc.button(l="Left FK Leg to BND Leg", c=self.callLButtonLegFK)
        mc.button(l="Right FK Leg to BND Leg", c=self.callRButtonLegFK)

        mc.rowColumnLayout(numberOfColumns=2)
        mc.button(l="Left IK Leg to BND Leg", c=self.callLButtonLegIK)  # Match left IK arm to result arm
        mc.radioButtonGrp("leftIKLegMode", vr=True, numberOfRadioButtons=2,
                          labelArray2=["Auto Knee (NoFlip)", "Manual (Pole Vector)"],
                          select=1)
        mc.setParent("..")

        mc.rowColumnLayout(numberOfColumns=2)
        mc.button(l="Right IK Leg to BND Leg", c=self.callRButtonLegIK)  # Match left IK arm to result arm
        mc.radioButtonGrp("rightIKLegMode", vr=True, numberOfRadioButtons=2,
                          labelArray2=["Auto Knee (NoFlip)", "Manual (Pole Vector)"],
                          select=1)
        mc.setParent("..")

        mc.showWindow("matchApp")

    def callLButtonArmFK(self, *args):
        self.arm_FKtoResult("l_")
        return

    def callRButtonArmFK(self, *args):
        self.arm_FKtoResult("r_")
        return

    def callLButtonLegFK(self, *args):
        self.leg_FKtoResult("l_")
        return

    def callRButtonLegFK(self, *args):
        self.leg_FKtoResult("r_")
        return

    def callLButtonArmIK(self, *args):
        forearm = mc.radioButtonGrp("leftForeArmMode", q=True, select=True)
        self.arm_IKtoResult(forearm_mode=forearm, leftRight="l_")
        return

    def callRButtonArmIK(self, *args):
        forearm = mc.radioButtonGrp("rightForeArmMode", q=True, select=True)
        self.arm_IKtoResult(forearm_mode=forearm, leftRight="r_")
        return

    def callLButtonLegIK(self, *args):
        lowerLegMode = mc.radioButtonGrp("leftIKLegMode", q=True, select=True)
        self.leg_IKtoResult(leftRight="l_", lowerLegMode=lowerLegMode)
        return

    def callRButtonLegIK(self, *args):
        lowerLegMode = mc.radioButtonGrp("rightIKLegMode", q=True, select=True)
        self.leg_IKtoResult(leftRight="r_", lowerLegMode=lowerLegMode)
        return
