from SettingsManager import Settings
from FolderManager import FolderManager
from UserInteraction import UserInterface
from CameraManager import PhotoManager
from PhotoTailor import Tailor

import utils

class Runner:

    def __init__(self):
        self._settings = Settings()
        self._folders = FolderManager(self._settings.get_main_folder_path())
        self._ui = UserInterface()
        self._camera = PhotoManager()
        self._editor = Tailor()
        self._continue = True

    def prepare(self):
        self._camera.start_camera()

    def main_execution(self):
        while True:
            self._camera.get_shoot_from_pc(self._folders.get_current_path(), self._ui)
            photo_path, photo_name = utils.get_the_file_in_dir(self._folders.get_current_path())
            if self._ui.confirm_shot(photo_path, utils.detect_os()):
                # the photo is accepted, we can go on
                break

        effect_name = self._ui.choose_polaroid_effect()
        effect_path = utils.get_asset_path_from_name(effect_name)
        # let's edit it
        self._editor.set_infos(photo_path, effect_path, self._folders.get_output_folder_path())
        self._editor.edit(photo_name, self._folders.get_originals_path())

    def keep_going(self):
        # here in the future a more complex solution
        return self._continue

    def final_cleaning(self):
        self._camera.stop_camera()