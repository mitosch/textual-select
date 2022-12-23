# Textual: Select

A simple select widget (aka dropdown) for [textual](https://github.com/Textualize/textual) with an optional search field.

![select_focus](https://user-images.githubusercontent.com/922559/209305346-6b8971b1-7a3a-4424-bdf8-c439b9d74e28.png)

![select_open](https://user-images.githubusercontent.com/922559/209305349-84f39432-b1e4-405e-8854-a8d7a33230ae.png)

![select_search](https://user-images.githubusercontent.com/922559/209305352-9ad2e7c1-9dc6-435f-b1bd-8dba5f5b2642.png)


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
* It can only open below, not above: Make sure to reserve space below the
  dropdown.
* The dropdown list has a fixed height of 5 entries. This will be configurable
  in future versions.

## Similar Widgets

* If you are looking for an autocomplete, please refer to
  [textual-autocomplete](https://github.com/darrenburns/textual-autocomplete)
  by Darren Burns.
