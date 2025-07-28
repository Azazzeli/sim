# mods/__init__.py
import importlib
import pkgutil
import os
import sys

sys.path.append(os.path.dirname(__file__))


def load_mods(game_instance):
    mods = []

    # ⚠️ Сначала загружаем mod_intro
    try:
        module = importlib.import_module("mods.mod_intro")
        if hasattr(module, "init"):
            module.init(game_instance)
        mods.append(module)
        print("✅ Модуль загружен: mod_intro")
    except Exception as e:
        print(f"❌ Ошибка в mod_intro: {e}")

    # Затем остальные
    for _, module_name, _ in pkgutil.iter_modules([os.path.dirname(__file__)]):
        if module_name.startswith("mod_") or module_name.startswith("event_"):
            if module_name == "mod_intro":
                continue
            try:
                module = importlib.import_module(f"mods.{module_name}")
                if hasattr(module, "init"):
                    module.init(game_instance)
                mods.append(module)
                print(f"✅ Модуль загружен: {module_name}")
            except Exception as e:
                print(f"❌ Ошибка в модуле {module_name}: {e}")
    return mods