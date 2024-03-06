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


## Similar projects

- [fedfind](https://pagure.io/fedora-qa/fedfind) - Python module and CLI for
  finding and inspecting Fedora composes and deliverables
