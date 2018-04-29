import maya.cmds as mc


class pcFKIKSwitching():
    def __init__(self):
        self.window = "bcWindow"
        self.title = "pcRigHands"
        self.winSize = (500, 100)

        self.createUI()

    def diffVal(self, val1, val2):
        val3 = []
        for i in range(len(val1)):
            val3.append((val1[i] - val2[2]))

        return val3

    def l_arm_FKtoResult(self, *args):
        # left FK to IK
        default_upperArm_length = mc.getAttr("l_upperArm_normalize_DIV.input2X")  # default_upperArm_length = 23.508
        default_lowerArm_length = mc.getAttr("l_lowerArm_normalize_DIV.input2X")  # default_upperArm_length = 27.351
        # current values
        curr_upperArm_length = mc.getAttr("JNT_BND_l_lowerArm.translateX")
        curr_lowerArm_length = mc.getAttr("JNT_BND_l_hand.translateX")

        upperArm_length_factor = curr_upperArm_length / default_upperArm_length
        lowerArm_length_factor = curr_lowerArm_length / default_lowerArm_length

        mc.setAttr("CTRL_FK_l_upperArm.length", upperArm_length_factor)
        mc.setAttr("CTRL_FK_l_lowerArm.length", lowerArm_length_factor)

        mc.setAttr("{0}.rotate".format("CTRL_gimbalCorr_l_arm"), 0, 0, 0)

        '''mc.xform("CTRL_FK_l_upperArm", ws=True, ro=(r_upperArm[0], r_upperArm[1], r_upperArm[2]))
        mc.xform("CTRL_FK_l_lowerArm", ws=True, ro=(r_lowerArm[0], r_lowerArm[1], r_lowerArm[2]))
        mc.xform("CTRL_FK_l_hand", ws=True, ro=(r_hand[0], r_hand[1], r_hand[2]))'''

        mc.matchTransform("CTRL_FK_l_upperArm", "JNT_FKsnap_l_upperArm", rot=True)
        mc.matchTransform("CTRL_FK_l_lowerArm", "JNT_FKsnap_l_lowerArm", rot=True)
        mc.matchTransform("CTRL_FK_l_hand", "JNT_FKsnap_l_hand", rot=True)
        mc.setAttr("CTRL_settings_l_arm.fkik_blend", 0)  # now that we have the FK in place, we want to switch to it

    def r_arm_FKtoResult(self, *args):
        # right FK to IK

        default_upperArm_length = mc.getAttr("r_upperArm_normalize_DIV.input2X")  # default_upperArm_length = 23.508
        default_lowerArm_length = mc.getAttr("r_lowerArm_normalize_DIV.input2X")  # default_upperArm_length = 27.351
        # current values
        curr_upperArm_length = mc.getAttr("JNT_BND_r_lowerArm.translateX")
        curr_lowerArm_length = mc.getAttr("JNT_BND_r_hand.translateX")

        upperArm_length_factor = abs(curr_upperArm_length / default_upperArm_length)
        lowerArm_length_factor = abs(curr_lowerArm_length / default_lowerArm_length)

        '''r_upperArm = mc.xform("JNT_FKsnap_r_upperArm", query=True, worldSpace=True, rotation=True)
        r_lowerArm = mc.xform("JNT_FKsnap_r_lowerArm", query=True, worldSpace=True, rotation=True)
        r_hand = mc.xform("JNT_FKsnap_r_hand", query=True, worldSpace=True, rotation=True)'''

        mc.setAttr("CTRL_FK_r_upperArm.length", upperArm_length_factor)
        mc.setAttr("CTRL_FK_r_lowerArm.length", lowerArm_length_factor)

        mc.setAttr("{0}.rotate".format("CTRL_gimbalCorr_r_arm"), 0, 0, 0)

        '''mc.xform("CTRL_FK_r_upperArm", ws=True, ro=(r_upperArm[0]*-1, r_upperArm[1], r_upperArm[2]*-1))
        mc.xform("CTRL_FK_r_lowerArm", ws=True, ro=(r_lowerArm[0], r_lowerArm[1], r_lowerArm[2]))
        mc.xform("CTRL_FK_r_hand", ws=True, ro=(r_hand[0], r_hand[1], r_hand[2]))'''

        mc.matchTransform("CTRL_FK_r_upperArm", "JNT_FKsnap_r_upperArm", rot=True)
        mc.matchTransform("CTRL_FK_r_lowerArm", "JNT_FKsnap_r_lowerArm", rot=True)
        mc.matchTransform("CTRL_FK_r_hand", "JNT_FKsnap_r_hand", rot=True)

        mc.setAttr("CTRL_settings_r_arm.fkik_blend", 0)  # now that we have the FK in place, we want to switch to it

    def l_arm_IKtoResult(self, forearm_mode=1, *args):
        # left IK to FK
        default_upperArm_length = mc.getAttr("l_upperArm_normalize_DIV.input2X")  # default_upperArm_length = 23.508
        default_lowerArm_length = mc.getAttr("l_lowerArm_normalize_DIV.input2X")  # default_upperArm_length = 27.351
        # current values
        curr_upperArm_length = mc.getAttr("JNT_BND_l_lowerArm.translateX")
        curr_lowerArm_length = mc.getAttr("JNT_BND_l_hand.translateX")

        print("forearm_mode: {0}".format(forearm_mode))
        tolerance = 0.001

        if forearm_mode == 1:
            print("Forearm mode 1")
            if ((abs(curr_upperArm_length - default_upperArm_length) > tolerance) or (
                    abs(curr_lowerArm_length - default_lowerArm_length) > tolerance)):
                mc.setAttr("CTRL_l_elbow.elbowSnap", 1)
                mc.setAttr("CTRL_settings_l_arm.IK_stretch", 0)

            mc.matchTransform("CTRL_l_arm", "GRP_IKsnap_l_arm", rotation=True)
            mc.matchTransform("CTRL_l_arm", "GRP_IKsnap_l_arm", position=True)
            mc.matchTransform("CTRL_l_elbow", "JNT_BND_l_lowerArm", position=True)

            mc.setAttr("CTRL_l_elbow.FKIK_lowerArmBlend", 1)

        else:  # if forearm 2/IK FKelbow is selected
            print("Forearm mode ")
            lowerArm_length_factor = curr_lowerArm_length / default_lowerArm_length

            ctrlElbow = "CTRL_l_elbow"
            tgtJnt = "GRP_IKsnap_l_elbow"

            print(mc.matchTransform("CTRL_l_elbow", "JNT_BND_l_lowerArm", pos=True))

            mc.matchTransform("CTRL_FK_l_lowerArmElbow", "JNT_BND_l_lowerArm", rotation=True)
            mc.matchTransform("CTRL_FK_l_handElbow", "JNT_FKsnap_l_hand", rotation=True)

            mc.setAttr("CTRL_l_elbow.elbowSnap", 1)
            mc.setAttr("CTRL_l_elbow.FKIK_lowerArmBlend", 0)

            mc.setAttr("CTRL_FK_l_lowerArmElbow.length", lowerArm_length_factor)

        mc.setAttr("CTRL_settings_l_arm.fkik_blend", 1)  # now that we have the FIK in place, we want to switch to it

        # mc.setAttr("CTRL_settings_l_arm.fkik_blend", 1)

    def r_arm_IKtoResult(self, forearm_mode=1, *args):
        # right IK to FK
        default_upperArm_length = mc.getAttr("r_upperArm_normalize_DIV.input2X")  # default_upperArm_length = -23.508
        default_lowerArm_length = mc.getAttr("r_lowerArm_normalize_DIV.input2X")  # default_upperArm_length = -27.351
        # current values
        curr_upperArm_length = mc.getAttr("JNT_BND_r_lowerArm.translateX")
        curr_lowerArm_length = mc.getAttr("JNT_BND_r_hand.translateX")

        print("forearm_mode: {0}".format(forearm_mode))
        tolerance = 0.001

        if forearm_mode == 1:
            if ((abs(curr_upperArm_length - default_upperArm_length) > tolerance) or (
                    abs(curr_lowerArm_length - default_lowerArm_length) > tolerance)):
                mc.setAttr("CTRL_r_elbow.elbowSnap", 1)
                mc.setAttr("CTRL_settings_r_arm.IK_stretch", 0)

            mc.matchTransform("CTRL_r_arm", "GRP_IKsnap_r_arm", rotation=True)
            mc.matchTransform("CTRL_r_arm", "GRP_IKsnap_r_arm", position=True)
            mc.matchTransform("CTRL_r_elbow", "JNT_BND_r_lowerArm", position=True)

            mc.setAttr("CTRL_r_elbow.FKIK_lowerArmBlend", 1)
        else:  # if forearm 2/IK FKelbow is selected
            lowerArm_length_factor = abs(curr_lowerArm_length / default_lowerArm_length)

            mc.setAttr("CTRL_r_elbow.elbowSnap", 1)
            mc.setAttr("CTRL_r_elbow.FKIK_lowerArmBlend", 0)

            mc.matchTransform("CTRL_r_elbow", "JNT_BND_r_lowerArm", position=True)
            mc.matchTransform("CTRL_FK_r_lowerArmElbow", "JNT_BND_r_lowerArm", rotation=True)
            mc.matchTransform("CTRL_FK_r_handElbow", "JNT_FKsnap_r_hand", rotation=True)

            mc.setAttr("CTRL_FK_r_lowerArmElbow.length", lowerArm_length_factor)

        mc.setAttr("CTRL_settings_r_arm.fkik_blend", 1)  # now that we have the FIK in place, we want to switch to it

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

        mc.button(l="Left FK Arm to IK Arm", c=self.l_arm_FKtoResult)
        mc.button(l="Right FK Arm to IK Arm", c=self.r_arm_FKtoResult)

        mc.rowColumnLayout(numberOfColumns=2)
        mc.button(l="Left IK Arm to FK Arm BND", c=self.callLButton)  # Match left IK arm to result arm
        mc.radioButtonGrp("leftForeArmMode", vr=True, numberOfRadioButtons=2, labelArray2=["IK forearm", "FK forearm"],
                          select=1)
        mc.setParent("..")

        mc.rowColumnLayout(numberOfColumns=2)
        mc.button(l="Right IK Arm to FK Arm BND", c=self.callRButton)  # Match left IK arm to result arm
        mc.radioButtonGrp("rightForeArmMode", vr=True, numberOfRadioButtons=2, labelArray2=["IK forearm", "FK forearm"],
                          select=1)
        mc.setParent("..")

        mc.showWindow("matchApp")

    def callLButton(self, *args):
        forearm = mc.radioButtonGrp("leftForeArmMode", q=True, select=True)
        print("forearm choice: {0}".format(forearm))
        self.l_arm_IKtoResult(forearm_mode=forearm)
        return

    def callRButton(self, *args):
        forearm = mc.radioButtonGrp("rightForeArmMode", q=True, select=True)
        self.r_arm_IKtoResult(forearm_mode=forearm)
        return
