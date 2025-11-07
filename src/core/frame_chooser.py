from core.folder_manager import FolderManager, FileNaming, AssetManager
from settings.settings_manager import Settings
from ui.userInteraction import UserInterface
from core.photo_edit_manager import Tailor

import utils.utils as utils
import random


class FrameChooser():

    def __init__(self) -> None:
        self._settings = Settings()
        self._folders = FolderManager(self._settings.get_main_folder_path())
        self._assets = AssetManager()
        self._ui = UserInterface(self._assets.get_corners_names())
        self._editor = Tailor()
        self._SINGLE_FRAME = False
        self._RANDOM_FRAME = True


    def choose_frame(self, photo_path):
        # effect_name = self._ui.choose_polaroid_effect()
        # effect_path = utils.get_asset_path_from_name(effect_name)
        if self._SINGLE_FRAME:
            [effect_path, accepted] = self.show_single_edit(photo_path)
        elif self._RANDOM_FRAME:
            [effect_path, accepted] = self.show_random_edit(photo_path)
        else:
            [effect_path, accepted] = self.choice_edit_with_preview(photo_path)

        return [effect_path, accepted]
            

    def show_random_edit(self, photo_path):
        frames = self._assets.get_corners_names()
        random_frame = random.choice(frames)
        effect_name = random_frame + ".png"
        effect_path = utils.get_asset_path_from_name(effect_name)
        # ugly application to get faster
        # self._ui.show_preview_without_response(self._editor.prepare_single_photo(photo_path,effect_path))
        if self._ui.show_preview_image(self._editor.prepare_single_photo(photo_path, effect_path)):
            return [effect_path, True]
        else:
            return ['', False]


    def show_single_edit(self, photo_path):
        """
        Method which shows the preview of the edited photo with the single effect and returns the effect path if accepted or False if not.
        :param photo_path: photo path to edit
        :return: effect path or False
        """
        

        effect_name = self._assets.get_corners_names()[0]+".png"
        effect_path = utils.get_asset_path_from_name(effect_name)
        # ugly application to get faster
        # self._ui.show_preview_without_response(self._editor.prepare_single_photo(photo_path,effect_path))
        if self._ui.show_preview_image(self._editor.prepare_single_photo(photo_path, effect_path)):
            return [effect_path, True]
        else:
            return ['', False]
        

    def choice_edit_with_preview(self, photo_path):
        '''
        Method which allows the user to choose the effect to apply to the shooted photo with a preview.
        Returns the effect path when the edited photo is accepted.
        :param photo_path: photo path to edit
        :return: effect path
        '''
        # in this case the photo was already accepted in the runner method, so only the edit will be choosen
        # in other words: here the logic to change the photo is not implemented
        while True:
            effect_name = self._ui.choose_polaroid_effect()
            effect_path = utils.get_asset_path_from_name(effect_name)
            if self._ui.show_preview_image(self._editor.prepare_single_photo(photo_path, effect_path)):
                return [effect_path, True]