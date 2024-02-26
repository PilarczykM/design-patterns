from abc import ABC
import enum
from typing import List


class OutputFormat(enum.Enum):
    MARKDOWN = enum.auto()
    HTML = enum.auto()


class ListStrategy(ABC):
    def start(self, buffer: List[str]) -> None:
        pass

    def end(self, buffer: List[str]) -> None:
        pass

    def add_list_item(self, buffer: List[str], item: str) -> None:
        pass


class MarkdownListStrategy(ListStrategy):
    def add_list_item(self, buffer: List[str], item: str) -> None:
        buffer.append(f"  * {item}\n")


class HtmlListStrategy(ListStrategy):
    def start(self, buffer: List[str]) -> None:
        buffer.append("<ul>\n")

    def end(self, buffer: List[str]) -> None:
        buffer.append("</ul>\n")

    def add_list_item(self, buffer: List[str], item: str) -> None:
        buffer.append(f"  <li>{item}</li>\n")


class TextProcessor:
    def __init__(self, list_strategy: ListStrategy = MarkdownListStrategy()) -> None:
        self.buffer: List[str] = []
        self.list_strategy = list_strategy

    def append_list(self, items: List[str]):
        self.list_strategy.start(self.buffer)
        for item in items:
            self.list_strategy.add_list_item(self.buffer, item)
        self.list_strategy.end(self.buffer)

    def set_format(self, format: OutputFormat):
        match format:
            case OutputFormat.MARKDOWN:
                self.list_strategy = MarkdownListStrategy()
            case OutputFormat.HTML:
                self.list_strategy = HtmlListStrategy()
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
