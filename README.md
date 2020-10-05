# pynamotf

This converts [pynamodb](https://github.com/pynamodb/PynamoDB) models to terraform. Pynamodb is a python mapper for dynamodb.

Warning: this is not maintained. I wrote this for a project that I no longer operate.

I hope this is useful to you as a timesaver, but if you're using this in production code, be careful.

## Installation

```
pip install git+https://github.com/abe-winter/pynamotf.git
```

## Usage

```python
from pynamodb.models import Model
from pynamotf.convert import model_to_resource

# define your models somewhere
class Table(Model):
  ...

# for each model, format it
print(str(model_to_resource(Table).format()))
```
