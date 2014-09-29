# coding: utf-8
#
# This module do initial configuration.
# And provide setting value that read the configuration file.

import os
import sys
import ConfigParser
from fabric.api import env
import uuid
import logging
from logging.handlers import RotatingFileHandler
from logging import StreamHandler


# setup fabric env
env.forward_agent = True
env.use_ssh_config = True
env.warn_only = True
env.colorize_errors = True

env.is_test = False
env.is_chef = False

STDOUT_LOG_FILE = 'stdout.log'

# for prefix of tmpfile
UUID = uuid.uuid4()


# append module dir to sys.path
def init(chefrepo_dir=None, test_chefrepo_dir=None):
    env.cmd_history = []  # for debug

    global CONFIG
    global CHEFREPO_DIR, TEST_CHEFREPO_DIR
    global STORAGE_DIR, LOG_DIR, PACKAGE_DIR, CHEF_RPM, TMP_CHEF_RPM
    global FABSCRIPT_MODULE, FABSCRIPT_MODULE_DIR
    global COOKBOOKS_DIRS, NODE_DIR, ROLE_DIR, ENVIRONMENT_DIR
    global FABLIB_MODULE_DIR, FABLIB_MAP
    global LOGGER_LEVEL, LOGGER_FORMATTER, NODE_LOGGER_MAX_BYTES, NODE_LOGGER_BACKUP_COUNT
    global CHEF_CLIENT_PACKAGES

    if test_chefrepo_dir:
        TEST_CHEFREPO_DIR = test_chefrepo_dir
    if chefrepo_dir:
        CHEFREPO_DIR = chefrepo_dir
    elif TEST_CHEFREPO_DIR:
        if TEST_CHEFREPO_DIR not in sys.path:
            sys.path.remove(CHEFREPO_DIR)
            sys.path.append(TEST_CHEFREPO_DIR)
        CHEFREPO_DIR = TEST_CHEFREPO_DIR

    # complement to absolute path from path relative to the chef-repo
    def complement_path(path, is_check_dir=False):
        if path == '':
            return None
        if path.find('/') == 0:
            return path
        elif path.find('~') == 0:
            return os.path.expanduser(path)

        return os.path.join(CHEFREPO_DIR, path)

    INIFILE = os.path.join(CHEFREPO_DIR, 'fabfile.ini')

    CONFIG = ConfigParser.SafeConfigParser()
    CONFIG.read(INIFILE)

    # read common settings
    STORAGE_DIR = complement_path(CONFIG.get('common', 'storage_dir'))
    LOG_DIR = os.path.join(STORAGE_DIR, CONFIG.get('common', 'log_dir'))
    node_dir = CONFIG.get('common', 'node_dir')
    NODE_DIR = complement_path(node_dir)
    FABSCRIPT_MODULE = CONFIG.get('common', 'fabscript_module')
    FABSCRIPT_MODULE_DIR = os.path.join(CHEFREPO_DIR, FABSCRIPT_MODULE)
    FABLIB_MODULE = CONFIG.get('common', 'fablib_module')
    FABLIB_MODULE_DIR = os.path.join(CHEFREPO_DIR, FABLIB_MODULE)

    import maintenance
    maintenance.create_required_dirs()
    maintenance.git_clone_required_fablib()

    # logger settings
    ALL_LOG_FILE_NAME = 'all.log'
    ALL_LOG_FILE = os.path.join(LOG_DIR, ALL_LOG_FILE_NAME)
    ERROR_LOG_FILE_NAME = 'error.log'
    ERROR_LOG_FILE = os.path.join(LOG_DIR, ERROR_LOG_FILE_NAME)
    LOGGER_LEVEL = CONFIG.get('logger', 'level')
    LOGGER_LEVEL = getattr(logging, LOGGER_LEVEL.upper())
    LOGGER_FORMAT = CONFIG.get('logger', 'format', True)
    LOGGER_FORMATTER = logging.Formatter(fmt=LOGGER_FORMAT)
    LOGGER_CONSOLE_LEVEL = CONFIG.get('logger', 'console_level')
    LOGGER_CONSOLE_LEVEL = getattr(logging, LOGGER_CONSOLE_LEVEL.upper())
    LOGGER_CONSOLE_FORMAT = CONFIG.get('logger', 'console_format', True)
    LOGGER_CONSOLE_FORMATTER = logging.Formatter(fmt=LOGGER_CONSOLE_FORMAT)
    LOGGER_MAX_BYTES = CONFIG.getint('logger', 'max_bytes')
    LOGGER_BACKUP_COUNT = CONFIG.getint('logger', 'backup_count')
    NODE_LOGGER_MAX_BYTES = CONFIG.getint('node_logger', 'max_bytes')
    NODE_LOGGER_BACKUP_COUNT = CONFIG.getint('node_logger', 'backup_count')

    root_logger = logging.getLogger()
    root_logger.setLevel(LOGGER_LEVEL)

    stream_handler = StreamHandler()
    stream_handler.setFormatter(LOGGER_CONSOLE_FORMATTER)
    stream_handler.setLevel(LOGGER_CONSOLE_LEVEL)
    root_logger.addHandler(stream_handler)

    file_rotaiting_handler = RotatingFileHandler(ALL_LOG_FILE,
                                                 'a', LOGGER_MAX_BYTES, LOGGER_BACKUP_COUNT)
    file_rotaiting_handler.setFormatter(LOGGER_FORMATTER)
    root_logger.addHandler(file_rotaiting_handler)

    error_file_rotaiting_handler = RotatingFileHandler(ERROR_LOG_FILE,
                                                       'a', LOGGER_MAX_BYTES, LOGGER_BACKUP_COUNT)
    error_file_rotaiting_handler.setFormatter(LOGGER_FORMATTER)
    error_file_rotaiting_handler.setLevel(logging.ERROR)
    root_logger.addHandler(error_file_rotaiting_handler)


# chef-server setting
def is_chef(option=None):
    if option and option.find('s') != -1:
        env.is_chef = True
        return True
    else:
        return env.is_chef


def get_initial_json(host):
    return get_node_json({'name': host})


def get_node_json(dict_obj):
    return {
        'chef_environment': dict_obj.get('chef_environment', '_default'),
        'fab_run_list': dict_obj.get('fab_run_list', []),
        'data': dict_obj.get('data', {}),
    }


def get_node_log_json(dict_obj):
    return {
        'ipaddress': dict_obj.get('ipaddress', ''),
        'last_check': dict_obj.get('last_check', ''),
        'last_cook': dict_obj.get('last_cook', ''),
        'last_fabcooks': dict_obj.get('last_fabcooks', []),
        'last_runs': dict_obj.get('last_runs', []),
        'ssh': dict_obj.get('ssh', ''),
        'uptime': dict_obj.get('uptime', ''),
    }
