import maya.cmds as mc


class pcFKIKSwitching():
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
        # left IK to FK
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
            print("Forearm mode ")
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

        mc.button(l="Left FK Arm to IK Arm", c=self.callLButtonFK)
        mc.button(l="Right FK Arm to IK Arm", c=self.callRButtonFK)

        mc.rowColumnLayout(numberOfColumns=2)
        mc.button(l="Left IK Arm to FK Arm BND", c=self.callLButtonIK)  # Match left IK arm to result arm
        mc.radioButtonGrp("leftForeArmMode", vr=True, numberOfRadioButtons=2, labelArray2=["IK forearm", "FK forearm"],
                          select=1)
        mc.setParent("..")

        mc.rowColumnLayout(numberOfColumns=2)
        mc.button(l="Right IK Arm to FK Arm BND", c=self.callRButtonIK)  # Match left IK arm to result arm
        mc.radioButtonGrp("rightForeArmMode", vr=True, numberOfRadioButtons=2, labelArray2=["IK forearm", "FK forearm"],
                          select=1)
        mc.setParent("..")

        mc.showWindow("matchApp")

    def callLButtonFK(self, *args):
        self.arm_FKtoResult("l_")
        return

    def callRButtonFK(self, *args):
        self.arm_FKtoResult("r_")
        return

    def callLButtonIK(self, *args):
        forearm = mc.radioButtonGrp("leftForeArmMode", q=True, select=True)
        self.arm_IKtoResult(forearm_mode=forearm, leftRight="l_")
        return

    def callRButtonIK(self, *args):
        forearm = mc.radioButtonGrp("rightForeArmMode", q=True, select=True)
        self.arm_IKtoResult(forearm_mode=forearm, leftRight="r_")
        return
