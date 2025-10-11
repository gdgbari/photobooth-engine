from src.settings.SettingsManager import Settings
from src.core.FolderManager import FolderManager, FileNaming, AssetManager
from src.ui.UserInteraction import UserInterface
from src.core.CameraManager import PhotoManager
from src.core.disaster_recovery import resume_old_session
from src.core.FolderManager import FolderManager, FileNaming
from src.core.PhotoCompManager import Tailor
from src.core.QueueManager import QueueManager
from src.settings.SettingsManager import Settings
from src.ui.UserInteraction import UserInterface
from src.core.PrinterManager import Printer

import os
import src.utils.utils as utils
import shutil

class Runner:

    def __init__(self):
        self._settings = Settings()
        self._folders = FolderManager(self._settings.get_main_folder_path())
        self._camera = PhotoManager()
        self._editor = Tailor()
        self._queue = QueueManager()
        self._continue = True
        self._file_naming = FileNaming()
        self._assets = AssetManager()
        self._ui = UserInterface(self._assets.get_corners_names())
        # if in asset only one corner is present,
        # there is no need to ask the user every time which one apply
        self._SINGLE_FRAME = False
        self._printer = Printer(self._settings.get_printer_name(), self._settings.get_printer_options())

    def prepare(self):
        self._camera.init_camera()
        self._queue.load_queue()
        self._printer.prepare()

        # now check how many corners are present in the assets
        self._SINGLE_FRAME = self._assets.is_frame_single()

    def main_execution(self):
        disaster_has_happened = resume_old_session(self._folders.get_current_path())
        photo_path = ''
        if isinstance(disaster_has_happened, str):
            photo_path = disaster_has_happened
        else:
            [photo_path, _] = self.choice_photo_with_preview()

        # effect_name = self._ui.choose_polaroid_effect()
        # effect_path = utils.get_asset_path_from_name(effect_name)
        if self._SINGLE_FRAME:
            effect_path = self.show_single_edit(photo_path)
        else:
            effect_path = self.choice_edit_with_preview(photo_path)

        # ugly implementation of a faster pipeline
        # TODO: make effect_path be path or None Instead of path or False
        if isinstance(effect_path, bool):
            if not effect_path:
                # clean the folder
                self._folders.clean_current_path(photo_path)
                return

        times = self._ui.choose_times_to_print()
        # the photo is added to the queue and the folder get cleared
        self._queue.add_photo(self._folders.clean_current_path(photo_path), times)
        self._queue.add_edit(effect_path, times)

        while self._queue.queue_is_ready(): # if there are 2 or more photos in queue then start to edit
            path_to_print=self.edit() # actually there is no more the need to declare here this paths
            self._printer.print_image(path_to_print)

    def choice_photo_with_preview(self):
        while True:
            file_name = self._file_naming.get_photo_name()
            photo_path = self._camera.get_shoot_from_pc(self._folders.get_current_path(), file_name, self._ui)
            # photo_path = self._camera.get_fake_shoot(self._folders.get_current_path(),self._file_naming.get_photo_name() ,self._ui)

            # photo_path, photo_name = utils.get_the_file_in_dir(self._folders.get_current_path())
            # if self._ui.confirm_shot(photo_path, utils.detect_os()):
            if True:
                # the photo is accepted, we can go on
                # session has ended
                self._file_naming.increment_session_number()
                return [photo_path, '']
            else:
                shutil.move(os.path.join(self._folders.get_current_path(), file_name), os.path.join(self._folders.get_originals_path(), file_name))
                return False

    def show_single_edit(self, photo_path):
        """
        In case a single effect is proposed, there is no need to let thte user choice
        """
        effect_name = self._assets.get_corners_names()[0]+".png"
        effect_path = utils.get_asset_path_from_name(effect_name)
        # ugly application to get faster
        # self._ui.show_preview_without_response(self._editor.prepare_single_photo(photo_path,effect_path))
        if self._ui.show_preview_image(self._editor.prepare_single_photo(photo_path, effect_path)):
            return effect_path
        else:
            return False

    def choice_edit_with_preview(self, photo_path):
        while True:
            effect_name = self._ui.choose_polaroid_effect()
            effect_path = utils.get_asset_path_from_name(effect_name)
            if self._ui.show_preview_image(self._editor.prepare_single_photo(photo_path, effect_path)):
                return effect_path


    def edit(self):
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
