
from typing import Dict


class BasePlugin:
    pass


class BaseLoader:
    LOADER_CACHE: Dict[str, BasePlugin] = {}

    def __init__(self, no_cache=False):
        self.no_cache = no_cache

    def load(self, path: str, **kwargs):
        if self.no_cache:
            plugin = self.LOADER_CACHE.get(path, None)
            if plugin is not None:
                return plugin
            plugin = self.__call__(path, **kwargs)
            self.LOADER_CACHE[path] = plugin
        else:
            plugin = self.__call__(path, **kwargs)

        return plugin

    def __call__(self, path, **kwargs):
        raise NotImplementedError


class BaseConf:
    pass

