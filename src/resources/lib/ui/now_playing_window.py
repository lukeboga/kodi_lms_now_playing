import xbmc
import xbmcgui

class NowPlayingWindow(xbmcgui.WindowXML):
    def __init__(self, *args, **kwargs):
        """
        Initialize the NowPlayingWindow with optional arguments.
        
        Parameters:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super(NowPlayingWindow, self).__init__(*args, **kwargs)
        self.now_playing = kwargs.get('now_playing', {})

    def onInit(self):
        """
        Method called when the window is initialized.
        """
        self.update_now_playing_info()

    def update_now_playing_info(self):
        """
        Update the window with the 'now playing' information.
        """
        # Update the labels with 'now playing' information
        self.getControl(1001).setLabel(self.now_playing.get('title', 'Unknown Title'))
        self.getControl(1002).setLabel(self.now_playing.get('artist', 'Unknown Artist'))
        self.getControl(1003).setLabel(self.now_playing.get('album', 'Unknown Album'))

    def onClick(self, controlId):
        """
        Method called when a control is clicked.
        
        Parameters:
            controlId (int): The ID of the control that was clicked.
        """
        pass

    def onAction(self, action):
        """
        Method called when an action is performed.
        
        Parameters:
            action (xbmcgui.Action): The action that was performed.
        """
        if action == xbmcgui.ACTION_CLOSE:
            self.close()

