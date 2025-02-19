"""
Some projects such as Tito, Packit, Fedora Review Service, etc operate over
currently active Fedora releases. They either need to manualy define them in
a list or implement a code similar to this.
"""

import requests
from typing import Optional
from munch import Munch
from fedora_distro_aliases.cache import Cache, SaveLoad


def bodhi_active_releases():
    """
    Return all active releases from Bodhi
    https://bodhi.fedoraproject.org
    """
    bodhi_url = "https://bodhi.fedoraproject.org/releases/"
    releases = []
    states = ["current", "pending", "frozen"]

    # Bodhi's API returns results in pages of 20, so we must check if there are
    # additional pages to make sure we don't miss any releases.
    page = 1
    while True:
        response = requests.get(
            bodhi_url,
            params={"state": states, "page": page}
        )
        response.raise_for_status()
        response_json = response.json()
        releases.extend(response_json["releases"])
        if page == response_json["pages"]:
            break
        page += 1
    return releases


def get_distro_aliases(cache: Optional[SaveLoad] = None):
    """
    Define distribution aliases like `fedora-stable`, `fedora-branched`,
    `epel-all`, and more.
    """
    if cache is True:
        cache = Cache()
    try:
        releases = bodhi_active_releases()
        if cache:
            cache.save(releases)
    except requests.exceptions.RequestException as ex:
        if not cache:
            raise ex
        releases = cache.load()

    distros = [Distro.from_bodhi_release(x) for x in releases if x["name"] != "ELN"]
    distros.sort(key=lambda x: float(x.version_number))

    epel = [x for x in distros if x.product == "epel"]
    fedora = [x for x in distros if x.product == "fedora"]

    # The Fedora with the highest version is "rawhide", but
    # Bodhi always uses release names, and has no concept of "rawhide".
    fedora[-1].update({
        "name": "Rawhide",
        "long_name": "Fedora Rawhide",
        "version": "rawhide",
        "branch": "rawhide",
    })

    # During the window from branching to the final release, things can get
    # weird. Bodhi can be lying to us. For example, F40 was branched yesterday,
    # therefore Rawhide is F41 now. However bodhi says that Fedora 40 branch is
    # `rawhide` and F41 branch is `f41`.
    if fedora[-2].branch == "rawhide":
        fedora[-2].branch = "f{0}".format(fedora[-2].version)

    fedora_stable = [x for x in fedora if x.state == "current"]
    fedora_devel = [x for x in fedora if x.state in ("pending", "frozen")]

    return {
        "fedora-all": fedora,
        "fedora-stable": fedora_stable,
        "fedora-development": fedora_devel,
        "fedora-latest": fedora_devel[-2:-1] or fedora_stable[-1:],
        "fedora-latest-stable": fedora_stable[-1:],
        "fedora-branched": fedora_stable + fedora_devel[:-1],
        "epel-all": epel,
    }


class Distro(Munch):
    """
    Represent a single distribution
    """

    @classmethod
    def from_bodhi_release(cls, release):
        """
        Create a `Distro` object from Bodhi `release`
        """
        keys = ["name", "long_name", "version", "state", "branch", "id_prefix"]
        distro = cls({k: release.get(k) for k in keys})
        distro.version_number = release["version"]
        return distro

    @property
    def product(self):
        """
        It is cumbersome to work with `id_prefix` from the outside
        """
        if self.id_prefix == "FEDORA":
            return "fedora"
        if self.id_prefix == "FEDORA-EPEL":
            return "epel"
        return None

    @property
    def namever(self):
        """
        Name and version of this distro, e.g. fedora-rawhide or epel-9
        """
        if self.id_prefix == "FEDORA-EPEL":
            return self.name.lower()
        return self.long_name.lower().replace(" ", "-")
