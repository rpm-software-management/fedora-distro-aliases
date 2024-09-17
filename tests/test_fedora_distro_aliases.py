import os
import json
from unittest.mock import patch, MagicMock
from munch import Munch
from fedora_distro_aliases import (
    Distro,
    bodhi_active_releases,
    get_distro_aliases,
)

here = os.path.abspath(os.path.dirname(__file__))
datadir = os.path.join(here, "data")


def mock_responses(files):
    """
    We can use this function to comfortably mock responses from saved files.
    """
    responses = []
    for name in files:
        path = os.path.join(datadir, name)
        with open(path, "r") as fp:
            data = json.load(fp)
        response = MagicMock()
        response.json.return_value = data
        responses.append(response)
    return responses


def test_distro():
    release = Munch({
        "name": "Foo",
        "long_name": "Foo 123",
        "version": "123",
        "state": "current",
        "branch": "foo",
        "id_prefix": "FEDORA",
        "nonsense": True,
        "additional": "value",
    })
    distro = Distro.from_bodhi_release(release)
    assert distro.name == "Foo"
    assert distro.namever == "foo-123"
    assert distro.product == "fedora"
    assert distro.product == "fedora"
    assert distro.version_number == "123"
    assert "nonsense" not in distro
    assert "additional" not in distro


@patch("requests.get")
def test_f40_branch_to_final_release_window(requests_get):
    """
    Test that everything behaves as expected during the window from branching
    to the final release.
    """
    requests_get.side_effect = mock_responses([
        "bodhi-f40-branch-window.json",
    ])
    aliases = get_distro_aliases()
    branches = [x.branch for x in aliases["fedora-all"]]
    assert branches == ["f38", "f39", "f40", "rawhide"]

    namevers = [x.namever for x in aliases["fedora-all"]]
    expected = ["fedora-38", "fedora-39", "fedora-40", "fedora-rawhide"]
    assert namevers == expected

    versions = [x.version for x in aliases["fedora-all"]]
    assert versions == ["38", "39", "40", "rawhide"]

    version_numbers = [x.version_number for x in aliases["fedora-all"]]
    assert version_numbers == ["38", "39", "40", "41"]


@patch("requests.get")
def test_pagination(requests_get):
    """
    Test that pagination works as expected.
    """
    requests_get.side_effect = mock_responses([
        "bodhi-page-1.json",
        "bodhi-page-2.json",
    ])
    releases = bodhi_active_releases()
    names = [r.name for r in releases]
    assert names == [
        "ELN",
        "EPEL-10.0",
        "EPEL-8",
        "EPEL-9",
        "EPEL-9N",
        "F39",
        "F39C",
        "F39F",
        "F40",
        "F40C",
        "F40F",
        "F41",
        "F41C",
        "F41F",
        "F42",
        "F42C",
        "F42F",
    ]
