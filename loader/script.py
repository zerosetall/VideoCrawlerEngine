

import importlib
from pathlib import Path
import sys
from .base import BaseLoader, BasePlugin
from .python import PythonLoader


class ScriptLoader(BaseLoader):
    def __call__(self, path: str):
        ldr = PythonLoader()
        return ldr(path)


class ScriptPlugin(BasePlugin):
    def __init__(
        self,
        name: str,
        path: str,

    ):
        self.name = name

    def __call__(self):
        pass





if __name__ == '__main__':
    loader = ScriptLoader()
    res = loader('d:/zerosetall/VideoCrawlerEngine/repo/bilibili.py')
    print(res)
