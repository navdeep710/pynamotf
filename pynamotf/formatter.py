"formatting helpers and intermediate representations for terraform"

import json
from contextlib import contextmanager
from dataclasses import dataclass, field

@dataclass
class TFBlock:
  "represent a terraform block (i.e. braced section within a resource)"
  kind: str
  entries: list # same as TFResource entries

@dataclass
class TFResource:
  "terraform formatter for resources"
  res_type: str
  name: str
  entries: list = field(default_factory=list) # list where entries are (k, v) tuple or TFBlock. v can be (string, int, dict)

  def format(self, indenter=None):
    "render this into an indenter, return the indenter"
    indenter = indenter or Indenter()
    indenter.append('resource %s %s {' % (self.res_type, self.name))
    with indenter.block():
      for entry in self.entries:
        format_tf(indenter, entry)
    indenter.append('}')
    return indenter

class Raw(str):
  "marker class to render strings without quotes"

class Indenter:
  "helper to manage writing indented lines"
  def __init__(self):
    self.lines = []
    self.indents = 0
    self.indent = '  '

  @contextmanager
  def block(self):
    "context manager that releases indentation at the end"
    orig = self.indents
    self.indents += 1
    yield
    self.indents = orig

  def append(self, line):
    "add a line, automatically adds indentation at the front"
    self.lines.append(self.indent * self.indents + line)

  def __str__(self):
    "render lines"
    return '\n'.join(self.lines)

def format_tf(indenter, item):
  "render item into indenter"
  if isinstance(item, TFBlock):
    indenter.append('%s {' % item.kind)
    with indenter.block():
      for subitem in item.entries:
        format_tf(indenter, subitem)
    indenter.append('}')
  elif isinstance(item, tuple):
    key, val = item
    if isinstance(val, Raw):
      # note: must come before str -- Raw is also str
      indenter.append('%s = %s' % (key, val))
    elif isinstance(val, (str, int)):
      # note: json for double-quotes
      indenter.append('%s = %s' % (key, json.dumps(val)))
    elif isinstance(val, dict):
      indenter.append('%s = {' % key)
      with indenter.block():
        for tup in val.items():
          format_tf(indenter, tup)
      indenter.append('}')
    else:
      raise TypeError(type(val))
  else:
    raise TypeError("expected TFBlock or tuple")
