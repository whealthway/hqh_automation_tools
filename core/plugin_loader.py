import os
import importlib


def load_plugins():
    plugins = []

    for file in os.listdir("plugins"):
        if file.endswith(".py"):
            module_name = f"plugins.{file[:-3]}"
            module = importlib.import_module(module_name)

            if hasattr(module, "register"):
                plugins.append(module.register())

    return plugins
