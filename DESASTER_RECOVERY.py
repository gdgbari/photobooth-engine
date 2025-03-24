from FolderManager import FolderManager
from SettingsManager import Settings
from UserInteraction import UserInterface
import os


def resume_old_session(current_path):
    if len(os.listdir(current_path)) != 0:
        print('maybe some error occured in the last session')
        choice = input('do you want to resume it?')
        if choice == 'y':
            ui = UserInterface()
            return ui.visualize_current_photos(current_path)
        else:
            settings = Settings()
            folder = FolderManager(settings.get_main_folder_path())
            folder.clean_current_path('')
            return False

    return False