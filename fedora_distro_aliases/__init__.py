"""
Some projects such as Tito, Packit, Fedora Review Service, etc operate over
currently active Fedora releases. They either need to manualy define them in
a list or implement a code similar to this.
"""

import requests
from munch import Munch


def bodhi_active_releases():
    """
    Return all active releases from Bodhi
    https://bodhi.fedoraproject.org
    """
    bodhi_url =  "https://bodhi.fedoraproject.org/releases/"
    releases = []
    states = ["current", "pending", "frozen"]
    for state in states:
        url = "{0}?state={1}".format(bodhi_url, state)
        response = requests.get(url)
        response.raise_for_status()
        releases.extend(response.json()["releases"])
    return [Munch(x) for x in releases]


def get_distro_aliases():
    """
    Define distribution aliases like `fedora-stable`, `fedora-branched`,
    `epel-all`, and more.
    """
    releases = bodhi_active_releases()
    epel = []

    distros = [Distro.from_bodhi_release(x) for x in releases if x.name != "ELN"]
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
    fedora_devel = [x for x in fedora if x.state == "pending"]

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
        distro = cls({k: getattr(release, k) for k in keys})
        distro.version_number = release.version
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
