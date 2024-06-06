import numpy as np
import pygame
import argparse

# Define default grid dimensions and pixel sizes
DEFAULT_WIDTH = 50
DEFAULT_HEIGHT = 50
DEFAULT_PIXEL_WIDTH = 10
DEFAULT_PIXEL_HEIGHT = 10
DEFAULT_HUE_MID = 180
DEFAULT_HUE_RANGE = 360


def create_grid(width, height):
    """Create a grid with values ranging from -1 to 1."""
    return np.linspace(-1, 1, width * height).reshape(height, width)


def map_value_to_color(value, hue_mid=DEFAULT_HUE_MID, hue_range=DEFAULT_HUE_RANGE):
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


def render_grid(
    screen,
    grid,
    pixel_width=DEFAULT_PIXEL_WIDTH,
    pixel_height=DEFAULT_PIXEL_HEIGHT,
    hue_mid=180,
):
    """Render the grid using Pygame."""
    height, width = grid.shape
    for y in range(height):
        for x in range(width):
            value = grid[y][x]
            color = map_value_to_color(value, hue_mid)
            pygame.draw.rect(
                screen,
                color,
                (x * pixel_width, y * pixel_height, pixel_width, pixel_height),
            )
    pygame.display.flip()


def _main(args: argparse.Namespace):
    width, height = map(int, args.dimensions.split("x"))
    pixel_width, pixel_height = map(int, args.pixel_dimensions.split("x"))
    grid = create_grid(width, height)

    pygame.init()
    screen = pygame.display.set_mode((width * pixel_width, height * pixel_height))
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
                x //= pixel_width
                y //= pixel_height
                if 0 <= x < width and 0 <= y < height:
                    grid[y][x] = 0 if lower else 1

        render_grid(screen, grid, pixel_width, pixel_height)

    pygame.quit()


def _parse_args():
    parser = argparse.ArgumentParser(description="Liquid Surface Visualization")
    parser.add_argument(
        "-d",
        "--dimensions",
        type=str,
        default=f"{DEFAULT_WIDTH}x{DEFAULT_HEIGHT}",
        help="Grid dimensions as WIDTHxHEIGHT, e.g. %(default)s",
    )
    parser.add_argument(
        "-p",
        "--pixel-dimensions",
        type=str,
        default=f"{DEFAULT_PIXEL_WIDTH}x{DEFAULT_PIXEL_HEIGHT}",
        help="Pixel dimensions as WIDTHxHEIGHT, e.g. %(default)s",
    )
    return parser.parse_args()


def main():
    args = _parse_args()
    _main(args)


if __name__ == "__main__":
    main()
