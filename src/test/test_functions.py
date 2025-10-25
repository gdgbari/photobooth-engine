#######################################
# METHODS FOR MONKEY PUNCHING TESTING #
#######################################

from src.ui.UserInteraction import UserInterface

import os
import shutil


def get_fake_shoot(self, path, photo_name, user_interactor : UserInterface):
    user_interactor.press_to_shot()
    file_path = './src/test/test.jpg'
    # file_name = input('input file name:')
    target = os.path.join(path, photo_name)
    shutil.copyfile(file_path, target)
    return target

def fake_start_camera(self):
    return