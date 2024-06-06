import numpy as np
import pygame


def create_grid(size):
    """Create a grid with values ranging from -1 to 1."""
    return np.linspace(-1, 1, size**2).reshape(size, size)


def map_value_to_color(value):
    """
    Map a value from -1 to 1 to a color using HSV color space.
    -1 -> red (Hue 0)
     0 -> green (Hue 120)
     1 -> violet (Hue 240)
    """
    hue = (value + 1) * 0.5 * 240  # Scale value to range from 0 to 240 (red to violet)
    color = pygame.Color(0)
    color.hsva = (hue, 100, 100)  # Full saturation and value (brightness)
    return color.r, color.g, color.b


def render_grid(grid, pixel_size=10):
    """Render the grid using Pygame."""
    pygame.init()
    size = len(grid)
    screen = pygame.display.set_mode((size * pixel_size, size * pixel_size))
    pygame.display.set_caption("Liquid Surface Visualization")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for y in range(size):
            for x in range(size):
                color = map_value_to_color(grid[y][x])
                pygame.draw.rect(
                    screen,
                    color,
                    (x * pixel_size, y * pixel_size, pixel_size, pixel_size),
                )

        pygame.display.flip()

    pygame.quit()


def main():
    size = 100  # Example size, you can adjust as needed
    grid = create_grid(size)
    render_grid(grid)


if __name__ == "__main__":
    main()
