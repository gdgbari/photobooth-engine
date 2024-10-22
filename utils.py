import os
import platform

def get_asset_path_from_name(asset_name : str) -> str:
    # WARNING: if this function is not in the main folder of the project,
    # it will not work properly
    current_working_dir = os.getcwd()
    output_path = os.path.join(current_working_dir,'Assets')
    output_path = os.path.join(output_path, asset_name)
    return output_path

def get_the_file_in_dir(folder_path :str) :

    files = os.listdir(folder_path)
    files_path = []
    for file_name in files:
        files_path.append(os.path.join(folder_path,file_name))

    return files_path[0], files[0]

def get_name_from_path(file_path :str) -> str:
    return os.path.basename(file_path)

class Platform:
    def __init__(self, platform_name):
        self._platform = platform_name

    def is_wsl(self):
        if self._platform == 'WSL':
            return True
        else:
            return False

    def is_linux(self):
        if self._platform == 'Linux':
            return True
        else:
            return False

    def is_macos(self):
        if self._platform == 'macOS':
            return True
        else:
            return False

def detect_os():
    os_name = platform.system()

    output_obj = None
    if os_name == 'Linux':
        # check if wsl
        if 'microsoft' in platform.release().lower():
            output_obj = Platform('WSL')
        else:
            output_obj = Platform('Linux')
    elif os_name == 'Darwin':
        output_obj = Platform('macOS')
    elif os_name == 'Windows':
        output_obj = Platform('Windows')

    return output_obj


