from typing import List, Reversible, Tuple
import textwrap

import tcod

import color

class Message:
    def __init__(self, text: str, fg: Tuple[int, int, int]):
        self.text = text
        self.fg = fg
        self.count = 1

    @property
    def full_text(self) -> str:
        if self.count > 1:
            return f"{self.text} (x{self.count})"
        return self.text

class MessageLog:
    def __init__(self) -> None:
        self.messages: List[Message] = []

    def add_message(self, text: str, fg: Tuple[int, int, int] = color.white, *, stack: bool = True,) -> None:
        """Add a message to the log"""
        if stack and self.messages and text == self.messages[-1].text:
            self.messages[-1].count += 1
        else:
            self.messages.append(Message(text, fg))

    def render(self, console: tcod.Console, x: int, y: int, width: int, height: int,) -> None:
        """Render the log over the given area"""
        self.render_messages(console, x, y, width, height, self.messages)

    @staticmethod
    def render_messages(
        console: tcod.Console, x: int, y: int, width: int, height: int, messages: Reversible[Message],
    ) -> None:
        """Render the messages provided"""
        y_offset = height - 1

        for message in reversed(messages):
            for line in reversed(textwrap.wrap(message.full_text, width)):
                console.print(x=x, y=y + y_offset, string=line, fg=message.fg)
                y_offset -= 1
                if y_offset < 0:
                    return