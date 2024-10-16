import os
import shutil
import requests

# copied from game directory


dialogue_splitter = ' &lt;:&gt; '

resource_folder = 'tale/web/resources/'
static_folder = 'static/resources'

def split_text(text: str) -> list:
    separated = text.split(dialogue_splitter)
    if len(separated) != 2:
        separated = text.split(' <:> ')
    if len(separated) != 2:
        return None, text
    name = separated[0]
    content = separated[1]
    return name, content

def find_image(image_name: str, path: str) -> str:
    if not path.startswith('http'):
        path = os.path.join(path, resource_folder)
    if _check_file_exists(image_name + '.gif', path):
        return path + image_name + '.gif'
    elif _check_file_exists(image_name + '.png', path):
        return path + image_name + '.png'
    elif _check_file_exists(image_name + '.jpg', path):
        return path + image_name + '.jpg'
    print(f'No image found for {image_name}.')
    return ''

def _check_file_exists(filename: str, path: str) -> bool:
    if 'http' in path:
        r = requests.get(os.path.join(path, filename))
        return r.status_code == 200
    else:
        return os.path.exists(os.path.join(path, filename))
    