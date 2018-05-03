# coding: utf8
from __future__ import unicode_literals

import plac
import os
import subprocess
import sys
import ujson

from .link import link
from ._messages import Messages
from ..util import prints, get_package_path
from ..compat import url_read, HTTPError
from .. import about


@plac.annotations(
    model=("model to download, shortcut or name)", "positional", None, str),
    direct=("force direct download. Needs model name with version and won't "
            "perform compatibility check", "flag", "d", bool),
    unsecure=("unsecure mode - disables the verification of certificates", 
        "flag", "u", bool),
    caFile=("specify a certificate authority file to use for certificates "
        "validation. Ignored if --unsecure is used", "option", "c"))
def download(model, direct=False, unsecure=False, caFile=None):
    """
    Download compatible model from default download path using pip. Model
    can be shortcut, model name or, if --direct flag is set, full model name
    with version.
    The --unsecure optional flag can be used to disable ssl verification
    The --caFile option can be used to provide a local CA file
    used for certificate verification.
    """

    # sslVerify is the argument handled to the 'verify' parameter
    # of requests package. It must be either None, a boolean, 
    # or a String containing the path to CA file
    sslVerify = None
    if unsecure:
        caFile    = None
        sslVerify = False
    else:
        if caFile != None:
            sslVerify = caFile

    # Download the model
    if direct:
        dl = download_model('{m}/{m}.tar.gz'.format(m=model))
    else:
        shortcuts = get_json(about.__shortcuts__, "available shortcuts", sslVerify)
        model_name = shortcuts.get(model, model)
        compatibility = get_compatibility(sslVerify)
        version = get_version(model_name, compatibility)
        dl = download_model('{m}-{v}/{m}-{v}.tar.gz'.format(m=model_name,
                                                            v=version))
        if dl != 0:  # if download subprocess doesn't return 0, exit
            sys.exit(dl)
        try:
            # Get package path here because link uses
            # pip.get_installed_distributions() to check if model is a
            # package, which fails if model was just installed via
            # subprocess
            package_path = get_package_path(model_name)
            link(model_name, model, force=True,
                    model_path=package_path)
        except:
            # Dirty, but since spacy.download and the auto-linking is
            # mostly a convenience wrapper, it's best to show a success
            # message and loading instructions, even if linking fails.
            prints(Messages.M001.format(name=model_name), title=Messages.M002)


def get_json(url, desc, sslVerify):
    try:
        data = url_read(url, verify=sslVerify)
    except HTTPError as e:
        prints(Messages.M004.format(desc, about.__version__),
               title=Messages.M003.format(e.code, e.reason), exits=1)
    return ujson.loads(data)


def get_compatibility(sslVerify):
    version = about.__version__
    version = version.rsplit('.dev', 1)[0]
    comp_table = get_json(about.__compatibility__, "compatibility table", sslVerify)
    comp = comp_table['spacy']
    if version not in comp:
        prints(Messages.M006.format(version=version), title=Messages.M005,
               exits=1)
    return comp[version]


def get_version(model, comp):
    model = model.rsplit('.dev', 1)[0]
    if model not in comp:
        prints(Messages.M007.format(name=model, version=about.__version__),
               title=Messages.M005, exits=1)
    return comp[model][0]


def download_model(filename):
    download_url = about.__download_url__ + '/' + filename
    return subprocess.call(
        [sys.executable, '-m', 'pip', 'install', '--no-cache-dir', '--no-deps',
         download_url], env=os.environ.copy())
