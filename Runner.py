from SettingsManager import Settings
from FolderManager import FolderManager, FileNaming
from UserInteraction import UserInterface
from CameraManager import PhotoManager
from PhotoTailor import Tailor
from QueueManager import QueueManager

import utils

class Runner:

    def __init__(self):
        self._settings = Settings()
        self._folders = FolderManager(self._settings.get_main_folder_path())
        self._ui = UserInterface()
        self._camera = PhotoManager()
        self._editor = Tailor()
        self._queue = QueueManager()
        self._continue = True
        self._file_naming = FileNaming()

    def prepare(self):
        self._camera.start_camera()
        self._queue.load_queue()


    def main_execution(self):
        while True:
            self._camera.get_shoot_from_pc(self._folders.get_current_path(), self._file_naming.get_photo_name(), self._ui)
            # self._camera.get_fake_shoot(self._folders.get_current_path(),self._file_naming.get_photo_name() ,self._ui)
            self._file_naming.increment_session_number()
            photo_path, photo_name = utils.get_the_file_in_dir(self._folders.get_current_path())
            if self._ui.confirm_shot(photo_path, utils.detect_os()):
                # the photo is accepted, we can go on
                break
        # effect_name = self._ui.choose_polaroid_effect()
        # effect_path = utils.get_asset_path_from_name(effect_name)
        effect_path = self.choice_edit_with_preview(photo_path)

        times = self._ui.choose_times_to_print()
        # the photo is added to the queue and the folder get cleared
        self._queue.add_photo(self._folders.clean_current_path(photo_path),times)
        self._queue.add_edit(effect_path,times)

        while self._queue.queue_is_ready(): # if there are 2 or more photos in queue then start to edit
            self.edit(photo_path, effect_path)

    def choice_edit_with_preview(self, photo_path):
        while True:
            effect_name = self._ui.choose_polaroid_effect()
            effect_path = utils.get_asset_path_from_name(effect_name)
            if self._ui.show_preview_image(self._editor.prepare_single_photo(photo_path,effect_path)):
                return effect_path


    def edit(self, photo_path, effect_path):
        # let's edit it
        photo_list = self._queue.get_two_photos()
        edit_list = self._queue.get_two_edit()
        self._editor.set_infos(photo_list[0], edit_list[0], photo_list[1],edit_list[1],self._folders.get_output_folder_path())
        # get the name of the last file ... ( this will need an update )
        # edit the queue then clean the folder
        joined_photo = self._editor.edit() # there was a redundancy with the usage of "clean_current_path" method, given that at this point there won't be any image in "current" folder
        print(joined_photo)
        return joined_photo

    def keep_going(self):
        # here in the future a more complex solution
        return self._continue

    def final_cleaning(self):
        self._camera.stop_camera()
        self._queue.dismiss()