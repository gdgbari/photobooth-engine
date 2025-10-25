from src.settings.SettingsManager import Settings
from src.ui.UserInteraction import UserInterface
from gphoto2 import GPhoto2Error
from src.utils.utils import camera_is_connected

import gphoto2 as gp
import os
import time


'''
PhotoManager is the class which manages the camera operations, such as initialization and photo capturing.
'''

class PhotoManager:

    def __init__(self):
        '''
        Constructor method.
        '''

        self._camera = None
        self._settings_manager = Settings()

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
        '''
        Method which allows to take a photo from the connected camera and save it in the given path with the given name.
        If something goes wrong, the camera is re-initialized and the user is asked to take the photo again by recursion.
        :param path: the path where the photo has to be saved
        :param photo_name: the name of the photo to be saved
        :param user_interactor: the user interactor instance to manage user interactions
        :return: shooted photo path
        '''

        try:
            # print('Capturing image')
            user_interactor.press_to_shot()
            file_path = self._camera.capture(gp.GP_CAPTURE_IMAGE)
            target = os.path.join(path, photo_name)
            # print('Copying image to', target)
            camera_file = self._camera.file_get(
                file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL)
            camera_file.save(target)
            os.chmod(target, 0o777)

            user_interactor.notify_shot_taken()
            # subprocess.call(['xdg-open', target])
            return target
            # print('Camera file path: {0}/{1}'.format(file_path.folder, file_path.name))
        except GPhoto2Error as e:
            print(e)
            print('something went wrong')
            self.init_camera()
            return self.get_shoot_from_pc(path, photo_name, user_interactor)

    def init_camera(self):
        '''
        Method which initializes the camera.
        If something goes wrong, it retries until the camera is connected by recursion.
        '''

        while not camera_is_connected(self._settings_manager):
            print('camera not found. check if it\'s connected and try again')
            time.sleep(2)

        print('camera found')

        try:
            _, camera = gp.gp_camera_new()
            self._camera = camera
            self._camera.init()
        except GPhoto2Error as e:
            print(e)
            self.init_camera()


# DEBUG
#settings = Settings()

#ph_manager = PhotoManager()
#ph_manager.start_camera()
#ph_manager.get_shoot_from_pc(settings.get_main_folder_path())
#ph_manager.stop_camera()