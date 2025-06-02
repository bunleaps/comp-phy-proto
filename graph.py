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

        self.scrolling = True # set to false for testing

        self.num_balls = num_balls
        self.lines = []
        for i in range(num_balls):
            line, = self.ax.plot([], [], color="black")
            self.lines.append(line)

        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Speed")
        self.ax.legend(loc="upper right")

        # Fix y-axis to [0, 30]
        self.ax.set_ylim(0, 10)

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
        if self.scrolling:
            if t <= self.window_width:
                left, right = 0, self.window_width
            else:
                left, right = t - self.window_width, t
        else:
            left, right = 0, self.window_width

        self.ax.set_xlim(left, right)

        # 5) Redraw in interactive mode
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

class Graph2:
    def __init__(self, num_balls: int, window_width: float = 10, estimated_fps: int = 60):
        """
        num_balls:      how many separate kinetic energy lines to plot
        window_width:   how many seconds to show on the x‐axis at once
        estimated_fps:  approximate frames per second (used to size internal deques)
        """
        plt.ion()
        self.fig, self.ax = plt.subplots()

        self.scrolling = True 

        self.num_balls = num_balls
        self.lines = []
        for i in range(num_balls):
            line, = self.ax.plot([], [], color="black") # Default color, will be changed
            self.lines.append(line)

        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Kinetic Energy (J)")
        # self.ax.set_ylim(0, 10) # KE can vary, auto-scaling might be better initially
        self.ax.legend(loc="upper right")


        self.window_width = window_width
        max_points = int(estimated_fps * window_width * 2) # Increased buffer for smoother scrolling

        # Shared deque for time
        self.frames = deque(maxlen=max_points)
        # One deque of kinetic energies per ball
        self.kinetic_energies = [deque(maxlen=max_points) for _ in range(num_balls)]

        self._colors_configured = False

    def configure_colors(self, balls: list) -> None:
        """
        This method is called by update once to match line and label colors with the respective ball colors.
        balls: List of Ball instances
        """
        if len(balls) != self.num_balls:
            # If fewer balls are provided than expected, adjust num_balls
            # This can happen if balls are pocketed and removed from the list passed to update
            # However, for simplicity, we'll assume the list of balls always matches num_balls
            # or that num_balls is the maximum number of balls that will ever be plotted.
            # A more robust solution might involve dynamically adding/removing lines,
            # but for now, we'll stick to the initial num_balls.
            print(f"Warning: Graph2 color configuration expected {self.num_balls} balls, got {len(balls)}. Plotting up to {min(self.num_balls, len(balls))}.")
            # self.num_balls = len(balls) # This would alter the loop below, might be problematic if lines aren't adjusted.

        for i in range(min(self.num_balls, len(balls))): # Iterate up to the number of available balls or lines
            ball = balls[i]
            # Convert RGB to Matplotlib color
            if ball.color == (255, 255, 255): # WHITE
                mpl_color = (0, 0, 0) # Plot white balls as black
            else:
                r, g, b = ball.color
                mpl_color = (r / 255.0, g / 255.0, b / 255.0)
            
            if i < len(self.lines):
                self.lines[i].set_color(mpl_color)
                label = "Cue Ball" if i == 0 else f"Ball {i+1}"
                self.lines[i].set_label(label)

        self.ax.legend(loc="upper right")
        self._colors_configured = True

    def update(self, t: float, balls: list) -> None:
        """
        t:     current time in seconds
        balls: list of Ball instances
        """
        if not self._colors_configured and balls: # Ensure balls list is not empty
            self.configure_colors(balls)

        self.frames.append(t)

        for i in range(self.num_balls):
            if i < len(balls):
                ball = balls[i]
                # KE = 0.5 * m * v^2
                # ball.speed is math.hypot(self.vel[0],self.vel[1])
                # ball.mass is available
                if not ball.pocketed:
                    ke = 0.5 * ball.mass * (ball.speed ** 2)
                else:
                    ke = 0.0 # Pocketed balls have no KE for plotting
                self.kinetic_energies[i].append(ke)
            else:
                # If fewer balls than num_balls (e.g., pocketed and removed from main list)
                # append a zero or NaN, or handle appropriately.
                # For now, assume the 'balls' list might be shorter if some are pocketed
                # and we only update lines for existing balls.
                # If a line exists but no ball, its data won't update.
                # A better way might be to pass placeholder data or ensure 'balls' always has 'num_balls' items (even if 'None')
                self.kinetic_energies[i].append(0.0) # Append 0 if ball is missing/pocketed


        for i, line in enumerate(self.lines):
            line.set_data(self.frames, self.kinetic_energies[i])

        if self.scrolling:
            if t <= self.window_width:
                left, right = 0, self.window_width
            else:
                left, right = t - self.window_width, t
        else: # Not scrolling, fixed window from 0
            left, right = 0, self.window_width
            if self.frames: # Ensure frames is not empty
                 right = max(self.window_width, self.frames[-1] if self.frames else self.window_width)


        self.ax.set_xlim(left, right)
        
        # Auto-adjust y-axis for KE as it can vary more than speed
        self.ax.relim()
        self.ax.autoscale_view(True, True, True) # Autoscale y-axis based on current data

        # 5) Redraw in interactive mode
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
