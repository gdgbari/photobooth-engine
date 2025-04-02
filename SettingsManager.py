# Manager of the yaml file
# why do we even need all of this? It's a good practice because it's easier to add granularity

import yaml


class Settings:

    def __init__(self):
        self._settings_path = "./settings.yaml"

    def get_main_folder_path(self) -> str:
        with open(self._settings_path, 'r') as yaml_file:
            yaml_dict = yaml.safe_load(yaml_file)

        return yaml_dict['main_folder_path']

    def get_cam_name(self) -> str:
        with open(self._settings_path, 'r') as yaml_file:
            yaml_dict = yaml.safe_load(yaml_file)

        return yaml_dict['cam_name']


# DEBUG SECTION
# settings = Settings()
# print(settings.get_main_folder_path())
# print(settings.get_polaroid_effects())
# effect_dict = settings.get_polaroid_effects()
# print(type(effect_dict))
