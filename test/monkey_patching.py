# The integration test are executed by monkey patching, 
# we are substituting at runtime some methods with fakes one


import os
from src.core.runner import Runner
from src.core.runner import Runner
import src.core.camera_manager
import test_functions

def starter():
    runner = Runner()
    runner.prepare()
    while runner.keep_going():
        runner.main_execution()

##########################
# SUBSTITUTING FUNCTIONS # 
##########################

src.core.camera_manager.PhotoManager.init_camera = test_functions.fake_start_camera
src.core.camera_manager.PhotoManager.get_shoot_from_pc = test_functions.get_fake_shoot

starter()