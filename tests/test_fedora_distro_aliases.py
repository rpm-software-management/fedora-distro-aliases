from unittest.mock import patch
from munch import Munch
from fedora_distro_aliases import Distro, get_distro_aliases
from . import mock_responses


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
        "bodhi-f40-branch-window-current.json",
        "bodhi-f40-branch-window-pending.json",
        "bodhi-f40-branch-window-frozen.json",
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
