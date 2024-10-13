# this class get the chosen photo and applies the wanted corner

from PIL import Image


class Tailor:

    def __init__(self, chosen_photo_path: str, chosen_effect_path: str, output_folder_path: str):
        self._photo_path = chosen_photo_path
        self._effect_path = chosen_effect_path
        self._output_folder_path = output_folder_path

    def edit(self, file_name: str):
        file_path = self._output_folder_path + "\\" + file_name
        background = Image.open(self._photo_path)
        foreground = Image.open(self._effect_path)

        background.paste(foreground,(0,0),foreground)

        background.save(file_path, "PNG")

# DEBUG
ph_path = r"C:\Users\User\OneDrive\Desktop\PhotosOFBooth\current\test.jpg"
eff_path = r"C:\Users\User\PycharmProjects\pythonProject\PhotoBooth\Assets\Polaroid - 1.png"
output_f = r"C:\Users\User\OneDrive\Desktop\PhotosOFBooth\output"
tailor = Tailor(ph_path,eff_path,output_f)
tailor.edit("prova.png")