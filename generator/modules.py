import importlib
import itertools
import pkgutil
import pyclbr
import sys
import traceback
from functools import partial
# import fire
from pathlib import Path

from pynamotf.convert import model_to_resource


def add_path_python_path(path):
  sys.path.append(path)

def convert_super_attr_to_name(super_attribute):
  if isinstance(super_attribute,str):
    return super_attribute
  if isinstance(super_attribute, pyclbr.Class):
    return super_attribute.name


def get_classes(module_name, type_to_check):
  module_info = pyclbr.readmodule(module_name)
  classes = [item for item in module_info.values() if type_to_check in map(lambda x: convert_super_attr_to_name(x),item.super)]
  return classes



def get_class_of_type(class_info,type_to_check):
  if type_to_check in class_info.super:
    return class_info


def import_all_modules_in_path(path,module_name_filter):
  __all__ = []
  for loader, module_name, is_pkg in pkgutil.walk_packages([path]):
    if module_name_filter(module_name):
      print(module_name)
      try:
        __all__.append(module_name)
        _module = loader.find_module(module_name).load_module(module_name)
        globals()[module_name] = _module
      except:
        traceback.print_exc()
        print(f"failed while loading {module_name}.continue please")
  return __all__



def get_all_subclasses_of_pynamodb(path):
  modules = import_all_modules_in_path(path,lambda x: "model" in x)
  print(f"modules detected with model in name {len(modules)}")
  modules_with_class_as_base_model =  list(map(partial(get_classes, type_to_check="BaseModel"), modules))
  print(f"modules inherting from base model are {len(modules_with_class_as_base_model)}")
  return modules_with_class_as_base_model


def get_class_from_classname(module_name,classname):
  m = importlib.import_module(module_name)
  c = getattr(m, classname)
  return c

def generate_terraform_for_class_info_and_write_to_file(class_info,output_directory):
    terraform_scripts = [model_to_resource(get_class_from_classname(clazz.module,clazz.name)) for clazz in class_info]
    with open(f"{output_directory}/{class_info.module}.tf") as terraform_file:
      writable_script = "\n-----------\n".join(terraform_scripts)
      terraform_file.write(writable_script)
    return terraform_scripts



if __name__ == '__main__':
  # add_path_python_path(f'{str(Path.home())}/projects/git-projects/daftar/webserver')
  class_infos = get_all_subclasses_of_pynamodb(f"{str(Path.home())}/projects/git-projects/daftar/webserver/main/model")
  terraform_scripts = [generate_terraform_for_class_info_and_write_to_file(class_info,"/Users/navdeepagarwal/projects/git-projects/daftar/webserver/terraform_dynamodb_tables") for class_info in class_infos if len(class_info) > 0]
  terraform_scripts = list(itertools.chain(*terraform_scripts))
  print(f"length of all terraform scripts to be generated {len(terraform_scripts)}")
  [print(str(terraform_script.format())) for terraform_script in terraform_scripts]