import unittest

from textual_select import Select


class AttributeCases(unittest.TestCase):
    def test_empty_attributes(self):
        with self.assertRaises(TypeError) as context:
            Select()

        self.assertTrue(
            "missing 2 required positional arguments" in str(context.exception)
        )

    def test_required_attributes(self):
        dropdown_data = [
            {"value": 0, "text": "Pick-Up"},
            {"value": 1, "text": "SUV"},
            {"value": 2, "text": "Hatchback"},
        ]

        Select(items=dropdown_data, list_mount="#main_container")
