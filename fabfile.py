#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Deployment script.

This script is coded so it can make the deployments automagically in the
designed servers.
Also it documents the deployment process

USE: fab <hosts>:<username> <action>
EX: fab staging:admin release
"""

import os
import datetime
from string import Template
from contextlib import contextmanager

from fabric.api import env, run, local, require, put, prefix, sudo
from fabric.contrib.files import exists

BASE_DIR = os.path.dirname(__file__)

env.project_name = 'visiui'

env.tar = '%s-%s.tar.gz' % (
    env.project_name,
    datetime.datetime.now().strftime('%Y%m%d%H%M%S'),
)
env.bundle = '%s-static.tar.gz' % (
    env.project_name,
)

bundle_path = os.path.join(os.path.dirname(__file__), env.bundle)

env.use_ssh_config = True


@contextmanager
def virtualenv():
    with prefix('. %(venv_dir)s/bin/activate' % env):
        yield


def production(username='fudepan', hosts=['zapaton']):
    """Production environment."""
    env.hosts = hosts
    env.user = username
    base_dir = '/home/%s' % username
    env.deploy_dir = os.path.join(base_dir, 'sites/visiui')
    env.static_dir = os.path.join(base_dir, 'sites/visiui_static')
    env.venv_dir = os.path.join(base_dir, 'venvs/visiui')


def setup_env():
    """
    Creates required directories for deployment.
    It also attempts to install pip requirements on remote host.
    While not intended you might run it for local setup.
    """
    require('venv_dir')

    dirs = (env[x] for x in env if x.endswith('_dir'))

    for directory in dirs:
        if not exists(directory):
            run('mkdir -p %s' % directory)

    if not exists('%s/bin/activate' % env.venv_dir):
        run('virtualenv -q -ppython3 %s' % env.venv_dir)

    put('requirements.txt', 'requirements.txt')

    with virtualenv():
        run('pip -q install -Ur requirements.txt')


def upload_service(rev='default'):
    """
    Create a tarball honoring git's ignored and non-tracked files,
    uploads it and decompresses it in the rigth path.
    """
    require('host')
    require('deploy_dir')
    require('tar')
    local('git archive %s -o %s' % (rev, env.tar))
    put(env.tar, env.tar)
    run("tar xfz %s -C %s" % (env.tar, env.deploy_dir))


def write_template(file_name, template_name):
    '''
    Safe substitute env object variables into a file.
    Uses python's built in string format.

    https://docs.python.org/3/library/string.html#formatstrings
    '''
    template = Template(open(template_name).read())
    rendered_file = open(file_name, 'w')
    rendered_file.write(template.safe_substitute(env))
    rendered_file.close()

    return rendered_file


def sync_and_migrate():
    """Runs sycndb and migrate commands"""
    require("virtual_env")
    with prefix("source %s/bin/activate" % env.virtual_env):
        run("manage migrate")


def build_static_bundle():
    """
    Create a tarball of the static files
    to be uploaded later.
    It invokes django's collectstatic method and
    runs a regular grunt build.
    Requires your local development environment to be activated and the
    `presentes` management command to be available.
    """
    require('bundle')

    local('manage collectstatic --noinput')
    local('npm run build')
    local('tar cf %s -C ./static/ .' % env.bundle)


def upload_static(force=False):
    """
    Uploads `env.bundle` and decompresses it in the right path
    This will attempt to create and delete local gzips.
    Cleanup is not always what it should...
    """
    require('bundle')
    require('static_dir')
    require('bundle_path')
    if force or not os.path.exists(bundle_path):
        build_static_bundle()

    put(env.bundle_path, env.bundle)
    run('tar xf %s -C %s' % (env.bundle, env.static_dir))


def cleanup():
    run("rm %s" % env.tar)
    local("rm %s" % env.tar)
    run('rm %s' % env.bundle)
    local('rm %s' % env.bundle_path)


def restart_service():
    require('host')

    sudo('systemctl restart uwsgi')
    sudo('systemctl restart nginx')


def release(rev='HEAD', force=False):
    """
    End-to-end release.
    It's a wrapper for the other functions.
    """
    require('host')
    require('bundle')
    require('static_dir')
    require('venv_dir')
    require('tar')

    setup_env()
    upload_service(rev=rev)
    upload_static(force=force)
