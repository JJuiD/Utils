# 插件管理器
import traceback
from typing import Final

from flask import Flask
from define import singleton
from module.base import ModuleBase
from module.rss import RSSModule

class _ModuleManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(_ModuleManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self._last: ModuleBase | None = None
        self._modules: dict[str, ModuleBase] = {}

    def register(self, module: ModuleBase):
        print(f"Registered module: {module}")
        self._modules[module.name] = module
        module.init()

    def open(self, name: str):
        if self._last != None:
            self._last.close()
        module = self._modules[name]
        self._last = module
        result = module.open()
        if module.is_first:
            module.is_first = False
        return result

    def get_module(self, name: str):
        return self._modules[name]

    def execute_modules_by_type(self, name: str):
        print(f"Executing modules of type {name}:")

    def on_app_quit(self):
        for module in self._modules.values():
            module.on_app_quit()
        # TODO: 退出重复调用
        self._modules.clear()

ModuleManager = _ModuleManager()
ModuleManager.register(RSSModule('rss'))




