import os

def save_image(directory, image_file, image_name, image_extension):
    file_path = os.path.join(directory, f'{image_name}.{image_extension}')
    f = open(file_path, 'w')
    f.write(image_file)
    f.close()
    print('Saving image as ' + file_path)