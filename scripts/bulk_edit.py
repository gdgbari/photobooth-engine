import argparse
import os
import sys
from tqdm import tqdm

from core.photo_edit_manager import Tailor

# Add the src directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(project_root, ''))


def find_photos(directory):
    """Finds all image files in a directory."""
    photos = []
    for f in sorted(os.listdir(directory)):
        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            photos.append(os.path.join(directory, f))
    return photos


def check_effect(effect_path):
    return os.path.isfile(effect_path) & effect_path.lower().endswith('.png')


def main():
    parser = argparse.ArgumentParser(description='Bulk edit photos from a directory.')
    parser.add_argument('--input_dir', help='Directory containing photos to edit.',
                        default='/Users/vitodibari/Projects/GDGProjects/photobooth/test/assets/in')
    parser.add_argument('--output_dir', help='Directory to save edited photos.',
                        default='/Users/vitodibari/Projects/GDGProjects/photobooth/test/assets/out')
    parser.add_argument('--frame_path', help='Effect (frame file) path.',
                        default=os.path.join(project_root, 'assets/Milano.png'))
    args = parser.parse_args()

    if not os.path.isdir(args.input_dir):
        print(f"Error: Input directory not found at {args.input_dir}")
        return

    os.makedirs(args.output_dir, exist_ok=True)

    photos = find_photos(args.input_dir)
    if len(photos) < 1:
        print("Error: Empty input directory.")
        return

    effect = args.frame_path
    if not check_effect(effect):
        print(f"Error: No effect found in {args.frame_path}.")
        return

    tailor = Tailor()

    progress_bar = tqdm(photos, desc="Processing photos")
    for photo in progress_bar:
        progress_bar.set_description(f"Processing {os.path.basename(photo)} with effect {os.path.basename(effect)}")
        edited_path = tailor.prepare_single_photo(
            photo,
            effect,
            horizontal_offset=-150
        )
        save_path = os.path.join(args.output_dir, os.path.basename(photo))
        # progress_bar.set_description(f"Processing {os.path.basename(photo)} with effect {os.path.basename(effect)} to {save_path} \n") #log mode
        edited_path.save(save_path)


if __name__ == '__main__':
    main()
