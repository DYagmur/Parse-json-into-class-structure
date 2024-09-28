from typing import Union, List, Dict
import json

class Item:
    def __init__(self, name: str, value: Union[int, str, List['Item']]):
        self.name = name
        self.value = value

    # Method 1: Sum numeric values either by name or recursively if no name is given
    def sum_numeric(self, name: str = None) -> int:
        total = 0
        if isinstance(self.value, list):  # If the value is a list of items
            for item in self.value:
                if isinstance(item, Item):
                    if name is None:
                        total += item.sum_numeric()  # Recursive case: sum all integers
                    elif item.name == name and isinstance(item.value, int):
                        total += item.value
        elif isinstance(self.value, int) and (name is None or self.name == name):
            total += self.value
        return total

    # Method 2: Recursively search for an item by name and return its value
    def get_by_name(self, name: str) -> Union[int, str, None]:
        if self.name == name:
            return self.value
        if isinstance(self.value, list):
            for item in self.value:
                if isinstance(item, Item):
                    result = item.get_by_name(name)
                    if result is not None:
                        return result
        return None

    # Method 3: Find the first item with a matching value and return its name
    def get_by_value(self, value: Union[int, str]) -> Union[str, None]:
        if self.value == value:
            return self.name
        if isinstance(self.value, list):
            for item in self.value:
                if isinstance(item, Item):
                    result = item.get_by_value(value)
                    if result is not None:
                        return result
        return None

    # Method 4: Access items with the syntax item["name"]
    def __getitem__(self, name: str) -> 'Item':
        if self.name == name:
            return self
        if isinstance(self.value, list):
            for item in self.value:
                if isinstance(item, Item):
                    found_item = item[name]
                    if found_item:
                        return found_item
        return None

    def __repr__(self):
        return f"Item(name={self.name}, value={self.value})"

# Function to parse JSON into an Item object
def json_to_item(json_string: str) -> Item:
    def parse_item(item_data: Dict) -> Item:
        name = item_data["name"]
        value = item_data["value"]
        if isinstance(value, list):
            value = [parse_item(i) for i in value]
        return Item(name, value)

    json_obj = json.loads(json_string)
    return parse_item(json_obj)

# Example JSON Input
json_input = '{"name": "root", "value": [{"name": "item2", "value": "a string"}, {"name": "item3", "value": 5}]}'

# Parse the JSON into an Item object
root_item = json_to_item(json_input)

# Test methods
print("Sum numeric:", root_item.sum_numeric())  # Should output: 5
print("Get by name 'item2':", root_item.get_by_name('item2'))  # Should output: 'a string'
print("Get by value 5:", root_item.get_by_value(5))  # Should output: 'item3'
print("Access using item['item3']:", root_item["item3"])  # Should output: Item(name=item3, value=5)


##done!