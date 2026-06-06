from settings.settings_manager import Settings
from ui.userInteraction import UserInterface
from gphoto2 import GPhoto2Error
from utils import camera_is_connected
import gphoto2 as gp
import os
import time
import shutil


'''
PhotoManager class manages the camera operations, such as initialization and photo capturing.
'''

class PhotoManager:

    def __init__(self):
        self._camera = None
        self._settings_manager = Settings()

    def stop_camera(self):
        if self._settings_manager.get_mock_camera():
            return
        self._camera.exit()

    def get_shoot_from_camera(self, path, photo_name, user_interactor: UserInterface):
        '''
        Method which waits for a photo to be taken from the camera and saves it in the given path with the given name.
        If something goes wrong, the camera is re-initialized and the user is asked to take the photo again by recursion.
        :param path: the path where the photo has to be saved
        :param photo_name: the name of the photo to be saved
        :param user_interactor: the user interactor instance to manage user interactions
        :return: shot photo path
        '''

        if self._settings_manager.get_mock_camera():
            user_interactor.wait_for_camera_shutter()
            target = os.path.join(path, photo_name)
            mock_dir = os.path.join(os.getcwd(), 'test/assets/mock')
            mock_source = os.path.join(mock_dir, 'photo.jpg')
            if not os.path.exists(mock_source) and os.path.exists(mock_dir):
                files = [f for f in os.listdir(mock_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
                if files:
                    mock_source = os.path.join(mock_dir, files[0])
            shutil.copyfile(mock_source, target)
            os.chmod(target, 0o777)
            user_interactor.notify_shot_taken()
            return target

        try:
            user_interactor.wait_for_camera_shutter()
            timeout = 1000 # wait 1s for each event loop

            while True:
                # waits for a camera event
                event_type, event_data = self._camera.wait_for_event(timeout)

                if event_type == gp.GP_EVENT_FILE_ADDED:
                    # a new file is added in the camera
                    folder, file_name = event_data.folder, event_data.name
                    print(f"New photo detected: {file_name} in the folder {folder}")

                    # get the file
                    target = os.path.join(path, photo_name)
                    camera_file = self._camera.file_get(folder, file_name, gp.GP_FILE_TYPE_NORMAL)
                    camera_file.save(target)
                    os.chmod(target, 0o777)

                    # # Introduce a small delay to ensure camera finishes writing to the SD card
                    # time.sleep(1.5)
                    #
                    # # Try to retrieve and save the file (retry up to 3 times if size is 0 or GPhoto2Error occurs)
                    # for attempt in range(3):
                    #     try:
                    #         camera_file = self._camera.file_get(folder, file_name, gp.GP_FILE_TYPE_NORMAL)
                    #         camera_file.save(target)
                    #         if os.path.exists(target) and os.path.getsize(target) > 0:
                    #             break
                    #     except GPhoto2Error as download_err:
                    #         print(f"Attempt {attempt + 1} to retrieve file from camera failed: {download_err}")
                    #     # time.sleep(1.0)

                    user_interactor.notify_shot_taken()

                    return target
        except GPhoto2Error as e:
            print(e)
            print('something went wrong, re-initializing camera')
            self.init_camera()
            return self.get_shoot_from_camera(path, photo_name, user_interactor)

    def get_shoot_from_pc(self, path, photo_name, user_interactor : UserInterface):
        '''
        Method which allows taking a photo from the connected camera and saving it in the given path with the given name.
        If something goes wrong, the camera is re-initialized and the user is asked to take the photo again by recursion.
        :param path: the path where the photo has to be saved
        :param photo_name: the name of the photo to be saved
        :param user_interactor: the user interactor instance to manage user interactions
        :return: shot photo path
        '''

        if self._settings_manager.get_mock_camera():
            user_interactor.press_to_shoot()
            target = os.path.join(path, photo_name)
            mock_dir = os.path.join(os.getcwd(), 'test/assets/mock')
            mock_source = os.path.join(mock_dir, 'photo.jpg')
            if not os.path.exists(mock_source) and os.path.exists(mock_dir):
                files = [f for f in os.listdir(mock_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
                if files:
                    mock_source = os.path.join(mock_dir, files[0])
            shutil.copyfile(mock_source, target)
            os.chmod(target, 0o777)
            user_interactor.notify_shot_taken()
            return target

        try:
            # print('Capturing image')
            user_interactor.press_to_shoot()
            file_path = self._camera.capture(gp.GP_CAPTURE_IMAGE)
            target = os.path.join(path, photo_name)
            
            # # Introduce a small delay to ensure camera finishes writing to the SD card
            # time.sleep(1.5)
            #
            # # Try to retrieve and save the file (retry up to 3 times if size is 0 or GPhoto2Error occurs)
            # for attempt in range(3):
            #     try:
            #         camera_file = self._camera.file_get(
            #             file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL)
            #         camera_file.save(target)
            #         if os.path.exists(target) and os.path.getsize(target) > 0:
            #             break
            #     except GPhoto2Error as download_err:
            #         print(f"Attempt {attempt+1} to retrieve file from PC trigger failed: {download_err}")
            #     time.sleep(1.0)

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
        If something goes wrong, it retries by recursion until the camera is connected.
        '''

        if self._settings_manager.get_mock_camera():
            print("Mock camera enabled. Skipping real camera initialization.")
            return

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