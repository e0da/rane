import numpy as np
import pygame


def create_grid(size):
    """Create a grid with values ranging from -1 to 1."""
    return np.linspace(-1, 1, size**2).reshape(size, size)


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
    size = len(grid)
    for y in range(size):
        for x in range(size):
            value = grid[y][x]
            color = map_value_to_color(value, hue_mid)
            pygame.draw.rect(
                screen, color, (x * pixel_size, y * pixel_size, pixel_size, pixel_size)
            )
    pygame.display.flip()


def main():
    size = 100  # Example size, you can adjust as needed
    grid = create_grid(size)
    grid = grid.T  # Transpose to fix the orientation issue

    pygame.init()
    pixel_size = 10
    screen = pygame.display.set_mode((size * pixel_size, size * pixel_size))
    pygame.display.set_caption("Liquid Surface Visualization")

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
                if 0 <= x < size and 0 <= y < size:
                    grid[y][x] = 0 if lower else 1

        render_grid(screen, grid, pixel_size)

    pygame.quit()


if __name__ == "__main__":
    main()
