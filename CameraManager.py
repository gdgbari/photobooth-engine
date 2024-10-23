import gphoto2 as gp
import os
import shutil
from SettingsManager import Settings
from UserInteraction import UserInterface


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
        # WARNING, from now on the following is deprecated
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

    def get_shoot_from_pc(self, path, photo_name, user_interactor : UserInterface):
        user_interactor.press_to_shot()
        # print('Capturing image')
        file_path = self._camera.capture(gp.GP_CAPTURE_IMAGE)
        # print('Camera file path: {0}/{1}'.format(file_path.folder, file_path.name))
        target = os.path.join(path, photo_name)
        # print('Copying image to', target)
        camera_file = self._camera.file_get(
            file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL)
        camera_file.save(target)
        os.chmod(target, 0o777)

        user_interactor.notify_shot_taken()
        #subprocess.call(['xdg-open', target])
        return target

    def get_fake_shoot(self, path, photo_name, user_interactor : UserInterface):
        user_interactor.press_to_shot()
        # file_path = '/mnt/c/Users/gassi/Desktop/main/test.jpg'
        file_path = '/mnt/d/project/main/test.jpg'
        # file_name = input('input file name:')
        target = os.path.join(path, photo_name)
        shutil.copyfile(file_path, target)
        return target


# DEBUG
#settings = Settings()

#ph_manager = PhotoManager()
#ph_manager.start_camera()
#ph_manager.get_shoot_from_pc(settings.get_main_folder_path())
#ph_manager.stop_camera()