import random
import asyncio
from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import ANSI
from prompt_toolkit.output.color_depth import ColorDepth
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from io import StringIO

WIDTH = 30
HEIGHT = 15
TICK_RATE = 0.12

class SnakeGame:
    def __init__(self):
        self.reset()

    def reset(self):
        self.snake = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = (1, 0)
        self.food = self.spawn_food()
        self.score = 0
        self.game_over = False

    def spawn_food(self):
        while True:
            pos = (random.randint(1, WIDTH - 2), random.randint(1, HEIGHT - 2))
            if pos not in self.snake:
                return pos

    def change_direction(self, dx, dy):
        if (dx, dy) != (-self.direction[0], -self.direction[1]):
            self.direction = (dx, dy)

    def update(self):
        if self.game_over:
            return

        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        if (
            new_head[0] <= 0
            or new_head[0] >= WIDTH - 1
            or new_head[1] <= 0
            or new_head[1] >= HEIGHT - 1
            or new_head in self.snake
        ):
            self.game_over = True
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.food = self.spawn_food()
        else:
            self.snake.pop()

    def render(self):
        grid = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]

        for x in range(WIDTH):
            grid[0][x] = "#"
            grid[HEIGHT - 1][x] = "#"
        for y in range(HEIGHT):
            grid[y][0] = "#"
            grid[y][WIDTH - 1] = "#"

        fx, fy = self.food
        grid[fy][fx] = "●"

        for i, (x, y) in enumerate(self.snake):
            grid[y][x] = "█" if i == 0 else "▓"

        lines = ["".join(row) for row in grid]
        board = "\n".join(lines)

        text = Text()
        text.append(board, style="bold green")
        text.append(f"\n\nScore: {self.score}", style="bold yellow")

        if self.game_over:
            text.append(
                "\n\nGAME OVER - Press R to Restart or Q to Quit",
                style="bold red",
            )

        return Align.center(
            Panel(text, title="Snake", border_style="bright_blue")
        )

async def run_snake():
    game = SnakeGame()
    kb = KeyBindings()

    @kb.add("up")
    def _(event):
        game.change_direction(0, -1)

    @kb.add("down")
    def _(event):
        game.change_direction(0, 1)

    @kb.add("left")
    def _(event):
        game.change_direction(-1, 0)

    @kb.add("right")
    def _(event):
        game.change_direction(1, 0)

    @kb.add("r")
    def _(event):
        if game.game_over:
            game.reset()

    @kb.add("q")
    def _(event):
        event.app.exit()

    def get_text():
        buffer = StringIO()
        temp_console = Console(
            file=buffer,
            force_terminal=True,
            color_system="standard",
        )
        temp_console.print(game.render())
        return ANSI(buffer.getvalue())

    app = Application(
        layout=Layout(Window(FormattedTextControl(get_text))),
        key_bindings=kb,
        full_screen=True,
        style=Style.from_dict({
            "": "bg:#000000 #ffffff",
        }),
        color_depth=ColorDepth.DEPTH_8_BIT,
    )

    async def game_loop():
        while True:
            await asyncio.sleep(TICK_RATE)
            game.update()
            app.invalidate()

    asyncio.create_task(game_loop())
    await app.run_async()

def main():
    asyncio.run(run_snake())

