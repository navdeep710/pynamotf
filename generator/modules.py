import glob
import importlib
import os
import pkgutil
import traceback
from importlib import import_module

import fire
from pynamodb.models import Model
from pathlib import Path
import sys, inspect
import pyclbr


def add_path_python_path(path):
  sys.path.append(path)


def print_classes(module_name):
  module_info = pyclbr.readmodule(module_name)
  print(module_info)

  for item in module_info.values():
    print(item.name)


def import_all_modules_in_path(path,module_name_filter):
  __all__ = []
  for loader, module_name, is_pkg in pkgutil.walk_packages([path]):
    print(module_name)
    if module_name_filter(module_name):
      print(module_name)
      try:
        __all__.append(module_name)
        _module = loader.find_module(module_name).load_module(module_name)
        globals()[module_name] = _module
      except:
        traceback.print_exc()
        print(f"failed while loading {module_name}.continue please")



def get_all_subclasses_of_pynamodb(path):
  modules = import_all_modules_in_path(path,lambda x: "model" in x)
  list(map(print_classes,modules))



if __name__ == '__main__':
  add_path_python_path(f'{str(Path.home())}/projects/git-projects/daftar/webserver')
  get_all_subclasses_of_pynamodb(f"{str(Path.home())}/projects/git-projects/daftar/webserver/main/model")