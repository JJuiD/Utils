# 插件管理器
from typing import Final
from define import PluginType
from help.singleton import Singleton
from plugin.base import Plugin
from plugin.rss import RSSPlugin


__all__ = ["PluginManager", "Plugin", "PluginType"]

class _PluginManager(Singleton):
    def __init__(self):
        self._last: Plugin | None = None
        self._plugins: dict[str, Plugin] = {}

    def register(self, plugin: Plugin):
        print(f"Registered plugin: {plugin}")
        self._plugins[plugin.name] = plugin
        plugin.init()

    def open(self, name: str):
        if self._last != None:
            self._last.close()
        plugin = self._plugins[name]
        self._last = plugin
        return plugin.open()
    
    def get_plugin(self, name: str):
        return self._plugins[name]
    
    def execute_plugins_by_type(self, name: str):
        print(f"Executing plugins of type {name}:")

    def on_app_quit(self):
        for plugin in self._plugins.values():
            plugin.on_app_quit()

PluginManager: Final = _PluginManager()
PluginManager.register(RSSPlugin('rss'))