

import importlib
from pathlib import Path
from types import ModuleType
from typing import AnyStr
import sys
from .base import BaseLoader, BasePlugin


class PythonLoader(BaseLoader):
    IMPORT_DIRS = set()

    def __call__(self, path: str, global_scope: dict = None):
        p = Path(path)
        plugin_dir = str(p.parent)
        if not p.is_file():
            raise FileNotFoundError(f'不存在的文件 {p}')
        elif p.suffix not in ['.py']:
            raise FileNotFoundError(f'加载器不支持解析 {p.suffix}的文件')

        if plugin_dir not in self.IMPORT_DIRS:
            # sys.path.append(plugin_dir)
            self.IMPORT_DIRS.add(plugin_dir)

        with open(str(p), 'rb') as pyfile:
            source = pyfile.read()

        # 注入全局作用域探测代码，用于更新全局环境
        source += b'\ndef __global_scope_probe__(): pass'
        code = compile(source, '<string>', 'exec')

        if global_scope is None:
            global_scope = {}

        resp_scope = {}
        exec(code, global_scope, resp_scope)

        # 探测出全局环境
        probe_func = resp_scope.get('__global_scope_probe__', None)

        # DOC: https://docs.python.org/zh-cn/3.7/library/stdtypes.html#code-objects
        # 代码对象被具体实现用来表示“伪编译”的可执行 Python 代码，例如一个函数体。
        # 它们不同于函数对象，因为它们不包含对其全局执行环境的引用。
        probe_func.__globals__.update(resp_scope)
        return PythonPlugin(
            name=p.stem,
            path=str(p),
            global_scope=probe_func.__globals__,
            local_scope=resp_scope,
        )


class PythonPlugin(BasePlugin):
    def __init__(
        self,
        name: str,
        path: str,
        global_scope: dict,
        local_scope: dict,
    ):
        self.name = name
        self.path = path
        self.global_scope = global_scope
        self.local_scope = local_scope

    def get_scopes(self):
        yield from self.local_scope.items()

    def get_scope(self, name: str, default=None):
        return self.local_scope.get(name, default)
