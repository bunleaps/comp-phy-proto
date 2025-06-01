# graph.py

import matplotlib.pyplot as plt
from collections import deque
import numpy as np  # for norm if needed

class Graph:
    def __init__(self, num_balls: int, window_width: float = 10, estimated_fps: int = 60):
        """
        num_balls:      how many separate speed‐lines to plot
        window_width:   how many seconds to show on the x‐axis at once
        estimated_fps:  approximate frames per second (used to size internal deques)
        """
        plt.ion()
        self.fig, self.ax = plt.subplots()

        self.num_balls = num_balls
        self.lines = []
        for i in range(num_balls):
            line, = self.ax.plot([], [], color="black")
            self.lines.append(line)

        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Speed")
        self.ax.legend(loc="upper right")

        # Fix y-axis to [0, 30]
        self.ax.set_ylim(0, 30)

        self.window_width = window_width
        max_points = int(estimated_fps * window_width * 2)

        # Shared deque for time
        self.frames = deque(maxlen=max_points)
        # One deque of speeds per ball
        self.speeds = [deque(maxlen=max_points) for _ in range(num_balls)]

        # Will be set once we know actual Ball.color values
        self._colors_configured = False

    def configure_colors(self, balls: list) -> None:
        """
        This method is called by update once to match line and label colors with the respective ball colors

        balls: List of Ball instances
        """
        if len(balls) != self.num_balls:
            raise ValueError(f"Expected {self.num_balls} balls, got {len(balls)}.")

        for i, ball in enumerate(balls):
            # Convert RGB to Matplotlib color
            if ball.color == (255, 255, 255):
                mpl_color = (0, 0, 0)
            else:
                r, g, b = ball.color
                mpl_color = (r / 255.0, g / 255.0, b / 255.0)

            self.lines[i].set_color(mpl_color)

            # Label "Ball 1" → "Cue Ball"
            label = "Cue Ball" if i == 0 else f"Ball {i+1}"
            self.lines[i].set_label(label)

        self.ax.legend(loc="upper right")  # <-- Important
        self._colors_configured = True


    def update(self, t: float, balls: list) -> None:
        """
        t:     current time in seconds
        balls: list of Ball instances
        """
        # If colors haven’t been configured yet, do it now:
        if not self._colors_configured:
            self.configure_colors(balls)

        # 1) Append the current time to the shared deque
        self.frames.append(t)

        # 2) For each ball, compute its speed and append
        for i, ball in enumerate(balls):
            speed = getattr(ball, "speed", None)
            if speed is None:
                speed = np.linalg.norm(ball.vel)
            self.speeds[i].append(speed)

        # 3) Update each Line2D with its new (x, y) data
        for i, line in enumerate(self.lines):
            line.set_data(self.frames, self.speeds[i])

        # 4) Scroll the x-axis window to [t - window_width, t], clamped at zero
        if t <= self.window_width:
            left, right = 0, self.window_width
        else:
            left, right = t - self.window_width, t
        self.ax.set_xlim(left, right)

        # 5) Redraw in interactive mode
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
