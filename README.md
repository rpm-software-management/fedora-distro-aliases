# Fedora Distro Aliases

Some projects such as Tito, Packit, Fedora Review Service, etc operate over
currently active Fedora releases. They can use this package to find their
version numbers instead of manually defining a list.

This package queries Bodhi to find the active releases and therefore requires an
internet connection.

[![REUSE status](https://api.reuse.software/badge/github.com/rpm-software-management/fedora-distro-aliases)](https://api.reuse.software/info/github.com/rpm-software-management/fedora-distro-aliases)

## Supported aliases

| Alias name             | Description                                         |
|------------------------|-----------------------------------------------------|
| `fedora-all`           | All active Fedora releases                          |
| `fedora-stable`        | All stable Fedora releases                          |
| `fedora-development`   | Not yet branched Fedora releases                    |
| `fedora-latest`        | Latest Fedora release excluding Rawhide (as a list of one item) |
| `fedora-latest-stable` | Latest stable Fedora (as a list of one item)        |
| `fedora-branched`      | All branched Fedora releases                        |
| `epel-all`             | All active EPEL releases                            |


## Installation

The package is available in the Fedora repositories:

```
dnf install python3-fedora-distro-aliases
```

Alternatively, you can install it from PyPI

```
pip3 install fedora-distro-aliases
```


## Usage

```python
>>> from fedora_distro_aliases import get_distro_aliases
>>> aliases = get_distro_aliases()
```

Distribution names and their versions.

```python
>>> [x.namever for x in aliases["fedora-all"]]
['fedora-38', 'fedora-39', 'fedora-rawhide']
```

Append architectures and you have Mock chroot names

```python
>>> [f"{x.namever}-x86_64" for x in aliases["fedora-all"]]
['fedora-38-x86_64', 'fedora-39-x86_64', 'fedora-rawhide-x86_64']
```

Branch names in DistGit:

```python
>>> [x.branch for x in aliases["fedora-all"]]
['f38', 'f39', 'rawhide']
```

Only version numbers:

```python
>>> [x.version for x in aliases["fedora-all"]]
['38', '39', 'rawhide']
```

If you need a numeric version even for rawhide:

```python
>>> [x.version_number for x in aliases["fedora-all"]]
['38', '39', '40']
```


## Caching

To avoid a single point of failure on Bodhi API, we can cache successfully
fetched data, and use them when there is an issue.

```python
>>> aliases = get_distro_aliases(cache=True)
>>> [x.namever for x in aliases["fedora-all"]]
['fedora-39', 'fedora-40', 'fedora-rawhide']
```

To configure parameters for the cache pass an object instead of `True`.

```
>>> from fedora_distro_aliases import Cache
>>> cache = Cache(path="/tmp/fedora-distro-aliases-cache.json", ttl=3600)
>>> aliases = get_distro_aliases(cache=cache)
>>> [x.namever for x in aliases["fedora-all"]]
['fedora-39', 'fedora-40', 'fedora-rawhide']
```

To implement a custom caching mechanism, pass object of any class that
implements the `fedora_distro_aliases.cache.SaveLoad` protocol.


## Similar projects

- [opensuse-distro-aliases](https://github.com/rpm-software-management/opensuse-distro-aliases) -
  Aliases for active openSUSE releases
- [fedfind](https://pagure.io/fedora-qa/fedfind) - Python module and CLI for
  finding and inspecting Fedora composes and deliverables
