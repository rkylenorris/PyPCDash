from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

def set_app_volume(app_name, volume):
    """Sets the volume of a specific application.

    Args:
        app_name (str): Name of the application to control.
        volume (float): Volume level between 0.0 and 1.0.
    """

    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        if session.Process:
            if app_name.lower() in session.Process.name().lower():
                volume_interface = session.SimpleAudioVolume
                volume_interface.SetMasterVolume(volume, None)
                break


def get_audio_sessions():
    sessions = AudioUtilities.GetAllSessions()
    process_volumes = []
    for session in sessions:
        if session.Process:
            if session.Process.name().lower() in session.Process.name().lower():
                interface = session.SimpleAudioVolume
                process_volumes.append({"process": session.Process.name().lower(), "volume": round(interface.GetMasterVolume() * 100)})
                print(process_volumes)

    return process_volumes


if __name__ == "__main__":
    # app_name = "spotify.exe"  # Replace with the name of your application
    # volume = 1.  # Set volume to 50%
    # set_app_volume(app_name, volume)
    # print(get_audio_sessions())

    from ctypes import cast, POINTER
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    vol = volume.GetMasterVolumeLevelScalar() * 100
    vol_str = f"{vol:.0f}"
    print(vol_str)
