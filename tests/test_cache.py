import json
import requests
from tempfile import NamedTemporaryFile
from unittest import TestCase
from unittest.mock import patch
from fedora_distro_aliases import get_distro_aliases
from fedora_distro_aliases.cache import Cache, BadCache
from . import mock_responses


class TestCache(TestCase):

    def setUp(self):
        self.tmp = NamedTemporaryFile(prefix="fedora-distro-aliases-test-")

    def test_cache_isolated(self):
        """
        Make sure caching work on its own
        """
        data = {"foo": {"bar": "baz"}}

        # Test that caching doesn't modify the data
        cache = Cache(path=self.tmp.name)
        cache.save(data)
        assert cache.load() == data

        # Test we can load data if TTL is specified
        cache = Cache(path=self.tmp.name, ttl=60)
        assert cache.load() == data

        # If the cache is expired, we will raise an exception
        cache = Cache(path=self.tmp.name, ttl=-60)
        with self.assertRaises(BadCache):
            cache.load()

    @patch("requests.get")
    def test_cached_distro_aliases(self, requests_get):
        """
        Test `get_distro_aliases` support for caching
        """
        success = mock_responses([
            "bodhi-f40-branch-window.json",
        ])

        # Aliases without caching so that we have a point of reference
        requests_get.side_effect = success
        aliases = get_distro_aliases()


        # Network is fine so this should only save cache but don't use it
        requests_get.side_effect = success
        cache = Cache(path=self.tmp.name)
        assert get_distro_aliases(cache=cache) == aliases

        data = json.load(self.tmp)
        assert "data" in data
        assert "timestamp" in data


        # Network doesn't work but we have cache
        exception = requests.exceptions.RequestException
        requests_get.side_effect = exception
        with self.assertRaises(exception):
            # Without cache, we are toast
            get_distro_aliases()

        cached = get_distro_aliases(cache=cache)
        assert cached == aliases
        assert [x.namever for x in cached["fedora-all"]] ==\
            ['fedora-38', 'fedora-39', 'fedora-40', 'fedora-rawhide']


        # Network doesn't work but we don't have cache or it is unusable
        requests_get.side_effect = requests.exceptions.RequestException
        cache = Cache(path="nonexisting-nonsense-path.json")
        with self.assertRaises(BadCache):
            get_distro_aliases(cache=cache)
