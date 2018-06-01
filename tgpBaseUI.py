import maya.cmds as mc
from functools import partial


class BaseUI(object):
    def __init__(self):

        self.widget = {}
        self.window = "baseWindow"
        self.title = "Base Window"

        self.winSize = (500, 350)

        self.createUI()

    def createUI(self, *args):

        self.topLeftCorner = [0, 0]  # allows me to edit the prefs
        # check if window and prefs exist. If yes, delete.
        if mc.window(self.window, exists=True):
            mc.deleteUI(self.window, window=True)
        if mc.windowPref(self.window, exists=True):  # making slight adjustment here in keeping the topleft corner
            self.topLeftCorner = mc.windowPref(self.window, query=True, topLeftCorner=True)
            mc.windowPref(self.window, remove=True)

        # create the main window UI
        self.window = mc.window(self.window, title=self.title,
                                widthHeight=self.winSize,
                                sizeable=False, menuBar=True,
                                mnb=True, mxb=False, topLeftCorner=self.topLeftCorner)  # modifying

        # mc.windowPref(self.window, topLeftCorner=self.windowPosition)
        self.mainForm = mc.formLayout(numberOfDivisions=100)

        self.tagLine = mc.text(label="UI Test")
        self.mainColumnLayout = mc.columnLayout(rs=5, bgc=(0.21, 0.21, 0.21))

        # attach UI elemetns to mainFOrm layout
        mc.formLayout(self.mainForm, edit=True,
                      attachForm=(
                          (self.mainColumnLayout, "top", 0),
                          (self.mainColumnLayout, "right", 0),
                          (self.mainColumnLayout, "left", 0),
                          (self.mainColumnLayout, "bottom", 30),
                          (self.tagLine, "left", 0),
                          (self.tagLine, "right", 0)
                      ),

                      attachControl=(
                          (self.tagLine, "top",
                           10, self.mainColumnLayout)
                      )
                      )

        # create custom UI elements
        self.createCustom(self)

        mc.setParent("..")

        # CONSIDER USING IF NECESSARY

        self.createCommon(self)
        mc.setParent("..")

        # show the window
        mc.showWindow(self.window)

    def createCommon(self, *args):
        # create common UI elements for all class instances
        # create default buttons
        self.cmdButtonsSize = ((self.winSize[0] - 30) / 2, 30)

        self.createButton = mc.button(label="Create",
                                      width=self.cmdButtonsSize[0],
                                      height=self.cmdButtonsSize[1],
                                      command=partial(self.createButtonCmd)
                                      )

        self.cancelButton = mc.button(label="Cancel",
                                      width=self.cmdButtonsSize[0],
                                      height=self.cmdButtonsSize[1],
                                      command=self.cancelButtonCmd
                                      )

        mc.formLayout(self.mainForm, e=True, af=([self.createButton, "left", 5],
                                                 [self.createButton, "bottom", 35],
                                                 [self.cancelButton, "right", 5],
                                                 [self.cancelButton, "bottom", 35]
                                                 ),
                      ac=([self.cancelButton, "left", 5,
                           self.createButton])
                      )
        return

    def createCustom(self, *args):
        # create custom UI elements per class instance

        print ("Custom window")

    def createButtonCmd(self, *args):

        # override create command
        print("Button")

    def cancelButtonCmd(self, *args):

        # close the window
        mc.deleteUI(self.window, window=True)
