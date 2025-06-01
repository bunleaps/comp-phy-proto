import matplotlib.pyplot as plt
from collections import deque

class Graph:
    def __init__(self, window_width=10, estimated_fps=60):
        """
        window_width: how many seconds to show on the x-axis at once
        estimated_fps: approximate frames per second
        """
        plt.ion()
        self.fig, self.ax = plt.subplots()
        self.line_v, = self.ax.plot([], [], label="Speed")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Value")
        self.ax.legend()

        self.ax.set_ylim(0, 30)

        self.window_width = window_width

        # Keep enough points so we never drop data that should still be visible.
        max_points = int(estimated_fps * window_width * 2)
        self.frames    = deque(maxlen=max_points)
        self.speeds    = deque(maxlen=max_points)

    def update(self, t:float, speed:float, momentum=10, energy=50) -> None:
        """
        t: current time in seconds (float)
        """
        # 1) Append new data
        self.frames.append(t)
        self.speeds.append(speed)

        # 2) Update line data
        self.line_v.set_data(self.frames, self.speeds)

        # 3) Set x-limits so that, until t >= window_width, the range is [0, window_width].
        #    Once t > window_width, scroll: [t - window_width, t].
        if t <= self.window_width:
            left, right = 0, self.window_width
        else:
            left, right = t - self.window_width, t

        self.ax.set_xlim(left, right)

        # 4) Force redraw
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

        return