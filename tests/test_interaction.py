import pytest

from textual.app import App, ComposeResult
from textual.containers import Vertical

from textual_select import Select


@pytest.mark.asyncio
async def test_open_close():
    """Focus select, open it, press enter to select and close."""
    class OpenSelectApp(App):
        def compose(self) -> ComposeResult:
            dropdown_data = [
                {"value": 0, "text": "Pick-Up"},
                {"value": 1, "text": "SUV"},
                {"value": 2, "text": "Hatchback"},
            ]

            yield Vertical(
                Select(items=dropdown_data, list_mount="#main_container"),
                id="main_container"
            )
    app = OpenSelectApp()
    async with app.run_test() as pilot:
        assert len(app.query("SelectList")) == 1
        select = app.query_one("Select")
        select_list = app.query_one("SelectList")
        assert select.value == ""
        assert select.text == ""
        await pilot.press("tab")
        assert select_list.display is False
        await pilot.press("enter")
        assert select_list.display is True
        assert select.value == ""
        await pilot.press("enter")
        assert select_list.display is False
        assert select.value == 0
        assert select.text == "Pick-Up"
