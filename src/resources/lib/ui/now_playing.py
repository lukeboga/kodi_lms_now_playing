import xbmcgui

class NowPlaying(xbmcgui.WindowXML):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def onInit(self):
        # This method is called when the window is initialized
        pass

    def onClick(self, controlId):
        # This method is called when a control is clicked
        pass

    def onAction(self, action):
        # This method is called when an action is performed
        if action == xbmcgui.ACTION_PREVIOUS_MENU or action == xbmcgui.ACTION_NAV_BACK:
            self.close()

