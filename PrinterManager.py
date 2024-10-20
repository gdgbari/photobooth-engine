import os
import subprocess
import utils
from utils import Platform

class PrinterManager:

    def __init__(self, os_platform: Platform):
        self._platform = os_platform

    def print(self, file_path):
        if self._platform.is_linux():
            os.system(f"lp -o media=photo {file_path}")
        elif self._platform.is_wsl():

            def wsl_to_windows_path(wsl_path):
                """
                Converte un percorso WSL in un percorso Windows.

                :param wsl_path: Il percorso in formato WSL.
                :return: Il percorso convertito in formato Windows.
                """
                if wsl_path.startswith('/mnt/'):
                    # Rimuovi '/mnt/' e sostituisci '/' con '\'
                    windows_path = wsl_path.replace('/mnt/', 'C:\\').replace('/', '\\')
                    return windows_path

            # windows_file_path = wsl_to_windows_path(file_path)
            windows_file_path = 'C:\\Users\\gassi\\Desktop\\main\\output\\test.jpg'
            printer_name = 'EPSON Stylus DX7400 Series'
            command = [
                'powershell.exe',
                '-Command',
                f'Start-Process -FilePath "{windows_file_path}" -Verb Print -ArgumentList "-PrinterName \'{printer_name}\'"'
            ]
            # Visualizza il comando per il debug
            print("Eseguendo il comando:", " ".join(command))

            try:
                # Esegui il comando
                result = subprocess.run(command, capture_output=True, text=True)
                if result.returncode == 0:
                    print(
                        f"Stampa inviata con successo per il file: {windows_file_path} sulla stampante {printer_name}")
                else:
                    print(f"Errore durante la stampa: {result.stderr}")
            except Exception as e:
                print(f"Un errore inaspettato è avvenuto: {e}")




# DEBUG
printer = PrinterManager(utils.detect_os())
printer.print('/mnt/c/Users/gassi/Desktop/main/output/test.jpg')