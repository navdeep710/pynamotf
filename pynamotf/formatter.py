from contextlib import contextmanager

import json
from .models import TFBlock

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
    orig = self.indents
    self.indents += 1
    yield
    self.indents = orig

  def append(self, line):
    self.lines.append(self.indent * self.indents + line)

  def __str__(self):
    return '\n'.join(self.lines)

def format(indenter, item):
  "render item into indenter"
  if isinstance(item, TFBlock):
    indenter.append('%s {' % item.kind)
    with indenter.block():
      for subitem in item.entries:
        format(indenter, subitem)
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
          format(indenter, tup)
      indenter.append('}')
    else:
      raise TypeError(type(val))
  else:
    raise TypeError("expected TFBlock or tuple")
