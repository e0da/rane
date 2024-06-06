import numpy as np
import curses
import random

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
                    distance = np.sqrt(dx ** 2 + dy ** 2)
                    if distance <= drop.radius:
                        self.grid[drop.y + dy, drop.x + dx] += drop.strength * np.cos(distance)

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
    while True:
        stdscr.clear()
        for y in range(min(height, surface.height)):
            for x in range(min(width, surface.width)):
                value = surface.grid[y, x]
                color_pair = int(1 + 6 * (value - np.min(surface.grid)) / (np.max(surface.grid) - np.min(surface.grid)))
                stdscr.addstr(y, x, " ", curses.color_pair(color_pair))
        stdscr.refresh()
        surface.update()
        curses.napms(100)

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)

    width = 80
    height = 24
    surface = WaterSurface(width, height)

    while True:
        key = stdscr.getch()
        if key == ord('q'):
            break
        if key == ord('r'):
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            radius = random.randint(1, 5)
            strength = random.uniform(0.1, 1.0)
            drop = Raindrop(x, y, radius, strength)
            surface.add_drop(drop)
        render(stdscr, surface)

if __name__ == "__main__":
    curses.wrapper(main)
