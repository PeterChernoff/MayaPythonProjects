'''
Created on May 30, 2014
for Tin Girl Book and game project

@author: Eyal Assaf
'''
import maya.cmds as mc
# import tgpUtils as ut
from functools import partial


import pcCreateRigAlt00AUtilities
from pcCreateRigAlt00AUtilities import pcCreateRigUtilities as CRU

reload(pcCreateRigAlt00AUtilities)


class pcCreateRigAlt01SpineCode(object):
    def __init__(self, cbGeo=True, cbStretch=True, bndJnt="JNT_BND_spine1"):
        # default passes these values
        self.tgpMakeBC(cbGeo, cbStretch, bndJnt)

    def createIKSpline(self, jntStart, jntEnd, *args):

        ikSpines = mc.ikHandle(n="HDL_spine", sj=jntStart, ee=jntEnd, sol="ikSplineSolver", numSpans=1)

        hdlSpine = ikSpines[0]
        effSpine = ikSpines[1]
        crvSpine = ikSpines[2]

        effSpine = mc.rename(effSpine, "EFF_spine")
        crvSpine = mc.rename(crvSpine, "CRV_spine")

        return hdlSpine, effSpine, crvSpine

    def createSpineIK(self, jntArray, jntEnd, jntEndSize, crvToUse, *args):

        ikHip = mc.duplicate(jntEnd, n="JNT_IK_hip", renameChildren=True)
        mc.parent(ikHip, w=True)
        noUnicode = str(ikHip[0])
        mc.setAttr('{0}.radius'.format(noUnicode), jntEndSize * 3)
        ikShoulder = mc.duplicate(ikHip, n="JNT_IK_shoulder")
        spineIKs = [ikHip[0], ikShoulder[0]]

        # moves the named IK joints into position using constraints, then deletes the constraints
        todelete1 = mc.pointConstraint(jntArray[0], ikHip[0], mo=False)

        mc.delete(todelete1)

        '''
        Bind To: Selected Joints
        Bind Method: Closest Distance
        Skinning Method: Classic Linear
        Normalize Weights: Interactive
        Max Influences  2

        '''
        mc.select(crvToUse, ikShoulder, ikHip)

        # mc.skinCluster (ikHip, ikShoulder, crvSpine, sm=0, nw = 1)

        scls = mc.skinCluster(ikShoulder, ikHip, crvToUse, name='spine_skinCluster', toSelectedBones=True,
                              bindMethod=0, skinMethod=0, normalizeWeights=1, maximumInfluences=2)[0]

        return ikHip[0], ikShoulder[0], spineIKs

    def createIKSpineCtrls(self, spineIKs, *args):

        # create controls for IK Spines
        spineIKCtrls = []
        spineIKSizes = [[8, 18, 22], [6, 15, 20]]

        for i in range(len(spineIKs)):
            spineIKCtrl = CRU.createCTRLsNoOffset(spineIKs[i], 19, prnt=False, colourTU=17,
                                                  boxDimensionsLWH=spineIKSizes[i])
            spineIKCtrlReplace = spineIKCtrl.replace("_IK_", "_")
            mc.rename(spineIKCtrl, spineIKCtrlReplace)
            spineIKCtrls.append(spineIKCtrlReplace)

        # make the neck area more appealing
        '''cvsToMove = mc.select(spineIKCtrls[-1][1] + ".cv[:]")
        mc.rotate(-20, cvsToMove, y=True)
        mc.move(-2, cvsToMove, x=True, r=True, wd=True, ls=True)
        mc.move(2, cvsToMove, z=True, r=True, wd=True, ls=True)'''

        return spineIKCtrls

    def addIkTwist(self, hdlSpine, ikHip, ikShoulder, *args):

        '''
        Set World Up Type to Object Rotation Up (Start/End)
        Set Forward axis to Positive X
        Set Up axis to Negative Z
        Set Up Vector and Up Vector 2 to 0, 0, -1 (Best works if all joints are facing the same direction, and may need to be adjusted)
        Set World Up Object to JNT_IK_hip
        Set World Up Object 2 to JNT_IK_shoulder
        Set Twist Value Type to Start/End.

        '''
        mc.setAttr('{0}.dTwistControlEnable'.format(hdlSpine), True)

        mc.setAttr('{0}.dForwardAxis'.format(hdlSpine), 0)

        mc.setAttr('{0}.dWorldUpType'.format(hdlSpine), 4)
        mc.setAttr('{0}.dWorldUpAxis'.format(hdlSpine), 4)

        mc.setAttr('{0}.dWorldUpVectorX'.format(hdlSpine), 0)
        mc.setAttr('{0}.dWorldUpVectorY'.format(hdlSpine), 0)
        mc.setAttr('{0}.dWorldUpVectorZ'.format(hdlSpine), -1)

        mc.setAttr('{0}.dWorldUpVectorEndX'.format(hdlSpine), 0)
        mc.setAttr('{0}.dWorldUpVectorEndY'.format(hdlSpine), 0)
        mc.setAttr('{0}.dWorldUpVectorEndZ'.format(hdlSpine), -1)

        mc.connectAttr(ikHip + ".worldMatrix[0]", hdlSpine + ".dWorldUpMatrix")
        mc.connectAttr(ikShoulder + ".worldMatrix[0]", hdlSpine + ".dWorldUpMatrixEnd")

        mc.setAttr('{0}.dTwistValueType'.format(hdlSpine), 1)

    def addStretch(self, jntArray, crvSpine, jntArrayLen, *args):
        curveInfo = mc.arclen(crvSpine, ch=True)
        spineInfo = "spineInfo"

        curveInfo = mc.rename(curveInfo, "spineInfo")
        curveLen = mc.getAttr("{0}.arcLength".format(curveInfo))
        spineStretchNameDiv = "spine_stretchPercent_DIV"
        mc.shadingNode("multiplyDivide", n=spineStretchNameDiv, au=True)

        mc.setAttr("{0}.i2x".format(spineStretchNameDiv), curveLen)
        mc.setAttr("{0}.operation".format(spineStretchNameDiv), 2)

        mc.connectAttr("{0}.arcLength".format(curveInfo), "{0}.i1x".format(spineStretchNameDiv))

        # get the scales to the spines

        # to allow for the squash/stretch
        # get square root of output

        spineStretchNamePow = "spine_sqrtStretch_POW"

        mc.shadingNode("multiplyDivide", n=spineStretchNamePow, au=True)
        mc.setAttr("{0}.operation".format(spineStretchNamePow), 3)
        mc.setAttr("{0}.i2x".format(spineStretchNamePow), 0.5)
        mc.connectAttr("{0}.ox".format(spineStretchNameDiv), "{0}.i1x".format(spineStretchNamePow))

        # divide by the square root
        spineStretchNameInv = "spine_stretchInvert_DIV"
        mc.shadingNode("multiplyDivide", n=spineStretchNameInv, au=True)
        mc.setAttr("{0}.operation".format(spineStretchNameInv), 2)
        mc.setAttr("{0}.i1x".format(spineStretchNameInv), 1)
        mc.connectAttr("{0}.ox".format(spineStretchNamePow), "{0}.i2x".format(spineStretchNameInv))

        for i in range(jntArrayLen - 1):
            # connects the spine joints to the joint scale to allow for squash and stretch
            mc.connectAttr("{0}.ox".format(spineStretchNameDiv), "{0}.scaleX".format(jntArray[i]))
            mc.connectAttr("{0}.ox".format(spineStretchNameInv), "{0}.scaleY".format(jntArray[i]))
            mc.connectAttr("{0}.ox".format(spineStretchNameInv), "{0}.scaleZ".format(jntArray[i]))
        return spineInfo, spineStretchNameDiv

    def createFKJntAndCtrls(self, jntArrayLen, jntEndSize, spineIKCtrls, jntArray, *args):

        mc.select(cl=True)
        # create FK joints, then orient them to world
        fkJnts = []
        ctrlFKJntsTU = []
        addFKJnt = False
        grpFKConsts = []
        ctrlFKJntsEnds = []
        for i in range(0, jntArrayLen, 2):
            if i == jntArrayLen - 1:
                lastTerm = "_shoulder"
            elif i == 0:
                lastTerm = "_hip"
            else:
                lastTerm = "_spine{0}".format(i / 2)
                addFKJnt = True

            fkName = "JNT_FK{0}".format(lastTerm)

            pos = mc.xform(jntArray[i], query=True, translation=True, worldSpace=True)
            fkJnts.append(mc.joint(name=fkName, p=pos, rad=jntEndSize * 2))
            mc.joint(fkName, e=True, zso=True, oj="none")
            if addFKJnt:
                ctrlFKJntsTU.append(fkName)

            else:
                # creates the names for GRP_FKConsts
                ctrlFKJntsEnds.append(fkName)
                grpFKConsts.append("GRP_FKConst{0}".format(lastTerm))

            mc.setAttr('{0}.overrideEnabled'.format(fkName), 1)
            mc.setAttr("{0}.overrideColor".format(fkName), 18)

            addFKJnt = False
        # change the rotate order
        CRU.changeRotateOrder(fkJnts, "YZX")

        for i in range(len(grpFKConsts)):
            mc.group(n=grpFKConsts[i], em=True, w=True)
            mc.parent(spineIKCtrls[i], grpFKConsts[i])
        # mc.parentConstraint(ctrlFKJntsEnds[0], grpFKConsts[0], mo=True)
        # mc.parentConstraint(ctrlFKJntsEnds[1], grpFKConsts[1])
        # need the maintain offset on
        for i in range(len(grpFKConsts)):
            mc.parentConstraint(ctrlFKJntsEnds[i], grpFKConsts[i], mo=True)

        # create CTRLs, then parent them appropriately
        ctrlFKJnts = []  # keeps track of the offsets so we can parent them appropriately
        for i in range(len(ctrlFKJntsTU)):
            # Putting into a list so the CTRL sees it properly
            ctrlFK, fkShape = CRU.createCTRLsFKDirect(ctrlFKJntsTU[i], 18, orientVal=(0, 1, 0), colourTU=28)

            ctrlFKJnts.append(ctrlFK)

        cvsToMove = mc.select(ctrlFKJnts[0] + ".cv[:]")
        mc.move(2.5, cvsToMove, z=True, r=True, wd=True, ls=True)

        cvsToMove = mc.select(ctrlFKJnts[-1] + ".cv[:]")
        mc.move(3.5, cvsToMove, z=True, r=True, wd=True, ls=True)

        return fkJnts, ctrlFKJnts, grpFKConsts, ctrlFKJntsEnds

    def createHipCtrl(self, ikHip, spineIKCtrls, *args):
        # create hip controls

        fkHip = mc.duplicate(ikHip, n="JNT_FK_hip")
        # delete the children
        fkHipChilds = mc.listRelatives(fkHip[0], ad=True, f=True)
        mc.delete(fkHipChilds)
        fkHip = fkHip[0]

        fkHipEnd = mc.duplicate(fkHip, n="JNT_FK_hipEnd")[0]
        mc.move(-20, fkHipEnd, y=True, r=True)
        valToMove = mc.getAttr("{0}.ty".format(fkHipEnd))

        mc.parent(fkHipEnd, fkHip)

        fkHipOffsetCtrl = CRU.createCTRLs(fkHip, 27, prnt=True, colourTU=17)
        cvsToMove = mc.select(fkHipOffsetCtrl[1] + ".cv[:]")
        mc.move(-10, cvsToMove, x=True, r=True, wd=True, ls=True)

        mc.parent(fkHipOffsetCtrl[0], spineIKCtrls[0][
            1])
        mc.parent(fkHip, ikHip)

        return fkHip, fkHipOffsetCtrl

    def createBodyCtrl(self, grpFKConsts, ctrlFKJnts, fkJnts, spineIKs, crvSpine, hdlSpine, jntArray, *args):
        # Create body control

        ctrlBody = mc.circle(nr=(1, 0, 0), r=45, n="CTRL_body", degree=1, sections=4)[0]
        cvsToMove = mc.select(ctrlBody + ".cv[:]")
        mc.rotate(45, cvsToMove, x=True)
        mc.select(cl=True)
        toDelete = mc.parentConstraint(jntArray[0], ctrlBody, mo=False)
        mc.delete(toDelete)

        mc.setAttr('{0}.overrideEnabled'.format(ctrlBody), 1)
        mc.setAttr("{0}.overrideColor".format(ctrlBody), 13)
        mc.makeIdentity(ctrlBody, apply=True, t=True, r=True, s=True)
        CRU.changeRotateOrder([ctrlBody], "ZXY")

        grpTorsoName = "GRP_torso"
        grpTorso = mc.group(n=grpTorsoName, em=True, w=True)
        mc.parent(fkJnts[0], jntArray[0], grpFKConsts, crvSpine, hdlSpine, spineIKs, grpTorsoName)

        mc.parentConstraint(ctrlBody, grpTorso, mo=True)

        grpDNT = mc.group(n="GRP_DO_NOT_TOUCH_torso", em=True, w=True)
        mc.parent(grpDNT, grpTorso)
        mc.parent(spineIKs, crvSpine, hdlSpine, jntArray[0], grpDNT)

        mc.setAttr("{0}.inheritsTransform".format(crvSpine), False)

        return ctrlBody, grpTorso

    def createRootTransform(self, ctrlBody, grpTorso, spineInfo, spineStretchNameDiv, *args):
        # we are trying to normalize this value so the spine stretches properly
        rootName = "rootTransform"
        grpRootTransformName = "GRP_" + rootName

        grpRootTransform = mc.group(n=grpRootTransformName, em=True, w=True)
        mc.parent(ctrlBody, grpTorso, grpRootTransform)
        globalScaleNormalizeDiv = "globalScale_spineNormalize_DIV"
        mc.shadingNode("multiplyDivide", n=globalScaleNormalizeDiv, au=True)
        mc.setAttr("{0}.operation".format(globalScaleNormalizeDiv), 2)

        mc.connectAttr("{0}.arcLength".format(spineInfo), "{0}.i1x".format(globalScaleNormalizeDiv))
        mc.connectAttr("{0}.sy".format(grpRootTransformName), "{0}.i2x".format(globalScaleNormalizeDiv))
        # we want to overwrite the old version
        mc.connectAttr("{0}.ox".format(globalScaleNormalizeDiv), "{0}.i1x".format(spineStretchNameDiv), f=True)

        # creates the control
        ctrlRoot, fkShape = CRU.createCTRLsFKDirect(grpRootTransformName, 50, orientVal=(0, 1, 0), colourTU=13,
                                                    addPrefix="CTRL")

        ctrlRootRename = ctrlRoot.replace("_GRP_", "_")
        ctrlRoot = mc.rename(ctrlRoot, ctrlRootRename)
        CRU.layerEdit(ctrlRoot, bodyLayer=True, noRecurse=True, colourTU=13)

        CRU.lockHideCtrls(ctrlRoot, visibility=True)

        return globalScaleNormalizeDiv

    def spineCleanup(self, ctrlFKJnts, ctrlFKJntsEnds, grpFKConsts, grpTorso, ctrlBody, spineIKs, spineIKCtrls,
                     crvSpine, hdlSpine, jntArray, *args):  # lock attributes

        # lock the translate/scale for the control joints
        for i in range(len(ctrlFKJnts)):
            CRU.lockHideCtrls(ctrlFKJnts[i], translate=True, scale=True, visibility=True)
            CRU.lockHideCtrls(ctrlFKJnts[i], theVals=["radi"], channelBox=False, toLock=True, attrVisible=False)

        # lock everything for the other fk bones
        for i in range(len(ctrlFKJntsEnds)):
            CRU.lockHideCtrls(ctrlFKJntsEnds[i], translate=True, scale=True, rotate=True, visibility=True)
            CRU.lockHideCtrls(ctrlFKJntsEnds[i], theVals=["radi"], channelBox=False, toLock=True, attrVisible=False)

        # lock everything except visibility for grpTorso
        CRU.lockHideCtrls(grpTorso, translate=True, scale=True, rotate=True, )

        # lock everything for the grpFK Consts
        for i in range(len(grpFKConsts)):
            CRU.lockHideCtrls(ctrlFKJntsEnds[i], translate=True, scale=True, rotate=True, visibility=True)

        # lock and hide the scale and visibility for everything else
        CRU.lockHideCtrls(ctrlBody, scale=True, visibility=True)

        for i in range(len(spineIKs)):
            CRU.lockHideCtrls(spineIKs[i], scale=True)

        for i in range(len(spineIKCtrls)):
            CRU.lockHideCtrls(spineIKCtrls[i], visibility=True, scale=True)

        mc.setAttr('{0}.v'.format(crvSpine), False)
        mc.setAttr('{0}.v'.format(hdlSpine), False)

        CRU.lockHideCtrls(crvSpine, visibility=True)
        CRU.lockHideCtrls(hdlSpine, visibility=True)

        CRU.layerEdit(ctrlFKJnts, fkLayer=True, noRecurse=True, colourTU=CRU.clrBodyFK)
        CRU.layerEdit(ctrlFKJntsEnds, fkLayer=True, noRecurse=True, colourTU=CRU.clrBodyFK)
        CRU.layerEdit(spineIKCtrls, ikLayer=True, noRecurse=True, colourTU=CRU.clrBodyIK)
        CRU.layerEdit(jntArray, bndLayer=True, noRecurse=True, layerState=1)

        altBnds = [x for x in jntArray if "end" in x.lower()]
        CRU.layerEdit(altBnds, bndAltLayer=True, noRecurse=True, layerState=1)

        CRU.layerEdit(ctrlBody, bodyLayer=True, noRecurse=True, colourTU=CRU.clrBodyMain)

    def makeSpineStretchable(self, spineIKCtrls, globalScaleNormalizeDiv, spineStretchNameDiv, spineInfo):
        ctrlShoulder = spineIKCtrls[1]  # gonna be using the CTRL_spine a lot
        # get the default spine length
        defLen = mc.getAttr("{0}.arcLength".format(spineInfo))
        # create the blend node
        torsoStretch_blnd = "torso_stretchToggle"
        mc.shadingNode("blendColors", n=torsoStretch_blnd, au=True)

        # blend node inputs
        mc.connectAttr("{0}.outputX".format(globalScaleNormalizeDiv), "{0}.color1R".format(torsoStretch_blnd))
        mc.setAttr("{0}.color2R".format(torsoStretch_blnd), defLen)

        # blend node outputs
        mc.connectAttr("{0}.outputR".format(torsoStretch_blnd), "{0}.input1X".format(spineStretchNameDiv), f=True)

        # add the blend nodes
        stretchable = "stretchable"
        mc.addAttr(ctrlShoulder, longName=stretchable, at="enum", enumName="off:on", k=True)
        mc.setAttr("{0}.{1}".format(ctrlShoulder, stretchable), 1)
        mc.connectAttr("{0}.{1}".format(ctrlShoulder, stretchable), "{0}.blender".format(torsoStretch_blnd))

        return

    def tgpMakeBC(self, cbGeo=None, cbStretch=None, bndJnt=None, *args):
        symmetry = CRU.checkSymmetry()  # we want symmetry turned off for this process
        if cbGeo is None:
            cbGeo = mc.checkBox("selGeo_cb", q=True, v=True)
        if cbStretch is None:
            cbStretch = mc.checkBox("selStretch_cb", q=True, v=True)

        if bndJnt is None or bndJnt == "":
            bndJnt = mc.textFieldButtonGrp("jointLoad_tfbg", q=True, text=True)
            passVal = "jointLoad_tfbg"

        else:
            passVal = None
        bndJnts = CRU.tgpGetJnts(bndJnt, passVal, "joint", "Root Spine BND", ["JNT", "_BND_", "spine", "1"])

        # make sure the selections are not empty
        checkList = [bndJnts]

        if ((checkList[0] == "") or checkList[0] is None):
            mc.warning("You are missing a proper selection!")
            return
        else:
            # CRU.createLocatorToDelete()
            # create the IK base controls
            jntArray = bndJnts[:]
            jntStart = jntArray[0]
            jntEnd = jntArray[-1]

            noUnicode = str(jntEnd)
            jntEndSize = mc.getAttr('{0}.radius'.format(noUnicode))

            # gets values for later use
            jntArrayLen = len(jntArray)

            # IK Spline Handle
            hdlSpine, effSpine, crvSpine = self.createIKSpline(jntStart, jntEnd)

            # Create the IK joints
            ikHip, ikShoulder, spineIKs = self.createSpineIK(jntArray, jntEnd, jntEndSize, crvSpine)

            # Creating the IK Spine Controls:
            # bind the curve to the JNT IKs,
            spineIKCtrls = self.createIKSpineCtrls(spineIKs)

            # Rotation orders

            spineOrder = [ikHip, ikShoulder]
            spineOrder.extend(spineIKCtrls)

            CRU.changeRotateOrder(spineOrder, "ZXY")
            # we don't parent the values initially to avoi
            for i in range(len(spineIKCtrls)):
                mc.parentConstraint(spineIKCtrls[i], spineOrder[i], mo=True)

            # Adding the IK twist
            self.addIkTwist(hdlSpine, ikHip, ikShoulder, )

            # FK Joints and Controls
            fkJnts, ctrlFKJnts, grpFKConsts, ctrlFKJntsEnds = self.createFKJntAndCtrls(jntArrayLen, jntEndSize,
                                                                                       spineIKCtrls, jntArray)

            # Adding an extra hip control
            # fkHip, fkHipOffsetCtrl = self.createHipCtrl(ikHip, spineIKCtrls)

            # Torso squash and stretch
            spineInfo, spineStretchNameDiv = self.addStretch(jntArray, crvSpine, jntArrayLen, )

            # Torso Global Transform
            ctrlBody, grpTorso = self.createBodyCtrl(grpFKConsts, ctrlFKJnts, fkJnts, spineIKs, crvSpine, hdlSpine,
                                                     jntArray)

            # clean up, but we don't include certain bits of data
            self.spineCleanup(ctrlFKJnts, ctrlFKJntsEnds, grpFKConsts, grpTorso, ctrlBody, spineIKs, spineIKCtrls,
                              crvSpine, hdlSpine, jntArray)

            # Root Transform Node
            # we don't clean this one up yet
            globalScaleNormalizeDiv = self.createRootTransform(ctrlBody, grpTorso, spineInfo, spineStretchNameDiv)

            if cbStretch:
                self.makeSpineStretchable(spineIKCtrls, globalScaleNormalizeDiv, spineStretchNameDiv, spineInfo)

            # make the last thing we do the geometry
            if cbGeo:
                CRU.tgpSetGeo(jntArray, "JNT_BND_", setLayer=True)
                try:
                    CRU.tgpSetGeo([spineIKs[0]], "JNT_IK_", setLayer=True)
                    # mc.parent("GEO_hip", ikHip)
                except:
                    mc.warning("Hip geometry either does not exist or is not properly named")

        mc.select(ctrlFKJntsEnds[0])

        # reset the symmetry to the default because otherwise we might get wonky results
        # mc.symmetricModelling(symmetry=symmetry)
