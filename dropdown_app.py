from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Header, Footer, Label, Input

from widgets import Select


class DropdownApp(App):
    CSS = """
    #main_container {
        padding: 2 5;
    }

    #main_container > Label {
        margin: 3 1 1 1;
    }
    """

    def compose(self) -> ComposeResult:
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

        yield Header()
        yield Footer()
        yield Vertical(
            Label("Car type:"),
            Select(
                text="please select",
                items=dropdown_data,
                list_mount="#main_container"
            ),

            Label("Car type (searchable):"),
            Select(
                text="please select",
                items=dropdown_data,
                search=True,
                list_mount="#main_container"
            ),

            Label("Selected value:"),
            Input(value="-", id="selected_value"),

            id="main_container"
        )

    def on_select_changed(self, event: Select.Changed) -> None:
        self.query_one("#selected_value").value = str(event.value)


if __name__ == "__main__":
    app = DropdownApp()
    app.run()
