import yaml
import os

'''
Settings is the class which manages the settings.yaml file.
'''

class Settings:

    def __init__(self):
        self._settings_path = "./settings.yaml"

    def get_main_folder_path(self) -> str:
        '''
        Method wich returns the main folder path setted in settings.yaml file.
        :return: main folder path
        '''

        with open(self._settings_path, 'r') as yaml_file:
            yaml_dict = yaml.safe_load(yaml_file)
        return yaml_dict['main_folder_path']

    def get_printer_name(self) -> str:
        '''
        Method wich returns the printer name setted in settings.yaml file.
        :return: printer name
        '''

        with open(self._settings_path, 'r') as yaml_file:
            yaml_dict = yaml.safe_load(yaml_file)
        return yaml_dict['printer_name']

    def get_printer_options(self) -> dict:
        with open(self._settings_path, 'r') as yaml_file:
            yaml_dict = yaml.safe_load(yaml_file)

    def get_cam_name(self) -> str:
        '''
        Method wich returns the camera name setted in settings.yaml file.
        :return: camera name
        '''

        with open(self._settings_path, 'r') as yaml_file:
            yaml_dict = yaml.safe_load(yaml_file)

        return yaml_dict['cam_name']
    

    def get_backend_url(self) -> str:
        with open(self._settings_path, 'r') as yaml_file:
            yaml_dict = yaml.safe_load(yaml_file)

        return yaml_dict['backend']

    def get_event_name(self) -> str:
        '''
        Method wich returns the event name setted in settings.yaml file.
        :return: event name
        '''

        with open(self._settings_path, 'r') as yaml_file:
            yaml_dict = yaml.safe_load(yaml_file)

        return yaml_dict['event_name']
    
    def get_print_size(self) -> str:
        '''
        Method which returns the print size setted in settings.yaml file.
        :return: print size
        '''

        with open(self._settings_path, 'r') as yaml_file:
            yaml_dict = yaml.safe_load(yaml_file)

        return yaml_dict.get('print_size', '4x6') # Defaults to 4x6 if not specified
    
    def get_assets_path(self) -> str:
        '''
        Method which returns the path to the assets folder.
        :return: assets folder path
        '''
        return os.path.join(self._project_root, "assets")

        '''if 'printer_settings' in yaml_dict:
            settings = yaml_dict['printer_settings']
            if list(settings.keys()) == ['']:
                return None
            return settings

        return None'''


# DEBUG SECTION
# settings = Settings()
# print(settings.get_main_folder_path())
# print(settings.get_polaroid_effects())
# effect_dict = settings.get_polaroid_effects()
# print(type(effect_dict))