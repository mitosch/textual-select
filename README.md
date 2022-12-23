# Textual: Select

A simple select widget (aka dropdown) for [textual](https://github.com/Textualize/textual) with an optional search field.

## Usage

```python
from textual_select import Select

dropdown_data = [
    {"value": 0, "text": "Pick-Up"},
    {"value": 1, "text": "SUV"},
    {"value": 2, "text": "Hatchback"},
    {"value": 3, "text": "Crossover"},
    {"value": 4, "text": "Convertible"},
    {"value": 5, "text": "Sedan"},
    {"value": 6, "text": "Sports Car"},
    {"value": 7, "text": "Coupe"},
    {"value": 8, "text": "Minivan"}
]

Select(
    placeholder="please select",
    items=dropdown_data,
    list_mount="#main_container"
)
```

## Installation

```bash
pip install textual-select
```

Requires textual 0.6.0 or later.

## Limitations

This textual widget is in early stage and has some limitations:

* It needs a specific mount point (`list_mount`) where the dropdown list
  shall appear. This is needed because the container widget with the select
  itself could be too small. Maybe in future versions this will no longer
  needed.
* Mouse support is currently not implemented and will follow.
* Once an entry is selected, there is no possibility to "un-select" an entry.

## Similar Widgets

* If you are looking for an autocomplete, please refer to
  [textual-autocomplete](https://github.com/darrenburns/textual-autocomplete)
  by Darren Burns.
