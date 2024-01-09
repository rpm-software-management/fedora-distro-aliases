"""
Some projects such as Tito, Packit, Fedora Review Service, etc operate over
currently active Fedora releases. They either need to manualy define them in
a list or implement a code similar to this.
"""

from bodhi.client.bindings import BodhiClient
from munch import Munch


def bodhi_releases():
    """
    Return all releases from Bodhi
    https://bodhi.fedoraproject.org
    """
    bodhi_client = BodhiClient()
    releases = []
    page = pages = 1
    while page <= pages:
        results = bodhi_client.get_releases(exclude_archived=True, page=page)
        releases.extend(results.releases)
        page += 1
        pages = results.pages
    return releases


def bodhi_active_releases():
    """
    Return all active releases from Bodhi
    """
    states = ["current", "pending", "frozen"]
    return [x for x in bodhi_releases() if x.state in states]


def get_distro_aliases():
    """
    Define distribution aliases like `fedora-stable`, `fedora-branched`,
    `epel-all`, and more.
    """
    releases = bodhi_active_releases()
    epel = []

    distros = [Distro.from_bodhi_release(x) for x in releases if x.name != "ELN"]
    distros.sort(key=lambda x: int(x.version))

    epel = [x for x in distros if x.product == "epel"]
    fedora = [x for x in distros if x.product == "fedora"]

    # The Fedora with the highest version is "rawhide", but
    # Bodhi always uses release names, and has no concept of "rawhide".
    fedora[-1].update({
        "name": "Rawhide",
        "long_name": "Fedora Rawhide",
        "version": "rawhide",
    })

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
        return cls({k: getattr(release, k) for k in keys})

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
