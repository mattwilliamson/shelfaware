# OpenFoods API Client Library

A Python client library for interacting with the [Open Food Facts](https://world.openfoodfacts.org) API.

## Features

- Fetch food product information using barcodes.
- Display product images.
- Caching using `requests_cache` for efficient repeated queries.

## Installation

```sh
pip install requests requests_cache Pillow matplotlib
```

## Usage

```python
from openfoods.client import OpenFoodClient

client = OpenFoodClient()
product = client.fetch_product("4099100207149")

if product:
    print(product.product_name)
    client.fetch_image(product)
```

## Testing

```sh
python -m unittest discover openfoods/tests
```