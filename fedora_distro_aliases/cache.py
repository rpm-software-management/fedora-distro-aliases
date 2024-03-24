"""
To avoid a single point of failure on Bodhi API, we can cache successfully
fetched data, and use them when there is an issue.
"""

import os
import time
import json
from datetime import datetime, timedelta
from typing import Protocol


class SaveLoad(Protocol):
    def save(self, data) -> None:
        ...

    def load(self) -> dict:
        ...


class Cache:
    """
    Save and load cache from a JSON file
    """

    DEFAULT_PATH = "~/.cache/fedora-distro-aliases/cache.json"

    def __init__(self, path=None, ttl=None):
        """
        Create a new cache.

        Args:
          path: Path to the file containing the cached data.
          ttl: (int) TTL of the cache in seconds.
        """
        self.path = os.path.expanduser(path or self.DEFAULT_PATH)
        self.ttl = ttl

    def save(self, data):
        """
        Save important data from a successfull request to cache, so it can be
        recovered later.
        """
        body = {
            "data": data,
            "timestamp": time.time(),
        }
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w+") as fp:
            json.dump(body, fp)

    def load(self):
        """
        Load data from cache. If cache doesn't exist, or the data is too old,
        raise a `BadCache` exception.
        """
        try:
            with open(self.path, "r") as fp:
                cache = json.load(fp)
            created = datetime.fromtimestamp(cache["timestamp"])
        except OSError as ex:
            raise BadCache(str(ex)) from ex

        if self.ttl and created + timedelta(seconds=self.ttl) < datetime.now():
            msg = "The cache is older than {0} seconds".format(self.ttl)
            raise BadCache(msg)
        return cache["data"]


class BadCache(Exception):
    """
    When the cache file doesn't exist or the cache is older than acceptable
    """
