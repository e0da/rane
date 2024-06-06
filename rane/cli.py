import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Define the simulation parameters
GRID_SIZE = 100
TIME_STEPS = 100
DAMPING = 0.99

# Initialize the height and velocity matrices
height = np.zeros((GRID_SIZE, GRID_SIZE))
velocity = np.zeros((GRID_SIZE, GRID_SIZE))


# Drop a water droplet at a given position
def drop_droplet(x, y, magnitude):
    height[x, y] += magnitude


# Update the simulation
def update():
    global height, velocity

    # Calculate the change in height
    height_delta = (
        np.roll(height, 1, axis=0)
        + np.roll(height, -1, axis=0)
        + np.roll(height, 1, axis=1)
        + np.roll(height, -1, axis=1)
        - 4 * height
    )

    # Update the velocity and apply damping
    velocity += height_delta
    velocity *= DAMPING

    # Update the height
    height += velocity


# Initialize the plot
fig, ax = plt.subplots()
im = ax.imshow(height, cmap="viridis", vmin=-1, vmax=1)


def animate(i):
    update()
    im.set_array(height)
    return [im]


# Create an animation
ani = animation.FuncAnimation(fig, animate, frames=TIME_STEPS, interval=50, blit=True)

# Drop a few droplets to start the simulation
drop_droplet(50, 50, 10)
drop_droplet(30, 30, 5)
drop_droplet(70, 70, 5)

# Show the animation
plt.show()
