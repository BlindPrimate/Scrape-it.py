import os
import requests
from time import perf_counter

def make_dir_if_not_exist(dir: str) -> None:
    """Checks if provided directory exists and if not, creates it."""
    if not os.path.exists(dir):
        os.makedirs(dir)

def save_image(directory: str, image_file: bytes, image_name: str, image_extension: str) -> None:
    """Saves image to directory."""
    file_path = os.path.join(directory, f'{image_name}{image_extension}')
    print(f'Saving iamge as {file_path}')
    f = open(file_path, 'wb')
    f.write(image_file)
    f.close()

def get_image_from_url(url: str) -> bytes:
    """Retrieve image bytes from given URL."""
    image_file = requests.get(url)
    return image_file.content

def performance_check(func):
    start_t = perf_counter()
    def inner(*args, **kwargs):
        result = func(*args, **kwargs)
        end_t = perf_counter()
        print(func.__name__, end_t-start_t)
        return result
    return inner
