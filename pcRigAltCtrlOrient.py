'''
Created on May 30, 2014
for Tin Girl Book and game project

@author: Eyal Assaf


USE:

import tgpCtrlOrient as co
reload(co)
co.tgpCtrlOrient()

'''

import maya.cmds as mc
# import tgpUtils as ut
from tgpBaseUI import BaseUI as UI


class pcRigAltCtrlOrient(UI):
    def __init__(self):

        self.window = "coWindow"
        self.title = "tgpCtrlOrient"
        self.winSize = (250, 250)

        self.createUI()

    def createCustom(self, *args):
        # create the GUI
        mc.text(align="left", label="Select the joints and pick a ctrl axis.")
        mc.radioButtonGrp("rbtns", labelArray3=["X", "Y", "Z"],
                          cw3=(80, 80, 80), nrb=3, sl=1)
        mc.separator(st="in", w=250)
        #
        mc.floatFieldGrp("cRad", cal=(1, "left"), nf=1, label="Enter radius of the controls: ", v1=1, pre=2, w=300)
        mc.separator(st="in", w=250)
        mc.checkBox("pCheck", label="Parent controllers", v=1)
        mc.checkBox("lhCheck", label="Show only rotation channels", v=1)
        mc.checkBox("crCheck", label="Controllable Radius", v=1)
        #

        mc.showWindow(self.window)

    def createButtonCmd(self, *args):
        self.tgpMakeCtrl()

    def tgpMakeCtrl(self, *args):

        tempSkip = False
        # query the button selection
        axis = mc.radioButtonGrp("rbtns", q=True, select=True)
        getAxis = self.tgpGetAxis(axis)
        getRad = mc.floatFieldGrp("cRad", q=True, v1=True)
        gArray, cArray = [], []
        # error check to make sure only joints are selected
        selJoints = mc.ls(sl=True, fl=True, type="joint")
        numJnts = len(selJoints)
        rVals = ['rx', 'ry', 'rz']

        getCrCheck = mc.checkBox("crCheck", q=1, v=1)
        if numJnts == 0:
            mc.warning("pick a joint!")
        else:
            for i in range(numJnts):
                # get joint position
                jntInfo = mc.xform(selJoints[i], q=1, t=1, ws=1)

                # look for "_JNT" in joint naming convention
                ctrlName = selJoints[i].split("JNT_BND_")[1]



                # create curve controls and group it to itself

                ctrlCurveName = "CTRL_FK_{0}".format(ctrlName)
                ctrlCurve = mc.circle(name=ctrlCurveName,
                                      c=(0, 0, 0), nr=getAxis, sw=360, r=getRad, d=3,
                                      ut=0, tol=0.1, ch=1)
                print(ctrlCurve)
                ctrlCurveNameCircle = ctrlCurveName+"MakeCircle"

                mc.rename(ctrlCurve[1], ctrlCurveNameCircle)
                ctrlGroup = mc.group(name="GRP_{0}".format(ctrlName))

                # create an array of controls and groups for parenting option
                gArray.append(ctrlGroup)
                cArray.append(ctrlCurve[0])

                # move groups to joint position
                mc.xform(ctrlGroup, t=(jntInfo[0], jntInfo[1], jntInfo[2]), ws=True)

                # parentConstrain groups to joints and delete constraint
                connect = mc.parentConstraint(selJoints[i], ctrlGroup, mo=False)
                mc.delete(connect)
                #
                #

                # orientConstraint joint rotation to curves
                #mc.orientConstraint(ctrlCurve, selJoints[i])
                # we will use the connection editor in this
                for x in range(len(rVals)):
                    mc.connectAttr("{0}.{1}".format(ctrlCurveName, rVals[x]), "{0}.{1}".format(selJoints[i], rVals[x]))

                if getCrCheck:
                    cRadius = "cRadius"

                    mc.addAttr(ctrlCurveName, ln=cRadius, attributeType="float", k=True, minValue=0, defaultValue = getRad)

                    mc.connectAttr("{0}.{1}".format(ctrlCurveName, cRadius),"{0}.radius".format(ctrlCurveNameCircle))



                # pointConstraint groups to joints
                #mc.pointConstraint(selJoints[i], ctrlGroup, mo=False)

        if tempSkip:
            return
        # parent controls
        getPcheck = mc.checkBox("pCheck", q=1, v=1)  # checkbox enabled?
        getLhCheck = mc.checkBox("lhCheck", q=1, v=1)
        # if (getPcheck!=0):
        if getPcheck:
            for x in range(len(gArray)):
                try:
                    mc.parent(gArray[x + 1], cArray[x])
                except:
                    mc.select(clear=True)

        # hide all channels except rotation
        if getLhCheck:
            for y in range(len(cArray)):
                toLock = [".tx", ".ty", ".tz", ".sx", ".sy", ".sz", ".visibility"]
                for locked in range(len(toLock)):
                    mc.setAttr((cArray[y] + toLock[locked]),
                               k=False, cb=False)

    #
    def tgpGetAxis(self, axis):
        # create a dictionary with the axis values
        axisOpt = {'1': [1, 0, 0], '2': [0, 1, 0], '3': [0, 0, 1]}
        if (axis == 1):
            return axisOpt["1"]
        elif (axis == 2):
            return axisOpt["2"]
        elif (axis == 3):
            return axisOpt["3"]