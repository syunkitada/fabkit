# coding: utf-8

import os
import yaml
from lib import conf


def set(key_path, value):
    key, data_file = __get_key_file(key_path)
    data_dir = os.path.dirname(data_file)

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    databag = get_databag(key_path)
    databag.update({key: value})

    with open(data_file, 'w') as f:
        yaml.dump(databag, f)

    return


def get(key_path):
    splited_key = key_path.rsplit('.', 1)
    databag = get_databag(key_path)
    return databag[splited_key[1]]


def get_databag(key_path):
    key, data_file = __get_key_file(key_path)
    print key
    print data_file

    if os.path.exists(data_file):
        with open(data_file, 'r') as f:
            data = yaml.load(f)
    else:
        data = {}

    return data


def __get_key_file(key_path):
    splited_key = key_path.rsplit('.', 1)
    if len(splited_key) == 1:
        print 'key\'s format is [filepath].[keyname]'
        print 'e.g. common/database/mysql.password'
        return

    data_file = splited_key[0] + '.yaml'
    data_file = os.path.join(conf.DATABAG_DIR, data_file)
    key = splited_key[1]
    return key, data_file


def decode_str(value):
    splited_value = value.split('{%')
    if len(splited_value) > 1:
        result = ''
        for value in splited_value:
            splited_key = value.split('%}')
            if len(splited_key) > 1:
                key = splited_key[0]
                result += get(key) + splited_key[1]
            else:
                result += value

        return result
    else:
        return value