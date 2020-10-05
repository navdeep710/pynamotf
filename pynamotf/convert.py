"conversion logic for pynamo models -> terraform representation"

import json, pynamodb.attributes
from .formatter import Raw, Indenter
from .models import TFBlock, TFResource

# translation lookup. warning: 'RANGE' is a guess
KEY_TYPES = {'HASH': 'hash_key', 'RANGE': 'range_key'}
IGNORE_CAPACITY_CHANGES = TFBlock('lifecycle', [('ignore_changes', Raw('[read_capacity, write_capacity]'))])

def attr_type(attr):
  "get shortcode for terraform attribute type from a pynamo attribute instance"
  # warning: codebase makes it look like these are one-letter codes, but REPL prints out 'String'. Cross fingers.
  return attr.attr_type[0]

def envify(name):
  "turn a name into a per-env name"
  return '%s-${var.envname}' % name

def render_model(model, billing_mode='PROVISIONED', tags=None, ignore_capacity=True):
  "render a dynamo model as terraform"
  res = TFResource('aws_dynamodb_table', model.Meta.table_name)
  res.entries.append(('name', envify(model.Meta.table_name))) # envname bc this is globally unique
  if billing_mode == 'PROVISIONED':
    res.entries.append(('read_capacity', model.Meta.read_capacity_units))
    res.entries.append(('write_capacity', model.Meta.write_capacity_units))
  res.entries.append(('billing_mode', billing_mode))
  if ignore_capacity:
    res.entries.append(IGNORE_CAPACITY_CHANGES)

  # indexes
  all_index_keys = set()
  for index in model._get_indexes()['global_secondary_indexes']:
    assert index['projection']['ProjectionType'] != 'INCLUDE' # we don't support 'non_key_attributes' field?
    dets = [
      # note: not sure this needs to be envified (i.e. globally unique name) but no harm in it probably
      ('name', envify(index['index_name'])),
      ('projection_type', index['projection']['ProjectionType']),
    ]
    if billing_mode == 'PROVISIONED':
      dets.append(('write_capacity', index['provisioned_throughput']['WriteCapacityUnits']))
      dets.append(('read_capacity', index['provisioned_throughput']['ReadCapacityUnits']))
    index_keys = set()
    for key in index['key_schema']:
      dets.append((KEY_TYPES[key['KeyType']], key['AttributeName']))
      index_keys.add(key['AttributeName'])
      all_index_keys.add(key['AttributeName'])
    res.entries.append(TFBlock('global_secondary_index', dets))

  for name, attr in model.get_attributes().items():
    if attr.is_hash_key:
      res.entries.append(('hash_key', name))
    elif attr.is_range_key:
      res.entries.append(('range_key', name))
    elif name not in all_index_keys:
      # note: index creation fails if index key isn't an attr
      continue
    # following only happens if hash or range key, or key for an index
    res.entries.append(TFBlock('attribute', [
      ('name', name),
      ('type', attr_type(attr)),
    ]))
  if tags:
    res.entries.append(('tags', tags))
  print(str(res.format(Indenter())))
