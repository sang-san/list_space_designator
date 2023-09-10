# pricelist_space_designator

Compact class that can be used to distribute a given list of values into any specified number of sublists with adjustable max capacity, while maintaining equal commonness when possible.

Example:
```py
from separator import Pricelist_Separator_Middleware

separator_instance = Pricelist_Separator_Middleware(print_runtime=False)
print(separator_instance.separate_list_into_spaces([
  "value_one",
  "value_two",
  "value_three"
], [
  ("list_name_one", 4), # (list_name, max_capacity)
  ("list_name_two", 2),
  ("list_name_three", 2),
  ("list_name_four", 2),
]))
```
Output:
```
{
  'list_name_one': [
    'value_one',
    'value_two',
    'value_three'
  ],
  'list_name_two': [
    'value_one',
    'value_two'
  ],
  'list_name_three': [
    'value_three',
    'value_one'
  ],
  'list_name_four': [
    'value_two',
    'value_three'
  ]
}
```
