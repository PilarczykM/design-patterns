from abc import ABC, abstractmethod
import enum
from typing import Callable, List


class OutputFormat(enum.Enum):
    MARKDOWN = enum.auto()
    HTML = enum.auto()


StartListStrategy = Callable[[List[str]], None]
EndListStrategy = Callable[[List[str]], None]
AddListItemStrategy = Callable[[List[str], str], None]


def start_markdown_strategy(_: List[str]) -> None:
    pass


def end_markdown_strategy(_: List[str]) -> None:
    pass


def add_list_item_markdown_strategy(buffer: List[str], item: str) -> None:
    buffer.append(f"  * {item}\n")


def start_html_strategy(buffer: List[str]) -> None:
    buffer.append("<ul>\n")


def end_html_strategy(buffer: List[str]) -> None:
    buffer.append("</ul>\n")


def add_list_item_html_strategy(buffer: List[str], item: str) -> None:
    buffer.append(f"  <li>{item}</li>\n")


class TextProcessor:
    def __init__(
        self,
        start_list_strategy: StartListStrategy = start_markdown_strategy,
        end_list_strategy: EndListStrategy = end_markdown_strategy,
        add_list_item_strategy: AddListItemStrategy = add_list_item_markdown_strategy,
    ) -> None:
        self.buffer: List[str] = []
        self.start_list_strategy = start_list_strategy
        self.end_list_strategy = end_list_strategy
        self.add_list_item_strategy = add_list_item_strategy

    def append_list(self, items: List[str]):
        self.start_list_strategy(self.buffer)
        for item in items:
            self.add_list_item_strategy(self.buffer, item)
        self.end_list_strategy(self.buffer)

    def set_format(self, format: OutputFormat):
        match format:
            case OutputFormat.MARKDOWN:
                self.start_list_strategy = start_markdown_strategy
                self.end_list_strategy = end_markdown_strategy
                self.add_list_item_strategy = add_list_item_markdown_strategy
            case OutputFormat.HTML:
                self.start_list_strategy = start_html_strategy
                self.end_list_strategy = end_html_strategy
                self.add_list_item_strategy = add_list_item_html_strategy
            case _:
                raise ValueError("Unknown strategy!")

    def clear(self):
        self.buffer.clear()

    def __str__(self):
        return "".join(self.buffer)


if __name__ == "__main__":
    items = ["foo", "bar", "baz"]
    text_processor = TextProcessor()
    text_processor.append_list(items)
    print(text_processor)

    text_processor.set_format(OutputFormat.HTML)
    text_processor.clear()
    text_processor.append_list(items)
    print(text_processor)
