# Import necessary modules from the Kodi API
import xbmc
import xbmcgui
import sys

# Main entry point for the addon
def main():
    """
    The main function serves as the entry point for the addon.
    It loads a simple window from an XML file by default.
    """
    show_simple_window()

# Function to show a simple window using an XML file
def show_simple_window():
    """
    Opens a window using the simple XML file to display 'Hello World' text.
    """
    window = xbmcgui.WindowXML('simplewindow.xml', 'plugin.audio.klmsaddon', 'default')
    window.doModal()
    del window

# If this script is executed directly, call the main function
if __name__ == '__main__':
    main()

