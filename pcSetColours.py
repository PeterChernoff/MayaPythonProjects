import maya.cmds as mc

jointsTU = mc.ls(sl=True, type='joint')

for i in range(len(jointsTU)):
    jointName = jointsTU[i]

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

    mc.setAttr('{0}.overrideEnabled'.format(jointName), 1)
    mc.setAttr("{0}.overrideColor".format(jointName), 20)
