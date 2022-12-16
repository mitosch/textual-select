from __future__ import annotations

from textual.widget import Widget, events
from textual.containers import Vertical
from textual.widgets import Label, ListView, ListItem, Input
from textual.reactive import reactive
from textual.message import Message

from textual._segment_tools import line_crop
from rich.highlighter import Highlighter
from rich.console import RenderableType, Console, ConsoleOptions, RenderResult
from rich.segment import Segment
from rich.text import Text

# from textual import log


class SelectListSearchInput(Input):
    """Input for searching through the list."""

    DEFAULT_CSS = """
    SelectListSearchInput {
        border: none;
        background: transparent;
        border-bottom: tall $background;
    }
    SelectListSearchInput:focus {
        border: none;
        border-bottom: tall $accent;
    }
    """

    def __init__(
        self,
        select_list: SelectList,
        value: str | None = None,
        placeholder: str = "",
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ) -> None:
        super().__init__(
            value=value,
            placeholder=placeholder,
            name=name,
            id=id,
            classes=classes
        )
        self.select_list = select_list

    def watch_value(self, value):
        self.select_list.list_view.clear()
        self.select_list.items_filtered = []
        for item in self.select_list.items:
            if value.lower() in item["text"].lower():
                self.select_list.list_view.append(ListItem(Label(item["text"])))
                self.select_list.items_filtered.append(item)

    def action_scroll_down(self) -> None:
        self.select_list.list_view.action_cursor_down()

    def action_scroll_up(self) -> None:
        self.select_list.list_view.action_cursor_up()


class SelectList(Widget):
    DEFAULT_CSS = """
    SelectList {
      layer: dialog;
      background: $boost;
      border: tall $accent;
      /*
      height: 5;
      min-height: 5;
      */
      display: none;
    }
    SelectList.--search ListView {
      padding-top: 1;
    }
    SelectList ListItem {
      background: transparent;
      padding: 0 2;
    }
    SelectList ListView:focus > ListItem.--highlight {
      /*background: $accent 20%;*/
    }
    SelectList SelectListSearchInput {
      border: none;
      border-bottom: wide $panel;
    }
    """

    def __init__(
        self,
        select: Select,
        items: list,
        *children: Widget,
        search: bool | None = False,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ) -> None:
        if search:
            # when a search is there, add a class for pad-top the list
            classes = f"{str(classes)} --search"
        super().__init__(name=name, id=id, classes=classes)
        self.select = select
        self.items = items
        self.items_filtered = items
        self.search = search

    def compose(self):
        widgets = []
        list_items = []
        for item in self.items:
            list_items.append(ListItem(Label(item["text"])))
        self.list_view = ListView(*list_items)

        if self.search:
            widgets.append(SelectListSearchInput(select_list=self))

        widgets.append(self.list_view)

        yield Vertical(*widgets)

    def on_key(self, event: events.Key) -> None:
        # NOTE: the message ListView.Selected has drawbacks, we can't use:
        #   * emitted when opened drop-down list
        #   * not emitted, when enter pressed on the initially highlighted ListItem
        #   * emitted on single click (can be ok, but would close immediately)

        if event.key == "enter":
            if self.list_view.index is not None:
                # index can be None, if a search results in no entries
                # => do not change select value in this case
                self.select.text = self.items_filtered[self.list_view.index]["text"]
                self.select.value = self.items_filtered[self.list_view.index]["value"]
            self.display = False
            self.select.focus()

        if event.key == "tab" or event.key == "shift+tab":
            # suppress tab (blur) when drop-down is open.
            # looks like Gtk is handling it the same.
            event.prevent_default()


class _SelectRenderable:
    # TODO: make the chevron right aligned and do not crop it
    # OPTIMIZE: check if this code is really needed or the renderable can be skipped
    def __init__(self, select: Select) -> None:
        self.select = select

    def __rich_console__(
            self,
            console: "Console",
            options: "ConsoleOptions"
    ) -> "RenderResult":
        select = self.select
        # result = select._value + " ⌄"
        result = select._text + " \u25bc"  # <= triangle filled down
        width = select.content_size.width
        segments = list(result.render(console))
        line_length = Segment.get_line_length(segments)

        line = line_crop(
            list(segments),
            select.view_position,
            select.view_position + width,
            line_length
        )
        yield from line


class Select(Widget, can_focus=True):
    """A select widget with a drop-down."""
    # TODO: reset SelectListSearchInput when closing (and re-opening)
    # TODO: validate given items (list of dicts not like value, text)
    # OPTIMIZE: implement pg-down/up, end/home
    # OPTIMIZE: when empty, show dimmed text (e.g. "no entries")
    # OPTIMIZE: get rid of self.app.query_one(self.list_mount)
    # OPTIMIZE: option: individual height
    # OPTIMIZE: mini-bug: resize not nice when opened (edge case...)
    # OPTIMIZE: auto-select by key-press without search? (hard)
    # TODO: mouse: select highlighted ListItem (aka double-click)
    # TODO: mouse: close on blur
    # TODO: mouse: hover whole line (not only word of ListItem)
    # TODO: mouse: scrolling (baah... so many mouse-things)

    DEFAULT_CSS = """
    Select {
      background: $boost;
      color: $text;
      padding: 0 2;
      border: tall $background;
      height: 1;
      min-height: 1;
    }
    Select:focus {
      border: tall $accent;
    }
    """

    value = reactive("", layout=True, init=False)
    view_position = reactive(0)

    def __init__(
            self,
            items: list,
            list_mount: str,
            text: str | None = "",
            search: bool | None = False,
            placeholder: str = "",  # not implemented yet
            highlighter: Highlighter | None = None,
            name: str | None = None,
            id: str | None = None,
            classes: str | None = None
    ) -> None:
        self.select_classes = classes
        super().__init__(name=name, id=id, classes=classes)
        # if text is not None:
        #     self.text = text
        self.text = text
        self.items = items
        self.list_mount = list_mount
        self.highlighter = highlighter
        self.search = search

        self.select_list = None

    def render(self) -> RenderableType:
        return _SelectRenderable(self)

    @property
    def _text(self) -> Text:
        """Value of the current selection as text."""
        text = Text(self.text, no_wrap=True, overflow="ignore")
        return text

    def on_mount(self):
        # NOTE: mount-point for list is mandatory for the time beeing
        #
        # possibility to automatically find mount point of the drop-down list:
        # * find an ancestor, which's height is greater than the lists height
        # * if it fails (screen size too small, container too small), take
        #   screen container
        #
        # pseudo code:

        # for ancestor in self.ancestors:
        #     if issubclass(ancestor.__class__, Widget):
        #           it's a normal widget
        #     else if issubclass(..., App):
        #           use this child...
        if self.select_list is None:
            self.select_list = SelectList(
                select=self,
                items=self.items,
                search=self.search,
                classes=self.select_classes
            )
            self.app.query_one(self.list_mount).mount(self.select_list)

    def on_key(self, event: events.Key) -> None:
        if event.key == "enter":
            self.select_list.display = True
            self.select_list.styles.width = self.outer_size.width

            # OPTIMIZE: this could be done more configurable
            default_height = 5
            if self.search:
                default_height = 8
            if self.select_list.styles.height is None:
                self.select_list.styles.height = default_height
            if self.select_list.styles.min_height is None:
                self.select_list.styles.min_height = default_height
            if len(self.items) < 5:
                height = max(1, len(self.items))
                self.select_list.styles.height = height
                self.select_list.styles.min_height = height

            # calculate the offset by using the mount-point's offset:
            # setting the offset directly from self.region (Select widget)
            # has the header *not* included, therefore we need to subtract
            # the mount-point's offset.
            #
            # further explanation (or assumption):
            # it looks like the mount point has a relative offset, e.g. below
            # the header. setting the offset of the list directly seams to be
            # absolute.
            self.select_list.offset = self.region.offset - \
                self.app.query_one(self.list_mount).content_region.offset

            if self.search:
                self.select_list.query_one("SelectListSearchInput").focus()
            else:
                self.select_list.query("ListView").first().focus()

    async def watch_value(self, value: str) -> None:
        await self.emit(self.Changed(self, value))

    class Changed(Message, bubble=True):
        """Value was changed."""

        def __init__(self, sender: Select, value: str) -> None:
            super().__init__(sender)
            self.value = value
            self.select = sender
