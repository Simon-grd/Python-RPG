# animation.py
from rich.console import Console
from rich.live import Live
from rich.progress import Progress, BarColumn
from rich.text import Text
import time

def attack_animation(live=None):
    frames = ["⚔️", "🔥", "💥", "✨"]
    for frame in frames:
        if live:
            live.update(Text(frame, style="bold red"))
        else:
            print(frame)
        time.sleep(0.3)

def show_animated_ascii(ascii_art):
    console = Console()
    colors = ["#FF69B4", "#4B0082", "#0000FF", "#00FF00", "#FFFF00", "#FF7F00", "#FF0000"]
    for color in colors:
        console.clear()
        console.print(ascii_art, style=color)
        time.sleep(0.1)

def animate_xp_gain(start, end, required):
    progress = Progress(
        "[progress.description]{task.description}",
        BarColumn(bar_width=None),
        "[progress.percentage]{task.percentage:>3.0f}%"
    )
    with Live(progress, refresh_per_second=20):
        task = progress.add_task("XP", total=required)
        for xp in range(start, end + 1):
            progress.update(task, advance=1, description=f"{xp}/{required} XP")
            time.sleep(0.02)

def scroll_text(text, style="white", delay=0.03):
    console = Console()
    for char in str(text):
        console.print(char, style=style, end="", highlight=False)
        time.sleep(delay)
    print()

def screen_transition(style="cyan", length=30):
    console = Console()
    for i in range(length):
        console.print("▉" * i, style=style, end="\r")
        time.sleep(0.03)
    console.clear()
