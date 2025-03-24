from SettingsManager import Settings
from FolderManager import FolderManager, FileNaming
from UserInteraction import UserInterface
from CameraManager import PhotoManager
from PhotoTailor import Tailor
from QueueManager import QueueManager
from new_print import print_image

from DESASTER_RECOVERY import resume_old_session

import utils
import os
import shutil

class Runner:

    def __init__(self):
        self._settings = Settings()
        self._folders = FolderManager(self._settings.get_main_folder_path())
        self._ui = UserInterface(self._settings.get_polaroid_effects)
        self._camera = PhotoManager()
        self._editor = Tailor()
        self._queue = QueueManager()
        self._continue = True
        self._file_naming = FileNaming()
        # if in asset only one corner is present,
        # there is no need to ask the user every time which one apply
        self._SINGLE_CORNER = False

    def prepare(self):
        self._camera.start_camera()
        self._queue.load_queue()

        # now check how many corners are present in the assets



    def main_execution(self):
        disaster_has_happened = resume_old_session(self._folders.get_current_path())
        photo_path = ''
        if isinstance(disaster_has_happened, str):
            photo_path = disaster_has_happened
        else:
            [photo_path, photo_name] = self.choice_photo_with_preview()

        # effect_name = self._ui.choose_polaroid_effect()
        # effect_path = utils.get_asset_path_from_name(effect_name)
        effect_path = self.choice_edit_with_preview(photo_path)

        times = self._ui.choose_times_to_print()
        # the photo is added to the queue and the folder get cleared
        self._queue.add_photo(self._folders.clean_current_path(photo_path),times)
        self._queue.add_edit(effect_path,times)

        while self._queue.queue_is_ready(): # if there are 2 or more photos in queue then start to edit
            path_to_print=self.edit(photo_path, effect_path) # actually there is no more the need to declare here this paths
            print_image(path_to_print)

    def choice_photo_with_preview(self):
        while True:
            file_name = self._file_naming.get_photo_name()
            photo_path = self._camera.get_shoot_from_pc(self._folders.get_current_path(), file_name, self._ui)
            # self._camera.get_fake_shoot(self._folders.get_current_path(),self._file_naming.get_photo_name() ,self._ui)

            # photo_path, photo_name = utils.get_the_file_in_dir(self._folders.get_current_path())
            if self._ui.confirm_shot(photo_path, utils.detect_os()):
                # the photo is accepted, we can go on
                # session has ended
                self._file_naming.increment_session_number()
                return [photo_path, '']
            else:
                shutil.move(os.path.join(self._folders.get_current_path(), file_name), os.path.join(self._folders.get_originals_path(), file_name))



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
        joined_photo = self._editor.edit()
        print(joined_photo)
        return joined_photo

    def keep_going(self):
        # here in the future a more complex solution
        return self._continue

    def final_cleaning(self):
        self._camera.stop_camera()
        self._queue.dismiss()