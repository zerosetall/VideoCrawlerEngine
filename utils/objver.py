
from collections import defaultdict
from typing import Any


class VersionExistedError(Exception):
    def __init__(self, name, version):
        self.name = name
        self.version = version

    def __repr__(self):
        return f'<VersionExistedError name={self.name}, version={self.version}>'


class ObjectVersions:
    def __init__(self):
        self._name_version_obj = defaultdict(dict)

    def add(self, name, version, obj: Any):
        version_obj = self._name_version_obj.get(name, None)
        if version_obj is not None:
            raise VersionExistedError(name, version)
        self._name_version_obj[name][version] = obj

    def get_versions(self, name):
        return list(self._name_version_obj[name].keys())

    def iter_obj(self, name):
        return iter(self._name_version_obj[name].items())

    def remove_version(self, name, version):
        versions = self._name_version_obj[name]
        del versions[version]

    def get(self, name, version):
        return self._name_version_obj[name][version]

    def __contains__(self, item):
        if not isinstance(item, (list, tuple)):
            return item in self._name_version_obj
        elif len(item) != 2:
            raise ValueError(f'传入的数组长度应=2，(name, version) in obj')
        else:
            name, version = item
            return version in self._name_version_obj.get(name, {})