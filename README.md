# Textual: Select

A simple select widget (aka dropdown) for [textual](https://github.com/Textualize/textual).

Requires textual 0.6.0 or later.

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
