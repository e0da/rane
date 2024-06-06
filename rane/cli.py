import numpy as np
import curses
import random
import logging
from PIL import Image

# Configure logging
logging.basicConfig(
    filename="/tmp/water_surface.log", level=logging.DEBUG, format="%(message)s"
)


class WaterSurface:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width))
        self.drops = []

    def add_drop(self, drop):
        self.drops.append(drop)

    def update(self):
        new_grid = self.grid.copy()
        for drop in self.drops:
            self.apply_drop_effect(drop)
            drop.age += 1
        self.grid = new_grid

    def apply_drop_effect(self, drop):
        for dy in range(-drop.radius, drop.radius + 1):
            for dx in range(-drop.radius, drop.radius + 1):
                if 0 <= drop.y + dy < self.height and 0 <= drop.x + dx < self.width:
                    distance = np.sqrt(dx**2 + dy**2)
                    if distance <= drop.radius:
                        self.grid[drop.y + dy, drop.x + dx] += drop.strength * np.cos(
                            distance
                        )

    def save_to_png(self, filename):
        min_value = np.min(self.grid)
        max_value = np.max(self.grid)
        normalized_grid = (self.grid - min_value) / (max_value - min_value) * 255
        image = Image.fromarray(normalized_grid.astype(np.uint8))
        image.save(filename)

    def log_grid(self):
        log_msg = "\n".join(
            ["\t".join([f"{cell:.2f}" for cell in row]) for row in self.grid]
        )
        logging.debug("\n" + log_msg + "\n" + "-" * 50)


class Raindrop:
    def __init__(self, x, y, radius, strength):
        self.x = x
        self.y = y
        self.radius = radius
        self.strength = strength
        self.age = 0


def render(stdscr, surface):
    curses.start_color()
    curses.use_default_colors()
    for i in range(1, 8):
        curses.init_pair(i, i, -1)

    height, width = stdscr.getmaxyx()
    stdscr.clear()
    min_value = np.min(surface.grid)
    max_value = np.max(surface.grid)
    for y in range(min(height, surface.height)):
        for x in range(min(width, surface.width)):
            value = surface.grid[y, x]
            if max_value == min_value:
                color_pair = 1
            else:
                color_pair = int(1 + 6 * (value - min_value) / (max_value - min_value))
            color_pair = max(1, min(color_pair, 7))
            stdscr.addstr(y, x, " ", curses.color_pair(color_pair))
    stdscr.refresh()


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)

    width = 80
    height = 24
    surface = WaterSurface(width, height)

    frame_count = 0

    while True:
        key = stdscr.getch()
        if key == ord("q"):
            break
        if key == ord("r"):
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            radius = random.randint(1, 5)
            strength = random.uniform(0.1, 1.0)
            drop = Raindrop(x, y, radius, strength)
            surface.add_drop(drop)
        surface.update()
        render(stdscr, surface)
        curses.napms(100)

        # Save to PNG and log every 50 frames
        if frame_count % 50 == 0:
            surface.save_to_png(f"/tmp/water_surface_{frame_count}.png")
            surface.log_grid()

        frame_count += 1


if __name__ == "__main__":
    curses.wrapper(main)
