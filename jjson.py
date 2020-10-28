from json.decoder import JSONDecodeError

import json
import hashlib
import os


def save_json(file, path, name_file):
    while True:
        try:
            with open(path + name_file, 'w') as open_file:
                json.dump(file, open_file, indent=len(file))

                break

        except FileNotFoundError:
                os.makedirs(path)


def save_hash_json(obj, name_attribute, path, name_file, salt):
    hash_obj = hashFor(obj, salt)

    current_json = loading_json(path, name_file)

    config = {}
    if current_json == 'not file':
        config[name_attribute] = hash_obj
        save_json(config, path, name_file)

    else:
        for name in current_json:
            config[name] = current_json[name]

        else:
            config[name_attribute] = hash_obj
            save_json(config, path, name_file)


def loading_json(path, name_file):
    try:
        return json.load(open(path + name_file))

    except FileNotFoundError:
        return 'not file'


def hashFor(data, salt):
    hash_config = hashlib.md5()
    hash_config.update((repr(data) + salt).encode('utf-8'))
    return hash_config.hexdigest()


def remove_file(path, name_file):
    try:
        os.remove(path + name_file)

    except:
        pass