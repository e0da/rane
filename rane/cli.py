import numpy as np
import pygame


def create_grid(size):
    """Create a grid with values ranging from -1 to 1."""
    return np.linspace(-1, 1, size**2).reshape(size, size)


def map_value_to_color(value):
    """
    Map a value from -1 to 1 to a color from violet to red.
    -1 -> violet (RGB: 148, 0, 211)
     0 -> blue (RGB: 0, 0, 255)
     1 -> red (RGB: 255, 0, 0)
    """
    violet = np.array([148, 0, 211])
    blue = np.array([0, 0, 255])
    red = np.array([255, 0, 0])

    if value < 0:
        # Interpolate between violet and blue
        return tuple((violet + (blue - violet) * (value + 1)).astype(int))
    else:
        # Interpolate between blue and red
        return tuple((blue + (red - blue) * value).astype(int))


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
