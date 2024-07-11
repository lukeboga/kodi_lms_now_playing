# Import necessary modules from the Kodi API
import xbmc
from resources.lib.utils.log_message import log_message

def play():
    """
    Initiates playback on the Kodi player using PAPlayer.
    
    This function uses the xbmc.Player class to start playback of the currently selected media item.
    """
    try:
        # Create a new player instance using PAPlayer
        player = xbmc.Player(xbmc.PLAYER_CORE_PAPLAYER)
        # Start playback
        player.play()
        # Log the playback initiation
        log_message("Playback started.")
    except Exception as e:
        # Log any errors encountered during playback initiation
        log_message(f"Error starting playback: {e}", xbmc.LOGERROR)

def stop():
    """
    Stops playback on the Kodi player using PAPlayer.
    
    This function uses the xbmc.Player class to stop the currently playing media.
    """
    try:
        # Create a new player instance using PAPlayer
        player = xbmc.Player(xbmc.PLAYER_CORE_PAPLAYER)
        # Stop playback
        player.stop()
        # Log the playback stop
        log_message("Playback stopped.")
    except Exception as e:
        # Log any errors encountered during playback stop
        log_message(f"Error stopping playback: {e}", xbmc.LOGERROR)

def pause():
    """
    Pauses playback on the Kodi player using PAPlayer.
    
    This function uses the xbmc.Player class to pause the currently playing media.
    """
    try:
        # Create a new player instance using PAPlayer
        player = xbmc.Player(xbmc.PLAYER_CORE_PAPLAYER)
        # Pause playback
        player.pause()
        # Log the playback pause
        log_message("Playback paused.")
    except Exception as e:
        # Log any errors encountered during playback pause
        log_message(f"Error pausing playback: {e}", xbmc.LOGERROR)

def get_current_state():
    """
    Retrieves the current state of the Kodi player using PAPlayer.
    
    This function uses the xbmc.Player class to get the state of the currently playing media,
    including information such as whether it is playing, paused, or stopped.
    
    Returns:
        dict: A dictionary containing the player's state information.
    """
    try:
        # Create a new player instance using PAPlayer
        player = xbmc.Player(xbmc.PLAYER_CORE_PAPLAYER)
        # Retrieve player state
        is_playing = player.isPlaying()
        # Log the player state
        log_message(f"Player is {'playing' if is_playing else 'not playing'}.")
        return {'is_playing': is_playing}
    except Exception as e:
        # Log any errors encountered during state retrieval
        log_message(f"Error retrieving player state: {e}", xbmc.LOGERROR)
        return None

