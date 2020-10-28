from json.decoder import JSONDecodeError

import json
import hashlib
import os


class Config():
    def __init__(self, name_config, path_folder, param_dict=None):
        self.name_config = name_config + '.json'
        self.path_folder = path_folder
        self.param_dict = param_dict
        self.name_attribute = self.path_folder + self.name_config
        self.config = None
        self.salt = 'saltrandom'

        # self.loading_config()

    def set_name_config(self, name_config):
        self.name_config = name_config + '.json'
        self.name_attribute = self.path_folder + self.name_config

    def set_path_folder(self, path_folder):
        self.path_folder = path_folder
        self.name_attribute = self.path_folder + self.name_config

    def set_param_dict(self, param_dict):
        self.param_dict = param_dict

    def set_salt(self, salt, mode='update'):
        self.salt = salt

        if mode == 'update':
            self.loading_config()

    def get_name_config(self):
        return self.name_config[:-5]

    def get_path_folder(self):
        return self.path_folder

    def get_param_dict(self):
        return self.param_dict

    def get_config(self):
        return self.config

    def save_config(self):
        save_json(self.param_dict, self.path_folder, self.name_config)
        save_hash_json(self.param_dict, self.name_attribute, self.path_folder, '.hash.json', self.salt)

    def loading_config(self):
        while True:
            self.config = loading_json(self.path_folder, self.name_config)

            if self.config == 'not file':
                self.save_config()

            elif self.config == None:
                print('Error, not dict')
                return

            else:
                hash_config = loading_json(self.path_folder, '.hash.json')
                if hash_config[self.name_attribute] == hashFor(self.config, self.salt):
                    return self.config

                elif hash_config == 'not file':
                    remove_file(self.path_folder, self.name_config)
                    continue

                else:
                    remove_file(self.path_folder, self.name_config)
                    continue


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
    os.remove(path + name_file)