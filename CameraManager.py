import gphoto2 as gp
import os
from SettingsManager import Settings


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

    def get_shoot_from_pc(self, path):
        input('press any key to shoot')
        print('Capturing image')
        file_path = self._camera.capture(gp.GP_CAPTURE_IMAGE)
        print('Camera file path: {0}/{1}'.format(file_path.folder, file_path.name))
        target = os.path.join(path, file_path.name)
        print('Copying image to', target)
        camera_file = self._camera.file_get(
            file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL)
        camera_file.save(target)
        #subprocess.call(['xdg-open', target])
        return target

# DEBUG
settings = Settings()

ph_manager = PhotoManager()
ph_manager.start_camera()
ph_manager.get_shoot_from_pc(settings.get_main_folder_path())
ph_manager.stop_camera()