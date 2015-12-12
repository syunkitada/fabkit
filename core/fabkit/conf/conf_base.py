# coding: utf-8

import os
from oslo_config import cfg
from oslo_log import log

from constant import (  # noqa
    INIFILE_NAME,
    STDOUT_LOG_FILE_NAME,
    ALL_LOG_FILE_NAME,
    ERROR_LOG_FILE_NAME,
    DOC_DIR_NAME,
    YAML_EXTENSION,
    CLUSTER_YAML,
    CLUSTER_PICKLE,
    FABSCRIPT_YAML,
    DATAMAP_DIR,
)


CONF = cfg.CONF

default_opts = [
    cfg.StrOpt('storage_dir',
               default='storage',
               help='storage_dir is storing files(e.g. logs, packages of chef).'
                    '[absolute path or relative path from chef-repo]'),
    cfg.StrOpt('databag_dir',
               default='databag',
               help='databag dir'),
    cfg.StrOpt('tmp_dir',
               default='tmp',
               help='tmp dir'),
    cfg.StrOpt('node_dir',
               default='node',
               help='node dir'),
    cfg.StrOpt('fabscript_module',
               default='fabscript',
               help='fabscript_module is module including user\'s scripts of fabric.'
                    'This module must be placed in the repository.'),
    cfg.StrOpt('fablib_module',
               default='fablib',
               help='fablib_module is module including library of user or vendor for fabscript.'
                    'This module must be placed in the repository.')

]


CONF.register_opts(default_opts)


def complement_path(path):
    if path == '':
        return None
    if path.find('/') == 0:
        return path
    elif path.find('~') == 0:
        return os.path.expanduser(path)

    return os.path.join(CONF._repo_dir, path)


def init(fabfile_dir=None, repo_dir=None):
    INIFILE = os.path.join(repo_dir, INIFILE_NAME)
    log.register_options(CONF)
    CONF([], default_config_files=[INIFILE])
    CONF._fabfile_dir = fabfile_dir
    CONF._repo_dir = repo_dir
    CONF._storage_dir = complement_path(CONF.storage_dir)
    CONF._databag_dir = complement_path(CONF.databag_dir)
    CONF._tmp_dir = os.path.join(CONF._storage_dir, CONF.tmp_dir)
    CONF._node_dir = complement_path(CONF.node_dir)
    CONF._fabscript_module_dir = complement_path(CONF.fabscript_module)
    CONF._fablib_module_dir = complement_path(CONF.fablib_module)

    log.setup(CONF, 'fabkit')