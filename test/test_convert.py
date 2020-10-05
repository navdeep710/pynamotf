from pynamodb.models import Model
from pynamodb.indexes import GlobalSecondaryIndex, KeysOnlyProjection
from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute, JSONAttribute
from pynamotf.convert import model_to_resource

def make_meta(**kwargs):
  "helper to populate all the common meta fields"
  class Meta:
    read_capacity_units = 1
    write_capacity_units = 1

  for key, val in kwargs.items():
    setattr(Meta, key, val)

  return Meta

class Index(GlobalSecondaryIndex):
  Meta = make_meta(index_name='index', projection=KeysOnlyProjection())

  userid = UnicodeAttribute(hash_key=True)

class TableWithIndex(Model):
  Meta = make_meta(table_name='with_index')

  userid = UnicodeAttribute(hash_key=True)
  index = Index()

class TableWithRange(Model):
  Meta = make_meta(table_name='with_range')

  key1 = UnicodeAttribute(hash_key=True)
  key2 = UnicodeAttribute(range_key=True)
  date_attr = UTCDateTimeAttribute(null=True)
  json_attr = JSONAttribute()

def test_with_index():
  assert str(model_to_resource(TableWithIndex).format()) == """resource aws_dynamodb_table with_index {
  name = "with_index"
  read_capacity = 1
  write_capacity = 1
  billing_mode = "PROVISIONED"
  lifecycle {
    ignore_changes = [read_capacity, write_capacity]
  }
  global_secondary_index {
    name = "index"
    projection_type = "KEYS_ONLY"
    write_capacity = 1
    read_capacity = 1
    hash_key = "userid"
  }
  hash_key = "userid"
  attribute {
    name = "userid"
    type = "S"
  }
}"""

def test_with_range():
  assert str(model_to_resource(TableWithRange).format()) == """resource aws_dynamodb_table with_range {
  name = "with_range"
  read_capacity = 1
  write_capacity = 1
  billing_mode = "PROVISIONED"
  lifecycle {
    ignore_changes = [read_capacity, write_capacity]
  }
  hash_key = "key1"
  attribute {
    name = "key1"
    type = "S"
  }
  range_key = "key2"
  attribute {
    name = "key2"
    type = "S"
  }
}"""
