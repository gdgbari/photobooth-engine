from utils import Platform
import os
import subprocess
import utils


class PrinterManager:

    def __init__(self, os_platform: Platform):
        self._platform = os_platform

    def prepare(self):
        if self._platform.is_linux():
            # deve esserci cups e gutenprint
            def is_installed(package_name):
                try:
                    subprocess.run(["dpkg-query", "-W", package_name], check=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
                    return True
                except subprocess.CalledProcessError:
                    return False
            def install_package(package_name):
                try:
                    subprocess.run(["sudo", "apt-get", "install", "-y", package_name], check=True)
                except subprocess.CalledProcessError as e:
                    print(f"Errore durante l'installazione di {package_name}: {e}")

            if not is_installed("cups"):
                install_package("cups")

            if not is_installed("printer-driver-gutenprint"):
                install_package("printer-driver-gutenprint")

    def print(self, file_path):
        if self._platform.is_linux():
            # os.system(f"lp -o media=photo {file_path}")
            os.system(f'lp -o media=Custom.150x100mm {file_path}')
            os.system(f"lp -o media=photo {file_path}")
            return 'all right'
        elif self._platform.is_wsl():
            # proviamo ad utilizzare il tool USBIPD-WIN
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
            windows_file_path = 'C:\\Users\\gassi\\Desktop\\main\\test.jpg'
            linux_file_path = '/mnt/c/Users/gassi/Desktop/main/output/test.jpg'
            printer_name = 'EPSON Stylus DX7400 Series'
            command = [
                'powershell.exe',
                '-Command',
                f'Start-Process -FilePath "{windows_file_path}" -Verb Print -ArgumentList "-PrinterName \'{printer_name}\'"'
            ]
            command1 = [
                "powershell.exe",
                "-Command",
                f'lpr -S localhost -P "{printer_name}" "{windows_file_path}"'
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
# printer.print('/mnt/c/Users/gassi/Desktop/main/output/test.jpg')
# printer.print('/home/gape01/Desktop/main/output/test.jpg')
printer.prepare()
printer.print('/home/gape01/Desktop/main/output/DEVFESTBA_0003_01-DEVFESTBA_0003_01_00.jpg')
# typo
