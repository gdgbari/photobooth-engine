from PIL import Image

import os

import utils

'''
Tailor class gets the chosen photo and applies the wanted effect.
It provides methods to edit photos with the selected effects, add padding, combine paires of photos and edit to have one total photo with 2 polaroids inside.
'''

class Tailor:

    def __init__(self):
        self._photo_path = ''
        self._effect_path = ''
        self._output_folder_path = ''

    def set_infos(self, first_photo: str, first_effect: str,second_photo: str, second_effect: str, output_folder_path: str):
        """
        Information to edit *TWO* photos toghether in a single file
        Preliminary information for processing the single photo (it must be called before the editing of every photo).
        :param first_photo: chosen photo path
        :param first_effect: chosen effect path ( the polaroid file in /assets )
        :param output_folder_path: edited file path

        Future implementation: maybe it will be more elegant to create a class that just edits the photos and another one that marges them togheter
        """

        self._first_photo = first_photo
        self._first_effect = first_effect
        self._second_photo = second_photo
        self._second_effect = second_effect
        self._output_folder_path = output_folder_path

    def _build_output_path(self):
        '''
        Method which build the final path of the combined photo.
        It combines the name of the two photos stored in class parameters.
        Checks the output folder in order to verify if there are other combined photos.
        :return: combined photo path
        '''

        first_photo_name = utils.get_name_from_path(self._first_photo)[:-4]
        second_photo_name = utils.get_name_from_path(self._second_photo)[:-4]
        combined_name = first_photo_name + '-' + second_photo_name
        path = os.path.join(self._output_folder_path, combined_name + '_00.jpg')
        i = 1
        while os.path.exists(path):
            path = os.path.join(self._output_folder_path, combined_name + '_0' + str(i) + '.jpg')
            i += 1
        return path

    def edit(self)-> str:
        """
        Edits the photos
        :param edited_file_name: file name (with extension!), it is not the path,
               it will be the name of the final file
        :return: edited file path, as string
        """

        # DISCUSSION ABOUT THE DIMENSION AND RATIO OF THE IMAGE
        #   analysis on the true height of the polaroid 41+760+10 = 810 -> the height of the background (760) is 93%
        #   true height of the polaroid is 2000 -> the height wanted of the background is 1860

        #   what about the margin? the left and right margin are of 41 px as the upper margin, 41 px is 5% of height
        #   which with our dimension translate to 100 px

        #   the data extrapolated before are from wrong measure
        #   it seems that the correct h of the input image is 1528 px or 76,4 %
        #   it seam that the correct upper margin is 83 px or 4,15 %
        # END OF DISCUSSION

        edited_file_path = self._build_output_path()
        first_photo = self.prepare_single_photo(self._first_photo, self._first_effect)
        second_photo = self.prepare_single_photo(self._second_photo, self._second_effect)
        output_file = self._combine_two_photos(first_photo,second_photo)

        #HERE PADDING
        output_file = self.add_final_padding(output_file, 98)

        output_file.save(edited_file_path, "JPEG")

        # give 777 to edited file
        os.chmod(edited_file_path, 0o777)

        # self._final_cleaning(originals_folder,edited_file_name)
        return edited_file_path

    def _combine_two_photos(self, first_photo: Image, second_photo: Image) -> Image:
        '''
        Method which combines two edited photos into a single one.
        :param first_photo: first edited photo
        :param second_photo: second edited photo
        :return: combined photo
        '''

        output_image = Image.new('RGB', size=(3000,2000)) # right now the output is rotated
        output_image.paste(first_photo, (0, 0))
        output_image.paste(second_photo, (1500, 0))
        # rotate
        output_image = output_image.rotate(90, expand=True)
        return output_image

    def prepare_single_photo(self, photo, effect, horizontal_offset=0) -> Image:
        '''
        Method which edits a single photo with the chosen effect.
        The photo is automatically centered and resized to fit the effect's transparent area.
        :param photo: chosen photo path
        :param effect: chosen effect path (frame with a transparent hole)
        :param horizontal_offset: offset to shift the photo horizontally (positive = right, negative = left)
        :return: edited photo
        '''

        background = Image.open(photo)
        foreground = Image.open(effect)

        # Ensure frame has an alpha channel for transparency
        if foreground.mode != 'RGBA':
            foreground = foreground.convert('RGBA')

        # Find the transparent hole in the frame.
        # We create a mask from the alpha channel where transparent pixels are white.
        alpha = foreground.getchannel('A')
        mask = Image.eval(alpha, lambda a: 255 if a < 128 else 0)
        hole_bbox = mask.getbbox()

        if not hole_bbox:
            raise ValueError("Could not find a transparent hole in the effect frame. The frame must be a PNG with a transparent area for the photo.")

        hole_left, hole_top, hole_right, hole_bottom = hole_bbox
        hole_width = hole_right - hole_left
        hole_height = hole_bottom - hole_top

        # Ensure photo is in a compatible mode
        background = background.convert("RGB")

        # Resize and crop the photo to fill the hole, preserving aspect ratio.
        photo_width, photo_height = background.size

        # Calculate scale factor to "cover" the hole
        scale = max(hole_width / photo_width, hole_height / photo_height)
        new_photo_width = int(photo_width * scale)
        new_photo_height = int(photo_height * scale)
        resized_photo = background.resize((new_photo_width, new_photo_height), Image.Resampling.LANCZOS)

        # Crop the resized photo from the center to match the hole size
        # Apply horizontal offset here
        crop_x = (new_photo_width - hole_width) / 2 - horizontal_offset
        crop_y = (new_photo_height - hole_height) / 2
        
        # Ensure crop coordinates are within bounds (optional, but good practice)
        # If we shift too much, we might go out of bounds. For now, let's just crop.
        # PIL handles out-of-bounds crop by padding with black if I recall correctly, 
        # but usually crop() expects coordinates within the image. 
        # However, since we are resizing to cover, we usually have some slack.
        # Let's just apply the offset.
        
        cropped_photo = resized_photo.crop((crop_x, crop_y, crop_x + hole_width, crop_y + hole_height))

        # Composite the images.
        # Create a new image, paste the cropped photo into the hole, then paste the frame over it.
        output_image = Image.new('RGB', foreground.size)
        output_image.paste(cropped_photo, (hole_left, hole_top))
        output_image.paste(foreground, (0, 0), foreground)

        return output_image

    def add_final_padding(self, image: Image, percentage: int) -> Image:
        '''
        Method which adds a padding to the combined photo.
        :param image: combined photo
        :param percentage: percentage of resizing of the image
        :return: padded photo
        '''

        # i build a background big as the image but of color: #f0f0f0
        # resize the image with percentage
        # put the image onto the background
        img_w, img_h =  image.size
        canvas = Image.new('RGB', (img_w, img_h), (240,240,240))
        resized_w = int(img_w*(percentage/100))
        resized_h = int(img_h*(percentage/100))
        resized_image = image.resize((resized_w,resized_h))
        w_padding = int((img_w - resized_w) /2)
        h_padding = int((img_h - resized_h) /2)
        canvas.paste(resized_image, (w_padding,h_padding))

        return canvas

    # def _final_cleaning(self, originals_folder : str, file_name : str):
        # WARNING: this function is deprecated
        # at the end the file in the current folder has to be moved in the originals folder
        # previous_path = self._photo_path
        # final_path = os.path.join(originals_folder,file_name)
        # shutil.move(previous_path,final_path)


# DEBUG
# ph_path = "/home/gape01/PycharmProjects/photobooth/Assets/test.jpg"
# eff_path = "/home/gape01/PycharmProjects/photobooth/Assets/Polaroid - 1.png"
# output_f = "/home/gape01/Desktop"
# tailor = Tailor(ph_path,eff_path,output_f)
# tailor = Tailor()
# tailor.set_infos('/home/gape01/PycharmProjects/photobooth/Assets/test.jpg',
#                 '/home/gape01/PycharmProjects/photobooth/Assets/Polaroid - 1.png',
#                 '/home/gape01/PycharmProjects/photobooth/Assets/test.jpg',
#                 '/home/gape01/PycharmProjects/photobooth/Assets/Polaroid - 1.png',
#                 '/home/gape01/Desktop/main/output')
#tailor.edit()
# tailor.edit("prova.jpg")