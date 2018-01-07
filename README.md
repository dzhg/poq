[![Build Status](https://travis-ci.org/dzhg/poq.svg?branch=master)](https://travis-ci.org/dzhg/poq)

poq (Python Object Query utility)
=================================

`poq` is inspired by `jq` (a JSON processor, https://stedolan.github.io/jq/).

While `jq` is a very powerful tool but `poq` only has very limited features now.

`poq` supports `dict` and `list` (for now).

Although sometimes, a Python `dict` or `list` can be converted to JSON, then use `jq` to process it. However, in some 
cases, it requires additional efforts for the conversion, especially, when `class` is involved.

Consider below example:

```
class Book:
    def __init__(self, title, price):
        self._title = title
        self._price = price
        
    def get_price(self):
        return self._price
     
    # ... more code
    
data = {
    "classic": {
        "count": 2
        "collection": [ Book("fiction1", 23.99), Book("fiction2", 13.99) ]
    },
    "mystery": {
        "count": 1
        "collection": [ Book("mystery1", 10.59) ]
    }
}
```

To convert `data` to JSON, a custom converter of class `Book` need to be created. If the converter is required by other 
code anyway, it's OK to create one.

But if the only requirement is to easily access the deep structure, `poq` would be handy.

```
classic_total = reduce(lambda x, y: x + y, list(map(lambda x: x.get_price(), poq.query(".classic.collection[]", data))))
```

Supported Filters
-----------------

### Identity Filter (.)

Returns the object itself. For example:

```
data = {
    "name": "poq",
    "language": "Python",
    "version": "0.1.0",
    "dependencies": [
        {
            "name": "ply",
            "version": "3.1.0"
        },
        {
            "name": "dummy",
            "version": "0.0.1"
        }
    ]
}

result = poq.query(".", data)

# `result` will be identical to `data`
```

### Dict Field Filter (.key)

Returns the value of the key in the dict. For example:

```
result = poq.query(".name", data)

assert result == "poq"
```

### List Iterator Filter ([])

Returns the value as a list. This filter just tells `poq` the data should be handled as a list.

For example:

```
# won't work
poq.query(".dependencies.name", data)

# works
poq.query(".dependencies[].name", data)

# result
["ply", "dummy"]
```

### List Index Filter ([idx])

```
poq.query(".dependencies[0].name", data)

# result
"ply"
```

### List Slice Filter ([start:end])

```
poq.query(".dependencies[0:].name", data)

# result
["ply", "dummy"]
```
