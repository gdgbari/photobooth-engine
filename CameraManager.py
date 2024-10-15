import gphoto2 as gp
import os
# let's be honest, the library chosen is a complete mess, the author himself said that:
# " it should not be used in a pythonic way "

# even if the following class may appear as a mere wrapper,
# it is suggested its use since it permit a later tuning


class PhotoManager:
    def __init__(self):
        creation_error, camera = gp.gp_camera_new()
        self._camera = camera

    def start_camera(self):
        # maybe later here could be added a loop in case the usb cave got detached
        self._camera.init()

    def stop_camera(self):
        self._camera.exit()

    def get_shoot(self, download_path):
        timeout = 5000
        try:
            print("waiting for a shoot...")
            while True:
                # waits for a camera event
                event_type, event_data = self._camera.wait_for_event(timeout)

                if event_type == gp.GP_EVENT_FILE_ADDED:
                    # a new file is added in the camera
                    folder, file_name = event_data.folder, event_data.name
                    print(f"New photo detected: {file_name} in the folder {folder}")

                    # get the file
                    file_path = os.path.join(download_path, file_name)
                    camera_file = self._camera.file_get(folder, file_name, gp.GP_FILE_TYPE_NORMAL)
                    camera_file.save(file_path)


                    return file_path
        finally:
            print('nothing detected')