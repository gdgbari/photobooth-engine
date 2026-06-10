import yaml

"""
Settings is the class which manages the settings.yaml file.
"""


class Settings:

    def __init__(self):
        self._settings_path = "./settings.yaml"

    def get_main_folder_path(self) -> str:
        """
        Method which returns the main folder path set in settings.yaml file.
        :return: main folder path
        """

        with open(self._settings_path, 'r') as yaml_file:
            yaml_dict = yaml.safe_load(yaml_file)
        return yaml_dict['main_folder_path']

    def get_printer_name(self) -> str:
        """
        Method which returns the printer name set in settings.yaml file.
        :return: printer name
        """

        with open(self._settings_path, 'r') as yaml_file:
            yaml_dict = yaml.safe_load(yaml_file)
        return yaml_dict['printer_name']

    def get_printer_options(self) -> dict:
        with open(self._settings_path, 'r') as yaml_file:
            yaml_dict = yaml.safe_load(yaml_file)
        return yaml_dict.get('printer_options', {})

    def get_cam_name(self) -> str:
        """
        Method which returns the camera name set in settings.yaml file.
        :return: camera name
        """

        with open(self._settings_path, 'r') as yaml_file:
            yaml_dict = yaml.safe_load(yaml_file)

        return yaml_dict['cam_name']

    def get_camera_connection(self) -> str:
        """
        Method which returns the camera connection type (usb or ptpip) set in settings.yaml file.
        :return: camera connection type
        """

        with open(self._settings_path, 'r') as yaml_file:
            yaml_dict = yaml.safe_load(yaml_file)

        return yaml_dict.get('camera_connection', 'usb')

    def get_camera_ip(self) -> str:
        """
        Method which returns the camera IP address set in settings.yaml file.
        :return: camera IP address
        """

        with open(self._settings_path, 'r') as yaml_file:
            yaml_dict = yaml.safe_load(yaml_file)

        return yaml_dict.get('camera_ip', '192.168.1.1')

    def get_backend_url(self) -> str:
        with open(self._settings_path, 'r') as yaml_file:
            yaml_dict = yaml.safe_load(yaml_file)

        return yaml_dict['backend']

    def get_event_name(self) -> str:
        """
        Method which returns the event name set in settings.yaml file.
        :return: event name
        """

        with open(self._settings_path, 'r') as yaml_file:
            yaml_dict = yaml.safe_load(yaml_file)

        return yaml_dict['event_name']

    def get_print_size(self) -> str:
        """
        Method which returns the print size set in settings.yaml file.
        :return: print size
        """

        with open(self._settings_path, 'r') as yaml_file:
            yaml_dict = yaml.safe_load(yaml_file)

        return yaml_dict.get('print_size', '4x6')  # Defaults to 4x6 if not specified

    def get_client_secret(self) -> str:
        """
        Method which returns the client secret set in settings.yaml file.
        :return: client secret
        """

        with open(self._settings_path, 'r') as yaml_file:
            yaml_dict = yaml.safe_load(yaml_file)

        return yaml_dict.get('client_secret', '')

    def get_capture_mode(self) -> str:
        """
        Method which returns the capture mode (pc or camera) set in settings.yaml file.
        :return: capture mode
        """

        with open(self._settings_path, 'r') as yaml_file:
            yaml_dict = yaml.safe_load(yaml_file)

        return yaml_dict.get('capture_mode', 'pc')  # Defaults to pc if not specified

    def get_mock_camera(self) -> bool:
        with open(self._settings_path, 'r') as yaml_file:
            yaml_dict = yaml.safe_load(yaml_file)
        return yaml_dict.get('mock_camera', False)

    def get_mock_printer(self) -> bool:
        with open(self._settings_path, 'r') as yaml_file:
            yaml_dict = yaml.safe_load(yaml_file)
        return yaml_dict.get('mock_printer', False)

    def get_enable_hotfolder(self) -> bool:
        with open(self._settings_path, 'r') as yaml_file:
            yaml_dict = yaml.safe_load(yaml_file)
        return yaml_dict.get('enable_hotfolder', False)

    def get_hotfolder_path(self) -> str:
        with open(self._settings_path, 'r') as yaml_file:
            yaml_dict = yaml.safe_load(yaml_file)
        return yaml_dict.get('hotfolder_path', '')

    def get_min_num_photos(self) -> int:
        with open(self._settings_path, 'r') as yaml_file:
            yaml_dict = yaml.safe_load(yaml_file)
        return yaml_dict.get('min_num_photos', 1)

    def get_max_num_photos(self) -> int:
        with open(self._settings_path, 'r') as yaml_file:
            yaml_dict = yaml.safe_load(yaml_file)
        return yaml_dict.get('max_num_photos', 99)
