# The integration test are executed by monkey patching, 
# we are substituting at runtime some methods with fakes one


import os
from src.core.Runner import Runner
import src.core.CameraManager
import src.test.test_functions

def starter():
    runner = Runner()
    runner.prepare()
    while runner.keep_going():
        runner.main_execution()

##########################
# SUBSTITUTING FUNCTIONS # 
##########################

src.core.CameraManager.PhotoManager.start_camera = src.test.test_functions.fake_start_camera
src.core.CameraManager.PhotoManager.get_shoot_from_pc = src.test.test_functions.get_fake_shoot

starter()