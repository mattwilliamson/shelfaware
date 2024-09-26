

```python
from inventory import InventoryManager

manager = InventoryManager()

# Add user
manager.add_user("john_doe")

# Add categories
manager.add_category("Produce")
manager.add_category("Meat")

# Add items
manager.add_item("john_doe", "Carrot", 5, "Produce")
manager.add_item("john_doe", "Ground Beef", 2, "Meat")

# View user's items
print(manager.get_user_items("john_doe"))  # ['Carrot', 'Ground Beef']

# View items by category
print(manager.get_items_by_category("john_doe", "Produce"))  # ['Carrot']
```

## Testing

```sh
python -m unittest discover -s shelfaware/food_inventory/tests
```