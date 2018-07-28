import maya.cmds as mc

import pymel.core.runtime as pyml

class pcDemoReelResetScene():
    def __init__(self, clearBaseVal=True, resetToDefaultVal=False, resetCameraVals=False, getCamera=False):

        if clearBaseVal:
            self.clearBaseVals()
        if resetToDefaultVal:
            self.resetToDefaultVals()
        if resetCameraVals:
            self.resetCameraVal()
        if getCamera:
            self.getCameraVals()


    def getCameraVals(self):
        camDemo = 'CAM_demoReel'
        camDemoShape = camDemo + "Shape"
        listCam = mc.listAttr(camDemo, k=True)
        listCamShape = mc.listAttr(camDemoShape, k=True)

        print(listCam)
        print(listCamShape)

        for i in range(len(listCam)):
            tVal = listCam[i]
            getVal = mc.getAttr("{0}.{1}".format(camDemo, tVal))
            print("mc.setAttr('{0}.{1}', {2})".format(camDemo, tVal, getVal))

        for i in range(len(listCamShape)):
            tVal = listCamShape[i]
            getVal = mc.getAttr("{0}.{1}".format(camDemoShape, tVal))
            print("mc.setAttr('{0}.{1}', {2})".format(camDemoShape, tVal, getVal))

    def resetCameraVal(self):
        mc.setAttr('CAM_demoReel.visibility', False)
        mc.setAttr('CAM_demoReel.translateX', 158.825646657)
        mc.setAttr('CAM_demoReel.translateY', 209.465431984)
        mc.setAttr('CAM_demoReel.translateZ', 368.062117146)
        mc.setAttr('CAM_demoReel.rotateX', -17.2636767822)
        mc.setAttr('CAM_demoReel.rotateY', 23.66212)
        mc.setAttr('CAM_demoReel.rotateZ', 4.34061713752e-16)
        mc.setAttr('CAM_demoReel.scaleX', 1.0)
        mc.setAttr('CAM_demoReel.scaleY', 1.0)
        mc.setAttr('CAM_demoReel.scaleZ', 1.0)
        mc.setAttr('CAM_demoReelShape.horizontalFilmAperture', 1.417)
        mc.setAttr('CAM_demoReelShape.verticalFilmAperture', 0.9445)
        mc.setAttr('CAM_demoReelShape.focalLength', 35.0)
        mc.setAttr('CAM_demoReelShape.lensSqueezeRatio', 1.0)
        mc.setAttr('CAM_demoReelShape.fStop', 5.6)
        mc.setAttr('CAM_demoReelShape.focusDistance', 5.0)
        mc.setAttr('CAM_demoReelShape.shutterAngle', 144.0)
        mc.setAttr('CAM_demoReelShape.centerOfInterest', 417.907322903)

    def resetToDefaultVals(self):
        pyml.SelectTool()

        leftRight = ["l_", "r_"]

        mc.setAttr("CTRL_eyes.eyesFollow", 0)
        mc.setAttr("CTRL_head.rotationSpace", 0)
        mc.setAttr("CTRL_head.translationSpace", 0)
        for i in range(len(leftRight)):
            lrVal = leftRight[i]
            mc.setAttr("CTRL_{0}foot.autoManualKneeBlend".format(lrVal), 1)
            mc.setAttr("CTRL_settings_{0}arm.fkik_blend".format(lrVal), 0)
            mc.setAttr("CTRL_settings_{0}leg.fkik_blend".format(lrVal), 1)

        mc.select(cl=True)

    def clearBaseVals(self):

        leftRight = ["l_", "r_"]
        translateVals = ["translateX", "translateY", "translateZ"]
        rotateVals = ["rotateX", "rotateY", "rotateZ"]
        scaleVals = ["scaleX", "scaleY", "scaleZ", ]

        length = "length"
        rotateLength = []
        rotateLength.extend(rotateVals)
        rotateLength.append(length)

        transRotate = []
        transRotate.extend(translateVals)
        transRotate.extend(rotateVals)

        transRotateScale = []
        transRotateScale.extend(transRotate)
        transRotateScale.extend(scaleVals)

        fingers = ["thumb", "pointer", "middle", "ring", "pinky"]

        footAttributes0 = ["kneeTwist", "roll", "tilt", "lean", "toeSpin", "toeWiggle", "toeLift", "ballLift",
                           "heelLift"]
        footAttributes1 = ["autoKneeLowerLegLength", "autoKneeUpperLegLength", ]

        handFingAttr = ["curl", "scrunch", "lean", "relax", "spread"]
        handAttr = []
        handAttr.extend(handFingAttr)
        handAttr.extend(["fist", "palmRaise", "sideRoll"])
        fingerAttr = []
        fingerAttr.extend(handFingAttr)
        fingerAttr.append(length)

        for i in range(len(transRotateScale)):
            tval = transRotateScale[i]
            if "scale" in transRotateScale[i]:
                setVal = 1
            else:
                setVal = 0
            mc.setAttr("CTRL_rootTransform.{0}".format(tval), setVal)

        mc.setAttr("CTRL_shoulder.stretchable", 1)
        mc.setAttr("CTRL_head.stretchable", 1)


        for i in range(len(transRotate)):
            tval = transRotate[i]
            mc.setAttr("CTRL_hip.{0}".format(tval), 0)
            mc.setAttr("CTRL_shoulder.{0}".format(tval), 0)
            mc.setAttr("CTRL_body.{0}".format(tval), 0)
            mc.setAttr("CTRL_head.{0}".format(tval), 0)
            mc.setAttr("CTRL_eyes.{0}".format(tval), 0)

        for i in range(len(rotateVals)):
            tval = rotateVals[i]
            mc.setAttr("CTRL_jaw.{0}".format(tval), 0)
            mc.setAttr("CTRL_FK_spine1.{0}".format(tval), 0)
            mc.setAttr("CTRL_FK_spine2.{0}".format(tval), 0)
            mc.setAttr("CTRL_FK_neckBase.{0}".format(tval), 0)

        for x in range(len(leftRight)):
            lrVal = leftRight[x]
            mc.setAttr("CTRL_{0}knee.kneeSnap".format(lrVal), 0)
            mc.setAttr("CTRL_{0}elbow.elbowSnap".format(lrVal), 0)

            mc.setAttr("CTRL_{0}elbow.FKIK_lowerArmBlend".format(lrVal), 1)
            mc.setAttr("CTRL_settings_{0}arm.IK_stretch".format(lrVal), 0)
            mc.setAttr("CTRL_settings_{0}leg.IK_stretch".format(lrVal), 0)

            mc.setAttr("CTRL_{0}foot.bendLimitAngle".format(lrVal), 45)
            mc.setAttr("CTRL_{0}foot.toeStraight".format(lrVal), 75)
            for i in range(len(footAttributes0)):
                tval = footAttributes0[i]
                mc.setAttr("CTRL_{0}foot.{1}".format(lrVal, tval), 0)

            for i in range(len(footAttributes1)):
                tval = footAttributes1[i]
                mc.setAttr("CTRL_{0}foot.{1}".format(lrVal, tval), 1)

            for i in range(len(handAttr)):
                tval = handAttr[i]
                mc.setAttr("CTRL_{0}hand.{1}".format(lrVal, tval), 0)

            for i in range(len(fingerAttr)):
                tval = fingerAttr[i]
                if length in tval:
                    setVal = 1
                else:
                    setVal = 0
                for j in range(len(fingers)):
                    fingVal = fingers[j]
                    mc.setAttr("CTRL_{0}{1}.{2}".format(lrVal, fingVal, tval), setVal)

            for i in range(len(translateVals)):
                tval = translateVals[i]
                mc.setAttr("CTRL_{0}eye.{1}".format(lrVal, tval), 0)
                mc.setAttr("CTRL_{0}shoulder.{1}".format(lrVal, tval), 0)
                mc.setAttr("CTRL_{0}knee.{1}".format(lrVal, tval), 0)
                mc.setAttr("CTRL_{0}elbow.{1}".format(lrVal, tval), 0)

            for i in range(len(rotateVals)):
                tval = rotateVals[i]
                mc.setAttr("CTRL_gimbalCorr_{0}arm.{1}".format(lrVal, tval), 0)
                mc.setAttr("CTRL_FK_{0}hand.{1}".format(lrVal, tval), 0)
                mc.setAttr("CTRL_FK_{0}handElbow.{1}".format(lrVal, tval), 0)

                mc.setAttr("CTRL_FK_{0}ankleTwist.{1}".format(lrVal, tval), 0)
                mc.setAttr("CTRL_FK_{0}ball.{1}".format(lrVal, tval), 0)

                for j in range(len(fingers)):
                    fingVal = fingers[j]
                    for k in range(1, 4):
                        if k == 3 and "thumb" in fingers[j]:
                            enterVal = "Orbit"
                        else:
                            enterVal = k
                            mc.setAttr("CTRL_FK_{0}{1}{2}.{3}".format(lrVal, fingVal, enterVal, tval), 0)

            for i in range(len(transRotate)):
                tval = transRotate[i]
                mc.setAttr("CTRL_{0}arm.{1}".format(lrVal, tval), 0)
                mc.setAttr("CTRL_{0}foot.{1}".format(lrVal, tval), 0)

            for i in range(len(rotateLength)):
                tval = rotateLength[i]
                if length in tval:
                    setVal = 1
                else:
                    setVal = 0
                mc.setAttr("CTRL_FK_{0}upperArm.{1}".format(lrVal, tval), setVal)
                mc.setAttr("CTRL_FK_{0}lowerArm.{1}".format(lrVal, tval), setVal)

                mc.setAttr("CTRL_FK_{0}lowerArmElbow.{1}".format(lrVal, tval), setVal)

                mc.setAttr("CTRL_FK_{0}lowerLeg.{1}".format(lrVal, tval), setVal)
                mc.setAttr("CTRL_FK_{0}upperLeg.{1}".format(lrVal, tval), setVal)
