# coding: utf-8
from __future__ import unicode_literals

from ..cli.download import download, get_compatibility, get_version, check_error_depr
from ..cli.link import is_package

import pytest


@pytest.mark.parametrize('model', ['en_core_web_md'])
def test_cli_download_get_matching_version_succeeds(model):
    comp = { model: ['1.7.0', '0.100.0'] }
    assert get_version(model, comp)


@pytest.mark.parametrize('model', ['en_core_web_md'])
def test_cli_download_get_matching_version_fails(model):
    diff_model = 'test_' + model
    comp = { diff_model: ['1.7.0', '0.100.0'] }
    with pytest.raises(SystemExit):
        assert get_version(model, comp)


@pytest.mark.parametrize('model', [False, None, '', 'all'])
def test_cli_download_no_model_depr_error(model):
    with pytest.raises(SystemExit):
        check_error_depr(model)


@pytest.mark.parametrize('package', ['numpy'])
def test_cli_link_is_package(package):
    """Test that an installed package via pip is recognised by link.is_package."""
    assert is_package(package)
