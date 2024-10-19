from SettingsManager import Settings
from FolderManager import FolderManager
from CameraManager import PhotoManager
from UserInteraction import UserInterface
from PhotoTailor import Tailor

import utils

from Runner import Runner

def main():
    print('hello world')

    settings = Settings()
    folders = FolderManager(settings.get_main_folder_path())
    user_interface = UserInterface()

    camera = PhotoManager()
    editor = Tailor()

    # CAMERA
    # end

    # here the photo is in the 'current' folder
    # let's ask the user it is the photo he likes
    photo_path, name = utils.get_the_file_in_dir(folders.get_current_path())
    user_interface.confirm_shot(photo_path, utils.detect_os())
    effect_name = user_interface.choose_polaroid_effect()
    effect_path = utils.get_asset_path_from_name(effect_name)
    # let's edit it
    editor.set_infos(photo_path, effect_path, folders.get_output_folder_path())
    editor.edit(name, folders.get_originals_path())

def new_main():
    runner = Runner()
    runner.prepare()
    while runner.keep_going():
        runner.main_execution()


if __name__ == '__main__':
    main()

