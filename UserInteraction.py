from PIL import Image
from utils import Platform
import subprocess
import os

# I choose to use this functions in a class because then transitioning to a GUI will be easier

class UserInterface:

    def choose_polaroid_effect(self) -> str:
        effect_list = ['Gemini', 'Flutter', 'Android', 'Firebase', 'Kotlin', 'Angular',
                       'Cloud', 'Jetpack Compose', 'TensorFlow', 'ARCore']

        print('Choose which effect to apply')

        while True:
            index = 1
            for effect_name in effect_list:
                print(f'[{index}]: {effect_name}')
                index = index + 1

            chosen_edit = input('pick a number: ')
            if chosen_edit.isdigit():
                chosen_edit = int(chosen_edit)
                if 0 < chosen_edit <= 10:
                    print('alright')
                    break

            print('Some error occurred, please try again')

        file_name = 'Polaroid - ' + str(chosen_edit) + '.png'
        return file_name

    def confirm_shot(self, photo_path, os_platform: Platform) -> bool:
        if os_platform.is_linux():
            # image = Image.open(photo_path)
            # image.show()
            subprocess.run(["xdg-open", photo_path])
        elif os_platform.is_wsl():
            windows_path = subprocess.check_output(['wslpath', '-w', photo_path]).decode().strip()
            subprocess.run(['powershell.exe', 'Start-Process', windows_path])
        elif os_platform.is_macos():
            # maybe in the future this will change
            # image = Image.open(photo_path)
            # image.show()
            user = os.getlogin()
            # Comando per aprire l'immagine come utente normale
            comando = ["sudo", "-u", user, "open", photo_path]
            # Esegui il comando
            subprocess.run(comando)
        elif os_platform.is_wsl():
            windows_path = subprocess.check_output(['wslpath', '-w', photo_path]).decode().strip()
            subprocess.run(['powershell.exe', 'Start-Process', windows_path])

        while True:
            print('Do you like it? y/n')

            decision = input('choose: ')

            if decision == 'y':
                return True
            elif decision == 'n':
                return False

            print('Some error occurred, please try again')

    def choose_times_to_print(self) -> int:
        """
        Choose how many times a photo get printed
        :return: the number of times the photo get printed
        """
        print('How many copies of the photo do you want to print?')
        while True:
            times = input('choose between 1 up to 99: ')
            if times.isdigit():
                times = int(times)
                if 0 < times <= 99:
                    while  True:
                        print('you choose '+str(times)+' copies, is it correct?')
                        ui_input = input('y/n: ')
                        if ui_input.lower() == 'y':
                            print('all right')
                            return times
                        elif ui_input.lower() == 'n':
                            break
            print('Some error occurred, please try again')


    def press_to_shot(self):
        input('press any key to shoot')

    def notify_shot_taken(self):
        print('shot taken')

    def show_preview_image(self, previw_img: Image):
        print('here the edit')
        previw_img.show()
        print('do you like it?')
        while True:
            choiche = input('y/n: ')
            if choiche == 'y':
                return True
            elif choiche == 'n':
                return False
            else:
                print('some error occured')

    def show_new_session_menu(self):
        while True:
            print(
                "Hoy many photos do wou want to shoot? Please choose a number between 1 and 5 (Press 0 if you want to recover precedent photos)")
            choice = int(input("Enter your choice: "))
            if 0 <= choice <= 5:
                return choice

            print("Please enter a valid choice")


