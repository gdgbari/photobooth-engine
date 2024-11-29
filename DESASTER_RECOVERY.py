import os
from UserInteraction import UserInterface
from FolderManager import FolderManager
from SettingsManager import Settings


def resume_old_session(current_path):
    if len(os.listdir(current_path)) != 0:
        print('maybe some error occured in the last session')
        choihce = input('do you want to resume it?')
        if choihce == 'y':
            ui = UserInterface()
            return ui.visualize_current_photos(current_path)
        else:
            settings = Settings()
            folder = FolderManager(settings.get_main_folder_path())
            folder.clean_current_path('')
            return False

    return False