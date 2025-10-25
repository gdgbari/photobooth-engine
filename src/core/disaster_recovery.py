from src.core.FolderManager import FolderManager, AssetManager
from src.settings.SettingsManager import Settings
from src.ui.UserInteraction import UserInterface
import os


def resume_old_session(current_path):
    '''
    This method implements disaster recovery procedure.
    If in the current folder there are some photos, the user is asked if it wants to resume the old session.
    If yes, the photos in the current folder are returned.
    If no, the current folder is cleaned.
    :param current_path: the path of the current folder
    :return: the list of the photos in the current folder if the user wants to resume the old session, False otherwise
    '''
    if len(os.listdir(current_path)) != 0:
        print('maybe some error occured in the last session')
        choice = input('do you want to resume it?')
        if choice == 'y':
            assets = AssetManager()
            ui = UserInterface(assets.get_corners_names())
            return ui.visualize_current_photos(current_path)
        else:
            settings = Settings()
            folder = FolderManager(settings.get_main_folder_path())
            folder.clean_current_path('')
            return False

    return False