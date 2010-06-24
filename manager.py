#!/usr/bin/env python

import sys
import os


class Plugin(object):
    pass


class PluginManager():
    def __init__(self, path=None, plugin_init_args={}):
        if path:
            self.plugin_dir = path
        else:
            self.plugin_dir = os.path.dirname(__file__) + '/plugins/'
        self.plugins = {}
        self._load_plugins()
        self._register_plugins(**plugin_init_args)

    def _load_plugins(self):
        sys.path.append(self.plugin_dir)
        plugin_files = [fn for fn in os.listdir(self.plugin_dir) if fn.startswith('plugin_') and fn.endswith('.py')]
        plugin_modules = [m.split('.')[0] for m in plugin_files]
        for module in plugin_modules:
            m = __import__(module)

    def _register_plugins(self, **kwargs):
        for plugin in Plugin.__subclasses__():
            obj = plugin(**kwargs)
            self.plugins[obj] = obj.keywords if hasattr(obj, 'keywords') else []

    def call_method(self, method, args={}, keywords=[]):
        for plugin in self.plugins:
            if not keywords or (set(keywords) & set(self.plugins[plugin])):
                try:
                    getattr(plugin, method)(**args)
                except:
                    pass

