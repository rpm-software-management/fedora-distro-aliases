# Fedora Distro Aliases

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
