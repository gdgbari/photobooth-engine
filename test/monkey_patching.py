# The integration test are executed by monkey patching, 
# we are substituting at runtime some methods with fakes one


import os
from core.runner import Runner
from core.runner import Runner
import core.camera_manager
import fake_functions as fake_functions

def starter():
    runner = Runner()
    runner.prepare()
    while runner.keep_going():
        runner.main_execution()

##########################
# SUBSTITUTING FUNCTIONS # 
##########################

core.camera_manager.PhotoManager.init_camera = fake_functions.fake_start_camera
core.camera_manager.PhotoManager.get_shoot_from_pc = fake_functions.get_fake_shoot

starter()