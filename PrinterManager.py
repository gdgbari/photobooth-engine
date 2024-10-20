import os

import utils
from utils import Platform

class PrinterManager:

    def __init__(self, os_platform: Platform):
        self._platform = os_platform

    def print(self, file_path):
        if self._platform.is_linux():
            os.system(f"lp -o media=photo {file_path}")


# DEBUG
printer = PrinterManager(utils.detect_os())
printer.print('/home/gape01/Desktop/main/output/test.jpg')