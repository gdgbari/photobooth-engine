# The integration tests are executed by monkey patching,
# we are substituting at runtime some methods with fake ones


import os
from photobooth.core.runner import Runner
import photobooth.core.camera_manager as camera_manager
import fake_functions as fake_functions


def starter():
    runner = Runner()
    runner.prepare()
    while runner.keep_going():
        runner.main_execution()


##########################
# SUBSTITUTING FUNCTIONS #
##########################

camera_manager.PhotoManager.init_camera = fake_functions.fake_start_camera
camera_manager.PhotoManager.get_shoot_from_pc = fake_functions.get_fake_shoot

starter()