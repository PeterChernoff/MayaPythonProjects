'''
Created on May 30, 2014
for Tin Girl Book and game project

@author: Eyal Assaf
'''
import maya.cmds as mc
# import tgpUtils as ut
from functools import partial
import tgpBaseUI
from tgpBaseUI import BaseUI as UI

reload(tgpBaseUI)

import pcCreateRigAlt00AUtilities

from pcCreateRigAlt00AUtilities import pcCreateRigUtilities as CRU

reload(pcCreateRigAlt00AUtilities)


class pcCreateRigAlt02HeadCode(object):
    def __init__(self, cbGeo=True, cbSpine=True,
                 jntIKShoulderCheck="JNT_IK_shoulder", grpTorsoDNTCheck="GRP_DO_NOT_TOUCH_torso",
                 ctrlRootTransCheck="CTRL_rootTransform", bndJnt="JNT_BND_neck1", jntHead="JNT_BND_head",
                 ctrlShoulderCheck="CTRL_shoulder", jntSpineEndCheck="JNT_BND_spineEnd",
                 cbJaw=True, cbEyes=True,
                 cbTorso=True, cbNeck=True, ):

        self.tgpMakeBC(cbGeo, cbSpine,
                       jntIKShoulderCheck, grpTorsoDNTCheck,
                       ctrlRootTransCheck, bndJnt, jntHead,
                       ctrlShoulderCheck, jntSpineEndCheck,

                       cbJaw, cbEyes,
                       cbTorso, cbNeck)

    def createIKSpline(self, jntStart, jntEnd, name, *args):

        ikSpline = mc.ikHandle(n="HDL_{0}".format(name), sj=jntStart, ee=jntEnd, sol="ikSplineSolver", numSpans=1)

        hdlSpline = ikSpline[0]
        effSpline = ikSpline[1]
        crvSpline = ikSpline[2]

        effSpline = mc.rename(effSpline, "EFF_{0}".format(name))
        crvSpline = mc.rename(crvSpline, "CRV_{0}".format(name))

        return hdlSpline, effSpline, crvSpline

    def createNeckIK(self, jntArray, jntEnd, jntEndSize, crvToUse, *args):

        ikNeckBase = mc.duplicate(jntEnd, n="JNT_IK_neckBase", renameChildren=True)
        mc.parent(ikNeckBase, w=True)
        noUnicode = str(ikNeckBase[0])
        mc.setAttr('{0}.radius'.format(noUnicode), jntEndSize * 3)
        ikNeckEnd = mc.duplicate(ikNeckBase, n="JNT_IK_neckEnd")

        CRU.changeRotateOrder(ikNeckEnd, "ZXY")
        neckIKs = [ikNeckBase[0], ikNeckEnd[0]]

        # moves the named IK joints into position using constraints, then deletes the constraints
        todelete1 = mc.parentConstraint(jntArray[0], ikNeckBase[0], mo=False)

        mc.delete(todelete1)

        '''
        Bind To: Selected Joints
        Bind Method: Closest Distance
        Skinning Method: Classic Linear
        Normalize Weights: Interactive
        Max Influences  2

        '''
        mc.select(crvToUse, ikNeckBase, ikNeckEnd)

        # mc.skinCluster (ikHip, ikShoulder, crvSpine, sm=0, nw = 1)

        scls = mc.skinCluster(ikNeckBase, ikNeckEnd, crvToUse, name='neck_skinCluster', toSelectedBones=True,
                              bindMethod=0, skinMethod=0, normalizeWeights=1, maximumInfluences=2)[0]

        return ikNeckBase[0], ikNeckEnd[0], neckIKs

    def addIkTwist(self, hdlSpline, ikBase, ikEnd, *args):

        '''
        Set World Up Type to Object Rotation Up (Start/End)
        Set Forward axis to Positive X
        Set Up axis to Negative Y
        Set Up Vector to 0, -1, 0
        Set Up Vector 2 to 0, -1, 0 (Best works if all joints are facing the same direction, and may need to be adjusted)
        Note: this would likely be 0, -1, -1 if using the default version with the end joint set to world space
        Set World Up Object to JNT_IK_neckBase
        Set World Up Object 2 to JNT_IK_neckEnd
        Set Twist Value Type to Start/End.

        '''
        mc.setAttr('{0}.dTwistControlEnable'.format(hdlSpline), True)

        mc.setAttr('{0}.dForwardAxis'.format(hdlSpline), 0)

        mc.setAttr('{0}.dWorldUpType'.format(hdlSpline), 4)
        mc.setAttr('{0}.dWorldUpAxis'.format(hdlSpline), 1)

        mc.setAttr('{0}.dWorldUpVectorX'.format(hdlSpline), 0)
        mc.setAttr('{0}.dWorldUpVectorY'.format(hdlSpline), -1)
        mc.setAttr('{0}.dWorldUpVectorZ'.format(hdlSpline), 0)

        mc.setAttr('{0}.dWorldUpVectorEndX'.format(hdlSpline), 0)
        mc.setAttr('{0}.dWorldUpVectorEndY'.format(hdlSpline), -1)
        mc.setAttr('{0}.dWorldUpVectorEndZ'.format(hdlSpline), 0)

        mc.connectAttr(ikBase + ".worldMatrix[0]", hdlSpline + ".dWorldUpMatrix")
        mc.connectAttr(ikEnd + ".worldMatrix[0]", hdlSpline + ".dWorldUpMatrixEnd")

        mc.setAttr('{0}.dTwistValueType'.format(hdlSpline), 1)
        mc.select(hdlSpline)

    def createHeadCtrls(self, ikNeckEnd, *args):
        # Creates the head control
        ctrlHeadName = "CTRL_head"
        ctrlHeadPre, ctrlHeadPreName = CRU.setupCtrl(ikNeckEnd, 14, orientVal=(0, 1, 0), colourTU=CRU.clrBodyFK, )
        ctrlHead = mc.rename(ctrlHeadPre, ctrlHeadName)
        todelete = mc.pointConstraint(ikNeckEnd, ctrlHead)
        mc.delete(todelete)

        mc.makeIdentity(ctrlHead, apply=True, t=True, r=True, s=True)
        mc.select(ctrlHead + ".cv[:]")
        mc.move(20, y=True, r=True, os=True, wd=True)
        CRU.changeRotateOrder([ctrlHead], "ZXY")
        CRU.layerEdit([ctrlHead], ikLayer=True, noRecurse=True)
        mc.parentConstraint(ctrlHead, ikNeckEnd, mo=True)

        return ctrlHead

    def createFKJntAndCtrls(self, jntArray, jntEnd, jntEndSize, *args):

        mc.select(cl=True)
        # create FK joints, then orient them to world
        fkJnts = []
        ctrlFKJntsTU = []
        addFKJnt = False
        grpFKConsts = []
        ctrlFKJntsEnds = []

        jntSize = len(jntArray)

        for i in range(0, jntSize):
            if i == jntSize - 1:
                lastTerm = "End"
            elif i == 0:
                lastTerm = "Base"
                addFKJnt = True
            else:
                # we only care if it's the first or last
                continue

            fkName = "JNT_FK_neck{0}".format(lastTerm)

            pos = mc.xform(jntArray[i], query=True, translation=True, worldSpace=True)
            fkJnts.append(mc.joint(name=fkName, p=pos, rad=jntEndSize * 2))

            if addFKJnt:
                ctrlFKJntsTU.append(fkName)

            else:
                # creates the names for GRP_FKConsts
                ctrlFKJntsEnds.append(fkName)
                grpFKConsts.append("GRP_FKConst{0}".format(lastTerm))

            mc.setAttr('{0}.overrideEnabled'.format(fkName), 1)
            mc.setAttr("{0}.overrideColor".format(fkName), 28)

            addFKJnt = False
        # change the rotate order
        CRU.changeRotateOrder([fkJnts[0]], "YZX")
        for i in range(len(fkJnts) - 1):
            mc.joint(fkJnts[i], e=True, zso=True, oj="yxz", secondaryAxisOrient="xup")

        # create the FK control and move it into a nice position
        ctrlFK, ctrlShape = CRU.createCTRLsFKDirect(fkJnts[0], 10, orientVal=(0, 1, 0), colourTU=CRU.clrBodyIK)
        # ctrlShape = mc.listRelatives(ctrlFK, s=True, )[0]
        fkJnts[0] = ctrlFK

        fkLength = mc.getAttr("{0}.ty".format(fkJnts[-1]))
        cvsToMove = mc.select(ctrlShape + ".cv[:]")
        mc.move(fkLength * .35, cvsToMove, y=True, r=True, wd=True, os=True)

        CRU.layerEdit(fkJnts, fkLayer=True, noRecurse=True)

        return ctrlFK, fkJnts

    def createGroupHead(self, ctrlHead, ikNeckEnd, fkJnts, *args):

        grpHead = "GRP_head"
        mc.group(em=True, w=True, n=grpHead)
        todelete = mc.pointConstraint(ikNeckEnd, grpHead)
        mc.delete(todelete)
        mc.makeIdentity(grpHead, a=True)
        mc.parent(ctrlHead, grpHead)

        todelete = mc.parentConstraint(fkJnts[-1], grpHead, mo=True)
        # chapter 9 has this deleted so we'll do that here
        mc.delete(todelete)

        return grpHead

    def addStretch(self, jntArray, crvSpline, jntSize, name, ctrlRootTrans, *args):
        curveInfo = mc.arclen(crvSpline, ch=True)
        splineInfo = "{0}Info".format(name)

        curveInfo = mc.rename(curveInfo, splineInfo)
        curveLen = mc.getAttr("{0}.arcLength".format(curveInfo))
        splineStretchNameDiv = "{0}_stretchPercent_DIV".format(name)
        mc.shadingNode("multiplyDivide", n=splineStretchNameDiv, au=True)

        mc.setAttr("{0}.i2x".format(splineStretchNameDiv), curveLen)
        mc.setAttr("{0}.operation".format(splineStretchNameDiv), 2)

        mc.connectAttr("{0}.arcLength".format(curveInfo), "{0}.i1x".format(splineStretchNameDiv))

        # get the scales to the spline

        # to allow for the squash/stretch
        # get square root of output

        splineStretchNamePow = "{0}_sqrtStretch_POW".format(name)

        mc.shadingNode("multiplyDivide", n=splineStretchNamePow, au=True)
        mc.setAttr("{0}.operation".format(splineStretchNamePow), 3)
        mc.setAttr("{0}.i2x".format(splineStretchNamePow), 0.5)
        mc.connectAttr("{0}.ox".format(splineStretchNameDiv), "{0}.i1x".format(splineStretchNamePow))

        # divide by the square root
        splineStretchNameInv = "{0}_stretchInvert_DIV".format(name)
        mc.shadingNode("multiplyDivide", n=splineStretchNameInv, au=True)
        mc.setAttr("{0}.operation".format(splineStretchNameInv), 2)
        mc.setAttr("{0}.i1x".format(splineStretchNameInv), 1)
        mc.connectAttr("{0}.ox".format(splineStretchNamePow), "{0}.i2x".format(splineStretchNameInv))

        for i in range(jntSize - 1):
            # connects the spline's joints to the joint scale to allow for squash and stretch
            mc.connectAttr("{0}.ox".format(splineStretchNameDiv), "{0}.scaleX".format(jntArray[i]))
            mc.connectAttr("{0}.ox".format(splineStretchNameInv), "{0}.scaleY".format(jntArray[i]))
            mc.connectAttr("{0}.ox".format(splineStretchNameInv), "{0}.scaleZ".format(jntArray[i]))

        globalScaleNormalizeDiv = "globalScale_{0}Normalize_DIV".format(name)
        mc.shadingNode("multiplyDivide", n=globalScaleNormalizeDiv, au=True)
        mc.setAttr("{0}.operation".format(globalScaleNormalizeDiv), 2)

        mc.connectAttr("{0}.arcLength".format(splineInfo), "{0}.i1x".format(globalScaleNormalizeDiv))
        mc.connectAttr("{0}.sy".format(ctrlRootTrans), "{0}.i2x".format(globalScaleNormalizeDiv))
        # we want to overwrite the old version
        mc.connectAttr("{0}.ox".format(globalScaleNormalizeDiv), "{0}.i1x".format(splineStretchNameDiv), f=True)

        return splineInfo, splineStretchNameDiv, globalScaleNormalizeDiv

    def parentRootTransform(self, ctrlRootTrans, crvNeck, hdlNeck, ikNeckBase, ikNeckEnd, grpHead, fkJntStart,
                            jntArrayStart, *args):
        grpHeadNeckName = "GRP_headNeck"
        grpHeadNeck = mc.group(n=grpHeadNeckName, w=True, em=True)
        mc.parent(crvNeck, hdlNeck, ikNeckBase, ikNeckEnd, grpHead, fkJntStart, jntArrayStart, grpHeadNeck)
        mc.parent(grpHeadNeck, ctrlRootTrans)

        mc.setAttr("{0}.inheritsTransform".format(crvNeck), False)
        return

    def createNeckShoulderLoc(self, cbSpine, jntIKShoulder, ikNeckBase, fkJnts, *args):
        locConstNeckShoulder = mc.spaceLocator(p=(0, 0, 0), name="LOC_const_neckShoulder")[0]
        # move to the base of the neck
        todelete = mc.pointConstraint(ikNeckBase, locConstNeckShoulder)
        mc.delete(todelete)

        if cbSpine:
            mc.parent(locConstNeckShoulder, jntIKShoulder)

        # Create a group for the FKNeck joint
        grpNeckFK = "GRP_FK_neck"
        mc.group(n=grpNeckFK, w=True, em=True)
        parentFK = mc.listRelatives(fkJnts[0], p=True)[0]
        mc.parent(grpNeckFK, parentFK)
        mc.parent(fkJnts[0], grpNeckFK)

        # locConstNeckShoulder parent constrains ikNeckBase and grpNeckFK
        mc.parentConstraint(locConstNeckShoulder, ikNeckBase, mo=True)
        mc.parentConstraint(locConstNeckShoulder, grpNeckFK, mo=True)

        mc.setAttr("{0}.v".format(locConstNeckShoulder), False)

        return locConstNeckShoulder, grpNeckFK

    def createSpaceSwitching(self, grpHead, ctrlHead, jntIKShoulder, ctrlRootTrans, fkJnts, grpTorsoDNT, *args):
        # to delete: I might have constrained the head control when I should have used the grpHead
        # creates the head follow attributes

        locHeadNeck = "LOC_space_headNeck"
        locHeadShoulder = "LOC_space_headShoulder"
        locHeadBody = "LOC_space_headBody"
        locHeadRoot = "LOC_space_headRoot"
        headLocArray = [locHeadNeck, locHeadShoulder, locHeadBody, locHeadRoot]
        for i in range(len(headLocArray)):
            mc.spaceLocator(p=(0, 0, 0), name=headLocArray[i])
        '''headLocArray.append(mc.spaceLocator(p=(0, 0, 0), name="LOC_space_headNeck")[0])
        headLocArray.append(mc.spaceLocator(p=(0, 0, 0), name="LOC_space_headShoulder")[0])
        headLocArray.append(mc.spaceLocator(p=(0, 0, 0), name="LOC_space_headBody")[0])
        headLocArray.append(mc.spaceLocator(p=(0, 0, 0), name="LOC_space_headRoot")[0])'''

        # moves these to the head
        for i in range(len(headLocArray)):
            todelete = mc.pointConstraint(fkJnts[-1], headLocArray[i])
            mc.delete(todelete)

        # parent the head space to their respective parts
        mc.parent(headLocArray[0], fkJnts[-1])
        mc.parent(headLocArray[1], jntIKShoulder)
        mc.parent(headLocArray[2], grpTorsoDNT)
        mc.parent(headLocArray[3], ctrlRootTrans)

        headFollowOrntConstr = mc.orientConstraint(headLocArray, grpHead)[0]
        headFollowPntConstr = mc.pointConstraint(headLocArray, grpHead)[0]

        headFollowRot = 'rotationSpace'
        headFollowTrans = 'translationSpace'
        mc.addAttr(ctrlHead, longName=headFollowRot, at="enum", enumName="Neck:Shoulders:upperBody:Root", k=True)
        mc.addAttr(ctrlHead, longName=headFollowTrans, at="enum", enumName="Neck:Shoulders:upperBody:Root", k=True)

        # grab the last 4 attributes
        headSpaceFollowOrnt = mc.listAttr(headFollowOrntConstr)[-4:]
        headSpaceFollowPnt = mc.listAttr(headFollowPntConstr)[-4:]
        for i in range(len(headSpaceFollowOrnt)):
            # set the driven key to 1 and the undriven keys to 0

            CRU.setDriverDrivenValues(ctrlHead, headFollowRot, headFollowOrntConstr, headSpaceFollowOrnt[i], i, 1)
            CRU.setDriverDrivenValues(ctrlHead, headFollowTrans, headFollowPntConstr, headSpaceFollowPnt[i], i, 1)
            for i2 in range(len(headSpaceFollowOrnt)):
                if i2 != i:
                    # need to have the second to last value be i, not i2
                    CRU.setDriverDrivenValues(ctrlHead, headFollowRot, headFollowOrntConstr, headSpaceFollowOrnt[i2], i,
                                              0)
                    CRU.setDriverDrivenValues(ctrlHead, headFollowTrans, headFollowPntConstr, headSpaceFollowPnt[i2], i,
                                              0)

        for i in range(len(headLocArray)):
            mc.setAttr("{0}.v".format(headLocArray[i]), False)

        return headLocArray, locHeadShoulder

    def createJawCtrls(self, jntArrayHead, jntHead, grpHead, *args):

        listCtrls = ["jaw1"]
        headOffsetCtrls = []
        for i in range(len(jntArrayHead)):
            # this is an iteration due to a previous version using that, but I like to keep it flexible
            val = str(jntArrayHead[i])

            if listCtrls[0] in val:
                # if the jaw, do the following
                sizeCtrl = 3
                orntVal = (0, 1, 0)
                # get the length of the bone
                getBoneChild = mc.listRelatives(val, type="joint", ad=True)

                boneLength = mc.getAttr("{0}.ty".format(getBoneChild[0]))
                boneLength2 = mc.getAttr("{0}.ty".format(getBoneChild[1]))
                ctrlJaw = "CTRL_jaw"
                grpJaw = "GRP_" + ctrlJaw

                mc.circle(nr=orntVal, r=sizeCtrl, n=ctrlJaw, degree=3)
                mc.group(ctrlJaw, n=grpJaw)

                # move the GRP_CTRL into position
                todelete = mc.parentConstraint(val, grpJaw)
                mc.delete(todelete)

                # move the CVs into place
                mc.select(ctrlJaw + ".cv[:]")
                mc.rotate(-33, x=True, r=True)

                mc.select(ctrlJaw + ".cv[:]")
                mc.move(0, -boneLength2 * 2.65, boneLength * 1.25, r=True)

                mc.pointConstraint(ctrlJaw, val, mo=True)
                mc.orientConstraint(ctrlJaw, val, mo=True)

        mc.parent(grpJaw, grpHead)
        mc.parentConstraint(jntHead, grpJaw, mo=True)

        return grpJaw, ctrlJaw

    def createEyeControls(self, eyeArray, ctrlHead, ctrlRootTrans, *args):
        # Create eye control
        eyeCtrlArray = []

        eyeGrpArray = []

        eyeRadBase = mc.listRelatives(eyeArray[-1], type="joint")[0]

        radiusBase = mc.getAttr("{0}.tz".format(eyeRadBase))

        for i in range(len(eyeArray)):
            # takes the eye joints, creates a corresponding locator
            eyeName = str(eyeArray[i]).replace("JNT_BND_", "")
            ctrlEye = "CTRL_" + eyeName
            grpEye = "GRP_" + ctrlEye
            eyeCtrlArray.append(mc.spaceLocator(p=(0, 0, 0), name=ctrlEye)[0])

            mc.setAttr('{0}.overrideEnabled'.format(eyeCtrlArray[i]), 1)
            if "_l_" in eyeCtrlArray[i]:
                mc.setAttr("{0}.overrideColor".format(eyeCtrlArray[i]), 14)
            elif "_r_" in eyeCtrlArray[i]:
                mc.setAttr("{0}.overrideColor".format(eyeCtrlArray[i]), 13)

            # groups them at the creation point

            eyeGrpArray.append(mc.group(ctrlEye, name=grpEye))

            # moves the eye into posiiton
            mc.matchTransform(eyeGrpArray[i], eyeArray[i], pos=True, rot=True)

            mc.move(radiusBase * 20, eyeGrpArray[i], z=True, r=True, os=True)

        # Create the eyes control
        eyesCtrlName = "CTRL_eyes"
        eyesCtrl = mc.circle(nr=(0, 1, 0), r=radiusBase * 7.5, n=eyesCtrlName, degree=1, sections=4)[0]

        mc.setAttr("{0}.ry".format(eyesCtrl), 45)
        mc.makeIdentity(eyesCtrl, a=True)  # freeze transform
        mc.setAttr("{0}.sx".format(eyesCtrl), 1.5)
        mc.makeIdentity(eyesCtrl, a=True)  # freeze transform
        mc.setAttr("{0}.rx".format(eyesCtrl), 90)
        mc.makeIdentity(eyesCtrl, a=True)  # freeze transform

        eyesGrp = mc.group(eyesCtrl, n="GRP_" + eyesCtrlName)

        todelete = mc.pointConstraint(eyeCtrlArray, eyesGrp)
        mc.delete(todelete)

        mc.parent(eyeGrpArray, eyesCtrl)
        mc.parent(eyesGrp, ctrlRootTrans)

        aimArray = []
        for i in range(len(eyeArray)):
            aimArray.append(mc.aimConstraint(eyeCtrlArray[i], eyeArray[i], aim=[0, 0, 1]))

        # create the eye follow settings
        eyesFollowLocArray = []

        locFollowHead = "LOC_follow_eyesHead"
        locFollowRoot = "LOC_follow_eyesRoot"

        eyesFollowLocArray.append(mc.spaceLocator(p=(0, 0, 0), name=locFollowHead)[0])
        eyesFollowLocArray.append(mc.spaceLocator(p=(0, 0, 0), name=locFollowRoot)[0])

        # moves the locators into position
        for i in range(len(eyesFollowLocArray)):
            todelete = mc.parentConstraint(eyesCtrl, eyesFollowLocArray[i], mo=False)
            mc.delete(todelete)

        mc.parent(eyesFollowLocArray[0], ctrlHead)

        mc.parent(eyesFollowLocArray[-1], ctrlRootTrans)

        eyesCtrlPrntConst = mc.parentConstraint(eyesFollowLocArray[0], eyesFollowLocArray[1], eyesGrp)[0]
        eyesFollow = 'eyesFollow'
        mc.addAttr(eyesCtrl, longName=eyesFollow, at="enum", enumName="head:root", k=True)

        # The last two attributes would be the relevant head and eye controls
        eyesFollowVals = mc.listAttr(eyesCtrlPrntConst)[-2:]

        CRU.setDriverDrivenValues(eyesCtrl, eyesFollow, eyesCtrlPrntConst, eyesFollowVals[0], 0, 1)
        CRU.setDriverDrivenValues(eyesCtrl, eyesFollow, eyesCtrlPrntConst, eyesFollowVals[0], 1, 0)

        CRU.setDriverDrivenValues(eyesCtrl, eyesFollow, eyesCtrlPrntConst, eyesFollowVals[1], 0, 0)
        CRU.setDriverDrivenValues(eyesCtrl, eyesFollow, eyesCtrlPrntConst, eyesFollowVals[1], 1, 1)

        for i in range(len(eyesFollowLocArray)):
            # hide the eye locators
            mc.setAttr("{0}.v".format(eyesFollowLocArray[i]), False)

        return eyeCtrlArray, eyesCtrl, eyeGrpArray, eyesGrp

    def neckCleanUp(self, jntArray, fkJnts, ikNeckBase, ikNeckEnd, hdlNeck, crvNeck, grpHead, grpNeckFK, ctrlHead,
                    *args):

        # Make the objects invisible
        mc.setAttr("{0}.v".format(ikNeckBase), False)
        mc.setAttr("{0}.v".format(ikNeckEnd), False)
        mc.setAttr("{0}.v".format(hdlNeck), False)
        mc.setAttr("{0}.v".format(crvNeck), False)
        # mc.setAttr("{0}.v".format(jntArray[0]), False)

        grpHeadDNT = "GRP_DO_NOT_TOUCH_head"
        mc.group(n=grpHeadDNT, w=True, em=True)
        parentFK = mc.listRelatives(jntArray[0], p=True)[0]
        mc.parent(grpHeadDNT, parentFK)
        mc.parent(jntArray[0], ikNeckBase, ikNeckEnd, hdlNeck, crvNeck, grpHeadDNT)

        # hide scale on ctrlHead
        CRU.lockHideCtrls(ctrlHead, scale=True)

        # hide translate, scale, radius on FK Control
        CRU.lockHideCtrls(fkJnts[0], scale=True, translate=True)
        CRU.lockHideCtrls(fkJnts[0], theVals=["radi"], channelBox=False, toLock=True, attrVisible=False)

        CRU.lockHideCtrls(grpHead, translate=True, rotate=True, scale=True, visibility=True)
        CRU.lockHideCtrls(grpNeckFK, translate=True, rotate=True, scale=True, visibility=True)
        CRU.lockHideCtrls(ikNeckEnd, translate=True, rotate=True, scale=True, visibility=True)

        CRU.layerEdit(jntArray, bndLayer=True, noRecurse=True)

        altBnds = [x for x in jntArray if "end" in x.lower()]
        CRU.layerEdit(altBnds, bndAltLayer=True, noRecurse=True)
        return grpHeadDNT

    def neckCleanUpExtras(self, cbJaw, grpJaw, ctrlJaw,
                          cbEyes, eyeCtrlArray, eyesCtrl, eyeGrpArray, eyesGrp,
                          grpHeadDNT, jntArrayHead,
                          ikNeckEnd, checkHead,

                          *args):
        if checkHead:
            mc.parent(jntArrayHead[0], grpHeadDNT)

        if cbJaw:
            CRU.lockHideCtrls(grpJaw, translate=True, rotate=True, scale=True, visibility=True)
            CRU.lockHideCtrls(ctrlJaw, translate=True, scale=True, visibility=True)

        if cbEyes:
            # lock and hide the group values for the eyes
            CRU.lockHideCtrls(eyesGrp, translate=True, rotate=True, scale=True, visibility=True)
            for i in range(len(eyeGrpArray)):
                CRU.lockHideCtrls(eyeGrpArray[i], translate=True, rotate=True, scale=True, visibility=True)

            # lock and hide all but the translates for the individual eyes
            for i in range(len(eyeCtrlArray)):
                CRU.lockHideCtrls(eyeCtrlArray[i], rotate=True, scale=True, visibility=True)

            # lock and hide the scale and visible eyes control
            CRU.lockHideCtrls(eyesCtrl, scale=True, visibility=True)
        # I'm just going to hardcode this bit for simplicity's sake

        grpGeoHead = "GRP_GEO_head"
        if mc.objExists(grpGeoHead):
            mc.parentConstraint(ikNeckEnd, grpGeoHead, mo=True)
            mc.parent(grpGeoHead, grpHeadDNT)

        if checkHead:
            altBnds = [x for x in jntArrayHead if "eye" in x.lower() or "jaw1" in x.lower() or "end" in x.lower()]
            CRU.layerEdit(jntArrayHead, bndLayer=True, noRecurse=True)
            CRU.layerEdit(altBnds, bndAltLayer=True, noRecurse=True)

    def toggleStretchTorso(self, locConstNeckShoulder, locHeadShoulder, jntIKShoulder, grpTorsoDNT, jntSpineEnd,
                           ctrlShoulder):
        # create the group
        grpHeadShoulders = "GRP_head_shoulders"
        mc.group(em=True, w=True, n=grpHeadShoulders)
        mc.matchTransform(grpHeadShoulders, jntIKShoulder, pos=True)

        # put it under Do Not Touch torso
        mc.parent(grpHeadShoulders, grpTorsoDNT)

        # parent the locators under it
        mc.parent(locConstNeckShoulder, locHeadShoulder, grpHeadShoulders)

        # creates the spine tip locator which will drive a lot
        locSpineTip = "LOC_spineTip"
        mc.spaceLocator(p=(0, 0, 0), name=locSpineTip)
        mc.matchTransform(locSpineTip, jntSpineEnd)
        mc.parent(locSpineTip, grpTorsoDNT)

        mc.pointConstraint(jntSpineEnd, locSpineTip, mo=True)
        mc.orientConstraint(ctrlShoulder, locSpineTip, mo=True)

        grpPrntConstr = mc.parentConstraint(jntIKShoulder, grpHeadShoulders, mo=True)[0]
        mc.parentConstraint(locSpineTip, grpHeadShoulders, mo=True)

        stretchable = "stretchable"

        grpPrntConstrVals = mc.listAttr(grpPrntConstr)[-2:]
        CRU.setDriverDrivenValues(ctrlShoulder, stretchable, grpPrntConstr, grpPrntConstrVals[0], 0, 0)
        CRU.setDriverDrivenValues(ctrlShoulder, stretchable, grpPrntConstr, grpPrntConstrVals[0], 1, 1)

        CRU.setDriverDrivenValues(ctrlShoulder, stretchable, grpPrntConstr, grpPrntConstrVals[1], 0, 1)
        CRU.setDriverDrivenValues(ctrlShoulder, stretchable, grpPrntConstr, grpPrntConstrVals[1], 1, 0)

        return

    def makeNeckStretchable(self, neckInfo, globalScaleNormalizeDiv, splineStretchNameDiv, ctrlHead):
        # get the default spine length
        defLen = mc.getAttr("{0}.arcLength".format(neckInfo))
        # create the blend node
        neckStretch_blnd = "neck_stretchToggle"
        mc.shadingNode("blendColors", n=neckStretch_blnd, au=True)

        # blend node inputs
        mc.connectAttr("{0}.outputX".format(globalScaleNormalizeDiv), "{0}.color1R".format(neckStretch_blnd))
        mc.setAttr("{0}.color2R".format(neckStretch_blnd), defLen)

        # blend node outputs
        mc.connectAttr("{0}.outputR".format(neckStretch_blnd), "{0}.input1X".format(splineStretchNameDiv), f=True)

        # add the blend nodes
        stretchable = "stretchable"
        mc.addAttr(ctrlHead, longName=stretchable, at="enum", enumName="off:on", k=True)
        mc.setAttr("{0}.{1}".format(ctrlHead, stretchable), 1)
        mc.connectAttr("{0}.{1}".format(ctrlHead, stretchable), "{0}.blender".format(neckStretch_blnd))

        return neckStretch_blnd, stretchable

    def toggleStretchNeck(self, jntEnd, grpHeadDNT, ctrlHead, stretchable, ikNeckEnd, jntHead):

        locNeckTip = "LOC_neckTip"
        mc.spaceLocator(p=(0, 0, 0), name=locNeckTip)

        # parent the jntEnd under grpHeadDNT
        mc.matchTransform(locNeckTip, jntEnd, pos=True)
        mc.parent(locNeckTip, grpHeadDNT)

        # constrain the neck tip
        mc.pointConstraint(jntEnd, locNeckTip)
        mc.orientConstraint(ctrlHead, locNeckTip)

        # the ikNeckEnd will probably have constrained it already
        neckPrntConstr = mc.parentConstraint(ikNeckEnd, jntHead, mo=True)[0]
        mc.parentConstraint(locNeckTip, jntHead, mo=True)

        neckPrntConstrVals = mc.listAttr(neckPrntConstr)[-2:]
        CRU.setDriverDrivenValues(ctrlHead, stretchable, neckPrntConstr, neckPrntConstrVals[0], 0, 0)
        CRU.setDriverDrivenValues(ctrlHead, stretchable, neckPrntConstr, neckPrntConstrVals[0], 1, 1)

        CRU.setDriverDrivenValues(ctrlHead, stretchable, neckPrntConstr, neckPrntConstrVals[1], 0, 1)
        CRU.setDriverDrivenValues(ctrlHead, stretchable, neckPrntConstr, neckPrntConstrVals[1], 1, 0)
        return

    def tgpMakeBC(self, cbGeo=None, cbSpine=None,
                  jntIKShoulderCheck=None, grpTorsoDNTCheck=None,
                  ctrlRootTransCheck=None, bndJnt=None, jntHead=None,
                  ctrlShoulderCheck=None, jntSpineEndCheck=None,
                  cbJaw=None, cbEyes=None,
                  cbTorso=None, cbNeck=None, *args):
        # symmetry = CRU.checkSymmetry()  # we want symmetry turned off for this process
        if cbGeo is None:
            cbGeo = mc.checkBox("selGeo_cb", q=True, v=True)
        if cbSpine is None:
            cbSpine = mc.checkBox("selSpineEnd_cb", q=True, v=True)

        ##########
        # We want to be able to have space switching regardless
        if jntIKShoulderCheck is None:
            jntIKShoulderCheck = mc.textFieldButtonGrp("jntIKShoulderLoad_tf", q=True, text=True)
            passVal = "jntIKShoulderLoad_tf"
        else:
            passVal = None
        jntIKShoulder = CRU.tgpGetTx(jntIKShoulderCheck, passVal, "joint", "IK Shoulder Joint",
                                     ["JNT", "_IK_", "shoulder"])
        if grpTorsoDNTCheck is None:
            grpTorsoDNTCheck = mc.textFieldButtonGrp("grpTorsoDNT_tfbg", q=True, text=True)
            passVal = "grpTorsoDNT_tfbg"
        else:
            passVal = None
        grpTorsoDNT = CRU.tgpGetTx(grpTorsoDNTCheck, passVal, "transform", "Torso DO NOT TOUCH",
                                   ["GRP", "DO", "NOT", "TOUCH"], "group")

        #####
        if ctrlRootTransCheck is None:
            ctrlRootTransCheck = mc.textFieldButtonGrp("rootTrans_tfbg", q=True, text=True)
            passVal = "rootTrans_tfbg"
        else:
            passVal = None
        ctrlRootTrans = CRU.tgpGetTx(ctrlRootTransCheck, passVal, "nurbsCurve", "Root Transform Control",
                                     ["CTRL", "rootTransform"], "control")

        if bndJnt is None or bndJnt == "":
            bndJnt = mc.textFieldButtonGrp("jointLoad_tfbg", q=True, text=True)
            passVal = "jointLoad_tfbg"
        else:
            passVal = None
        bndJnts = CRU.tgpGetJnts(bndJnt, passVal, "joint", "Root Neck Joint", ["JNT", "BND", "neck", "1"])
        checkList = bndJnts
        if checkList is None:
            checkList = [bndJnts]
        if "neck1" not in checkList[0]:
            mc.warning("Make the first selection the root neck joint")
            return

        # gets us most of the geos
        jntArrayNoEnd = [x for x in bndJnts if "End" not in x]
        jntArray = bndJnts[:]
        jntEnd = jntArray[-1]
        #####

        # make sure the selections are not empty

        checkList2 = []
        jntArrayHead = None

        if cbJaw is None:
            cbJaw = mc.checkBoxGrp("attrSelExtra_rbg", q=True, v1=True)
        if cbEyes is None:
            cbEyes = mc.checkBoxGrp("attrSelExtra_rbg", q=True, v2=True)
        if cbJaw or cbEyes:
            checkHead = True
        else:
            checkHead = False

        if cbTorso is None:
            cbTorso = mc.checkBoxGrp("setStretch_rgp", q=True, v1=True)

        if cbNeck is None:
            cbNeck = mc.checkBoxGrp("setStretch_rgp", q=True, v2=True)

        # only include if eyes or jaws
        if checkHead:
            if jntHead is None or jntHead == "":
                jntHead = mc.textFieldButtonGrp("jntHead_tfbg", q=True, text=True)
                passVal = "jntHead_tfbg"

            else:
                passVal = None
            jntHeads = CRU.tgpGetJnts(jntHead, passVal, "joint", "Head Joint", ["JNT", "BND", "head"])
            jntHeads = [x for x in jntHeads if "End" not in x[-3:]]

            jntArrayHead = jntHeads[:]
            checkList2 = jntHeads

            if checkList2 is None:
                checkList2 = [jntHeads]
            if "head" not in checkList2[0]:
                mc.warning("Make the first selection the root head joint")
                return
        if cbEyes:
            eyeArray = [x for x in jntArrayHead if "eye" in x]

        if cbTorso:
            if ctrlShoulderCheck is None:
                ctrlShoulderCheck = mc.textFieldButtonGrp("ctrlShoulderLoad_tf", q=True, text=True)
                passVal = "ctrlShoulderLoad_tf"
            else:
                passVal = None
            ctrlShoulder = CRU.tgpGetTx(ctrlShoulderCheck, passVal, "nurbsCurve", "Shoulder Control",
                                        ["CTRL", "shoulder"], "Control")
            if jntSpineEndCheck is None:
                jntSpineEndCheck = mc.textFieldButtonGrp("jntSpineEndLoad_tf", q=True, text=True)
                passVal = "jntSpineEndLoad_tf"
            else:
                passVal = None
            jntSpineEnd = CRU.tgpGetTx(jntSpineEndCheck, passVal, "joint", "Spine End",
                                       ["JNT", "BND", "spineEnd"])

        jntArrayLen = len(jntArray)

        noUnicode = str(jntEnd)
        jntEndSize = mc.getAttr('{0}.radius'.format(noUnicode))
        if ((checkList[0] == "") or checkList[0] is None):
            mc.warning("You are missing a proper selection!")
            return
        else:

            # CRU.createLocatorToDelete()
            hdlNeck, effNeck, crvNeck = self.createIKSpline(jntArray[0], jntEnd, "neck")
            ikNeckBase, ikNeckEnd, neckIKs = self.createNeckIK(jntArray, jntEnd, jntEndSize, crvNeck)

            self.addIkTwist(hdlNeck, ikNeckBase, ikNeckEnd)

            # creates the head control
            ctrlHead = self.createHeadCtrls(ikNeckEnd)

            # creates the FK and FK control
            ctrlFK, fkJnts = self.createFKJntAndCtrls(jntArray, jntEnd, jntEndSize)

            # creates the group head and
            grpHead = self.createGroupHead(ctrlHead, ikNeckEnd, fkJnts)

            neckInfo, splineStretchNameDiv, globalScaleNormalizeDiv = self.addStretch(jntArray, crvNeck, jntArrayLen,
                                                                                      "neck", ctrlRootTrans, )
            fkJntsStart = fkJnts[0]
            jntArrayStart = jntArray[0]
            self.parentRootTransform(ctrlRootTrans, crvNeck, hdlNeck, ikNeckBase, ikNeckEnd, grpHead, fkJntsStart,
                                     jntArrayStart, )

            # Space Switching Shoulders
            # In case we want to attach it to the body
            locConstNeckShoulder, grpNeckFK = self.createNeckShoulderLoc(cbSpine, jntIKShoulder, ikNeckBase,
                                                                         fkJnts, )
            # to delete test: see if the headGRP is where I'm supposed to be
            # self.createSpaceSwitching(ctrlHead, jntIKShoulder, ctrlRootTrans, fkJnts, grpTorsoDNT)
            headLocArray, locHeadShoulder = self.createSpaceSwitching(grpHead, ctrlHead, jntIKShoulder, ctrlRootTrans,
                                                                      fkJnts, grpTorsoDNT)
            # attach the extra bones to the head
            if checkHead:
                mc.parentConstraint(ikNeckEnd, jntArrayHead[0], mo=True)

            # we can create eyes and jaw
            if cbJaw:
                grpJaw, ctrlJaw = self.createJawCtrls(jntArrayHead, jntHead, grpHead)
            else:
                grpJaw, ctrlJaw = None, None

            if cbEyes:
                eyeCtrlArray, eyesCtrl, eyeGrpArray, eyesGrp, = self.createEyeControls(eyeArray, ctrlHead,
                                                                                       ctrlRootTrans)
            else:
                eyeCtrlArray, eyesCtrl, eyeGrpArray, eyesGrp, = None, None, None, None

            grpHeadDNT = self.neckCleanUp(jntArray, fkJnts, ikNeckBase, ikNeckEnd, hdlNeck, crvNeck, grpHead, grpNeckFK,
                                          ctrlHead)

            if cbTorso:
                self.toggleStretchTorso(locConstNeckShoulder, locHeadShoulder, jntIKShoulder, grpTorsoDNT, jntSpineEnd,
                                        ctrlShoulder)

            if cbNeck:
                neckStretch_blnd, stretchable = self.makeNeckStretchable(neckInfo, globalScaleNormalizeDiv,
                                                                         splineStretchNameDiv, ctrlHead)
                if checkHead:
                    self.toggleStretchNeck(jntEnd, grpHeadDNT, ctrlHead, stretchable, ikNeckEnd, jntHead)

            # it will be easier just to grab the groups above it
            self.neckCleanUpExtras(cbJaw, grpJaw, ctrlJaw,
                                   cbEyes, eyeCtrlArray, eyesCtrl, eyeGrpArray, eyesGrp,
                                   grpHeadDNT, jntArrayHead,
                                   ikNeckEnd, checkHead,
                                   )

            if cbGeo:
                CRU.tgpSetGeo(jntArrayNoEnd, setLayer=True)
                checkHeadExists = ["GEO_l_gland", "GEO_r_gland", "GEO_teethUpper"]
                checkJawExists = ["GEO_teethLower"]

                if checkHead:
                    CRU.tgpSetGeo(jntArrayHead, setLayer=True)
                    setHead = jntHeads[0]
                    if cbJaw:
                        setJaw = [x for x in jntHeads if "jaw" in x.lower()][-1]
                    else:
                        setJaw = jntHeads[0]
                else:
                    setHead = jntArray[-1]
                    setJaw = jntArray[-1]

                for i in range(len(checkHeadExists)):
                    # in case we have some special additions
                    testCheck = checkHeadExists[i]
                    try:
                        mc.parent(testCheck, setHead)
                    except:
                        pass

                for i in range(len(checkJawExists)):
                    testCheck = checkJawExists[i]

                    try:
                        mc.parent(testCheck, setJaw)
                    except:
                        mc.warning("Could not parent {0} under {1}".format(testCheck, setJaw))

            # reset the symmetry to the default because otherwise we might get wonky results
            # mc.symmetricModelling(symmetry=symmetry)
