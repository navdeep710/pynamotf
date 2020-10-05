"intermediate representations for terraform"

from dataclasses import dataclass, field

@dataclass
class TFBlock:
  kind: str
  entries: list # same as TFResource entries

@dataclass
class TFResource:
  "terraform formatter for resources"
  res_type: str
  name: str
  entries: list = field(default_factory=list) # list of either (k, v) or TFBlock. v can be (string, int, dict)

  def format(self, indenter):
    indenter.append('resource %s %s {' % (self.res_type, self.name))
    with indenter.block():
      for entry in self.entries:
        format(indenter, entry)
    indenter.append('}')
    return indenter
