import os
import requests

def make_dir_if_not_exist(dir: str) -> None:
    """Checks if provided directory exists and if not, creates it."""
    if not os.path.exists(dir):
        os.makedirs(dir)

def save_image(directory: str, image_file: bytes, image_name: str, image_extension: str) -> None:
    """Saves image to directory."""
    file_path = os.path.join(directory, f'{image_name}{image_extension}')
    f = open(file_path, 'wb')
    f.write(image_file)
    f.close()
    print('Saving image as ' + file_path)

def get_image_from_url(url: str) -> bytes:
    """Retrieve image bytes from given URL."""
    image_file = requests.get(url)
    return image_file.content

