# coding: utf8
from __future__ import unicode_literals

import requests
import os
import subprocess
import sys

from .link import link_package
from .. import about
from .. import util


def download(model=None, direct=False):
    check_error_depr(model)

    if direct:
        download_model('{m}/{m}.tar.gz'.format(m=model))
    else:
        model_name = check_shortcut(model)
        compatibility = get_compatibility()
        version = get_version(model_name, compatibility)
        download_model('{m}-{v}/{m}-{v}.tar.gz'.format(m=model_name, v=version))
        link_package(model_name, model, force=True)


def get_json(url, desc):
    r = requests.get(url)
    if r.status_code != 200:
        util.sys_exit(
            "Couldn't fetch {d}. Please find the right model for your spaCy "
            "installation (v{v}), and download it manually:".format(d=desc, v=about.__version__),
            "python -m spacy.download [full model name + version] --direct",
            title="Server error ({c})".format(c=r.status_code))
    return r.json()


def check_shortcut(model):
    shortcuts = get_json(about.__shortcuts__, "available shortcuts")
    return shortcuts.get(model, model)


def get_compatibility():
    version = about.__version__
    comp_table = get_json(about.__compatibility__, "compatibility table")
    comp = comp_table['spacy']
    if version not in comp:
        util.sys_exit(
            "No compatible models found for v{v} of spaCy.".format(v=version),
            title="Compatibility error")
    return comp[version]


def get_version(model, comp):
    if model not in comp:
        util.sys_exit(
            "No compatible model found for "
            "'{m}' (spaCy v{v}).".format(m=model, v=about.__version__),
            title="Compatibility error")
    return comp[model][0]


def download_model(filename):
    util.print_msg("Downloading {f}".format(f=filename))
    download_url = about.__download_url__ + '/' + filename
    subprocess.call([sys.executable, '-m',
        'pip', 'install', '--no-cache-dir', download_url],
        env=os.environ.copy())


def check_error_depr(model):
    if not model:
        util.sys_exit(
            "python -m spacy.download [name or shortcut]",
            title="Missing model name or shortcut")

    if model == 'all':
        util.sys_exit(
            "As of v1.7.0, the download all command is deprecated. Please "
            "download the models individually via spacy.download [model name] "
            "or pip install. For more info on this, see the documentation: "
            "{d}".format(d=about.__docs_models__),
            title="Deprecated command")
