import glob
import os
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


def import_all_modules_in_path(path):
  import os
  from glob import glob
  for file in glob( f"{path}*.py"):
    name = os.path.splitext(os.path.basename(file))[0]
    # add package prefix to name, if required
    module = __import__(name)
    for member in dir(module):
      print(member)
  return []

def get_all_subclasses_of_pynamodb(path):
  modules  =import_all_modules_in_path(path)
  list(map(print_classes,modules))



if __name__ == '__main__':
    get_all_subclasses_of_pynamodb(f"{str(Path.home())}/projects/git-projects/daftar/webserver/main/model")