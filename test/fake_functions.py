#######################################
# METHODS FOR MONKEY PUNCHING TESTING #
#######################################
import os
import shutil
from ui.userInteraction import UserInterface

def get_fake_shoot(self, path, photo_name, user_interactor : UserInterface):
    user_interactor.press_to_shot()
    file_path = './test/assets/photo.jpg'
    # file_name = input('input file name:')
    target = os.path.join(path, photo_name)
    shutil.copyfile(file_path, target)
    return target
    
def fake_start_camera(self):
    return