import numpy as np
import pygame
import sys

DEFAULT_WIDTH = 50
DEFAULT_HEIGHT = 50


def create_grid(width, height):
    """Create a grid with values ranging from -1 to 1."""
    return np.linspace(-1, 1, width * height).reshape(height, width)


def map_value_to_color(value, hue_mid=180, hue_range=360):
    """
    Map a value from -1 to 1 to a color using HSV color space.
    -1 -> hue_mid - hue_range / 2
     0 -> hue_mid
     1 -> hue_mid + hue_range / 2
    """
    hue_min = hue_mid - hue_range / 2
    hue_max = hue_mid + hue_range / 2
    hue = (value + 1) * 0.5 * (hue_max - hue_min) + hue_min
    hue = hue % 360  # Ensure hue stays within [0, 360] range
    color = pygame.Color(0)
    color.hsva = (hue, 100, 100)  # Full saturation and value (brightness)
    return color.r, color.g, color.b


def render_grid(screen, grid, pixel_size=10, hue_mid=180):
    """Render the grid using Pygame."""
    height, width = grid.shape
    for y in range(height):
        for x in range(width):
            value = grid[y][x]
            color = map_value_to_color(value, hue_mid)
            pygame.draw.rect(
                screen, color, (x * pixel_size, y * pixel_size, pixel_size, pixel_size)
            )
    pygame.display.flip()


def _main(width, height):
    grid = create_grid(width, height)

    pygame.init()
    pixel_size = 10
    screen = pygame.display.set_mode((width * pixel_size, height * pixel_size))
    pygame.display.set_caption("rane")

    running = True
    drawing = False
    lower = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True
                lower = pygame.key.get_mods() & pygame.KMOD_SHIFT
            elif event.type == pygame.MOUSEBUTTONUP:
                drawing = False
            elif event.type == pygame.MOUSEMOTION and drawing:
                x, y = event.pos
                x //= pixel_size
                y //= pixel_size
                if 0 <= x < width and 0 <= y < height:
                    grid[y][x] = 0 if lower else 1

        render_grid(screen, grid, pixel_size)

    pygame.quit()


def main():

    if len(sys.argv) == 1:
        width = DEFAULT_WIDTH
        height = DEFAULT_HEIGHT
    elif len(sys.argv) == 2:
        width = height = int(sys.argv[1])
    elif len(sys.argv) == 3:
        width = int(sys.argv[1] or DEFAULT_WIDTH)
        height = int(sys.argv[2] or DEFAULT_HEIGHT)
    else:
        print("Usage: rane [width] [height]")
        sys.exit(1)
    _main(width, height)


if __name__ == "__main__":
    main()
