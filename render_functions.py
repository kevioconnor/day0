from __future__ import annotations
import typing
from typing import TYPE_CHECKING
import color

if TYPE_CHECKING:
    from tcod import Console

def render_bar(console: Console, current_val: int, max_val: int, total_width: int) -> None:
    bar_width = int(float(current_val) / max_val * total_width)
    console.draw_rect(x=0, y=45, width=20, height=1, ch=1, bg=color.bar_empty)

    if bar_width > 0:
        console.draw_rect(x=0, y=45, width=bar_width, height=1, ch=1, bg=color.bar_filled)

    console.print(x=1, y=45, string=f"HP: {current_val}/{max_val}", fg=color.bar_text)