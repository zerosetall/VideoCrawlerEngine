

from .base import BaseLoader, BasePlugin
from .python import PythonLoader
from typing import Any, Callable, Union, List, Dict
from pydantic import ValidationError
from validator.model import ValidatorModel
from utils.objver import ObjectVersions, VersionExistedError


class CrawlerImplModel(ValidatorModel):
    NAME: str
    VERSION: str
    AUTHOR: str
    CREATE_AT: str
    SUPPORTS: Union[tuple, list]
    RANKING: Union[tuple, list]

    DEPENDENCIES: Union[tuple, list]

    run: Callable[[], None]

    close: Callable[[], None]


class CrawlerLoader(BaseLoader):
    PLUGINS = {}

    def __call__(self, path: str, **kwargs):
        ldr = PythonLoader()
        pyplg = ldr.load(path)

        scope = pyplg.get_scope('__all__')
        if type(scope) is not dict:
            scope = pyplg.get_scopes()
        models = {}
        for k, v in scope:
            try:
                crawler: CrawlerImplModel = CrawlerImplModel.validate(v)
            except ValidationError:
                continue
            else:
                # 加载依赖
                for dependency in crawler.DEPENDENCIES:
                    # TODO: dependency => path
                    path = ''
                    # self.load(path)

                name_version = f'{crawler.NAME}:{crawler.VERSION}'
                if name_version in models:
                    raise VersionExistedError(crawler.NAME, crawler.VERSION)
                models[name_version] = crawler
        if not models:
            raise NotImplementedError()
        return CrawlerPlugin(path, pyplg.name, scope, models)


class CrawlerPlugin(BasePlugin):
    MODELS = ObjectVersions()

    def __init__(
        self,
        path: str,
        name: str,
        scope: dict,
        models: Dict[str, CrawlerImplModel],
    ):
        self.name = name
        self.path = path
        self.scope = scope
        self.models = models

    def __call__(self):
        pass

    def __new__(cls, path, name, scope, models):
        for _, model in models.items():
            if (model.NAME, model.VERSION) in cls.MODELS:
                raise VersionExistedError(model.NAME, model.VERSION)
            cls.MODELS.add(model.NAME, model.VERSION, model)

        ins = super().__new__(cls)
        return ins


if __name__ == '__main__':
    loader = CrawlerLoader()
    res = loader('d:/zerosetall/VideoCrawlerEngine/repo/bilibili.py')
    print(res)
