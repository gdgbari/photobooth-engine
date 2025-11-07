from settings.settings_manager import Settings
from core.folder_manager import FolderManager, FileNaming, AssetManager
from ui.userInteraction import UserInterface
from core.camera_manager import PhotoManager
from core.disaster_recovery import resume_old_session
from core.photo_edit_manager import Tailor
from core.queue_manager import QueueManager
from settings.settings_manager import Settings
from ui.userInteraction import UserInterface
from core.printer_manager import Printer
from core.frame_chooser import FrameChooser

import os
import utils.utils as utils
import shutil


'''
Runner is the principal class that coordinates all the components of the application.
Here all the managers are instantiated and the main execution loop is implemented.
It provides methods to manage the life cycle of camera, editing and printing.
'''

class Runner:

    def __init__(self):
        '''
        Constructor method.
        '''

        self._settings = Settings()
        self._folders = FolderManager(self._settings.get_main_folder_path())
        self._camera = PhotoManager()
        self._editor = Tailor()
        self._queue = QueueManager()
        self._continue = True
        self._file_naming = FileNaming()
        self._assets = AssetManager()
        self._ui = UserInterface(self._assets.get_corners_names())
        self._frame_choser = FrameChooser()
        # if in asset only one corner is present,
        # there is no need to ask the user every time which one apply
        self._SINGLE_FRAME = False
        self._printer = Printer(self._settings.get_printer_name(), self._settings.get_printer_options())

    def prepare(self):
        '''
        Method which allows to prepare camera, initzialize printing and editing queue and prepare the printer.
        '''

        self._camera.init_camera()
        self._queue.load_queue()
        self._printer.prepare()

        # now check how many corners are present in the assets
        self._SINGLE_FRAME = self._assets.is_frame_single()

    def main_execution(self):
        '''
        Method where disasteer recovery is applied something strange happened in the last session, allowing to resume it.
        If there are many effects in the Assets folder, the user is allowed to choose which one to apply.
        Then the edited photo is shown to the user for confirmation.
        Then the user is asked how many copies of the photo he wants to print.
        At the end if there are 2 or more photos in the printing queue the printing process starts.
        '''

        disaster_has_happened = resume_old_session(self._folders.get_current_path())
        photo_path = ''
        if isinstance(disaster_has_happened, str):
            photo_path = disaster_has_happened
        else:
            [photo_path, _] = self.choice_photo_with_preview()


        [effect_path, photo_accepted] = self._frame_choser.choose_frame(photo_path)
        if not photo_accepted:
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
        '''
        Method which allows the user to take a photo.
        :return: shooted photo path
        '''

        while True:
            file_name = self._file_naming.get_photo_name()
            photo_path = self._camera.get_shoot_from_pc(self._folders.get_current_path(), file_name, self._ui)
            # photo_path = self._camera.get_fake_shoot(self._folders.get_current_path(),self._file_naming.get_photo_name() ,self._ui)

            # photo_path, photo_name = utils.get_the_file_in_dir(self._folders.get_current_path())
            # ATTENTION
            # up to now to make the pipeline faster, the user will not confirm the shoot here but only after the polaroid edit
            # in the future will added granurality
            # if self._ui.confirm_shot(photo_path, utils.detect_os()):
            if True:
                # the photo is accepted, we can go on
                # session has ended
                self._file_naming.increment_session_number()
                return [photo_path, '']
            else:
                shutil.move(os.path.join(self._folders.get_current_path(), file_name), os.path.join(self._folders.get_originals_path(), file_name))
                return False


    def edit(self):
        '''
        Mehod wich gets two photos and their effects from the queues and sends to the editor manager to edit them.
        :return: edited photo path
        '''
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