from munch import Munch
from fedora_distro_aliases import Distro


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
    assert "nonsense" not in distro
    assert "additional" not in distro
