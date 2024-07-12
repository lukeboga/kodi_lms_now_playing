import xbmc
import xbmcgui

class HelloWorldWindow(xbmcgui.WindowXMLDialog):
    """
    Custom window class for displaying a 'Hello, World!' message.
    """

    def __init__(self, *args, **kwargs):
        super(HelloWorldWindow, self).__init__(*args, **kwargs)

    def onInit(self):
        pass

