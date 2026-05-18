from matplotlib.animation import FuncAnimation

class MultiAnimator:
    def __init__(self, simulations, fig, axes):
        """The MultiAnimator is initialized with the simulation data and the Matplotlib figure/axes for display."""
        self.sims = simulations
        self.fig = fig
        self.axes = axes
        self.max_frame = 0
        self.paused = False

        self._setup()

    def _setup(self):
        """
        Set up all simulations (patches, axes) and get max frames.
        """
        for i, sim in enumerate(self.sims):
            frames = sim.display(self.fig, self.axes[i])
            self.max_frame = max(self.max_frame, frames)

    def animate_all(self, frame):
        """
        Syncs the visual position of all planetary bodies with their calculated physics history for each frame.
        """
        patching = []

        for sim in self.sims:
            sim.current_frame = frame  # keep track for pause logic

            for k, v in sim.bodies.items():
                if k in sim.patches:
                    if frame < len(v.position_history):
                        pos = v.position_history[frame]
                    else:
                        pos = v.position_history[-1 ] # Ensures the planet stays at its final position if history ends early

                    sim.patches[k].center = (pos[0], pos[1])
                    patching.append(sim.patches[k])

        return patching

    def on_key_press(self, event):
        """
        Pause/Resume ALL simulations + print orbital info.
        """
        if event.key == ' ':

            if not self.paused:
                # Pause animation
                self.anim.event_source.stop()
                self.paused = True

                print("\n------------------------------------")

                # Print orbital info for each simulation
                for sim in self.sims:
                    time_at_pause = sim.current_frame * sim.dT

                    print(f"\n--- {sim.body_type.__name__} ---")

                    for k, v in sim.bodies.items():
                        if k.lower() == "sun":
                            continue

                        last_time_index = -1
                        for i, time in enumerate(v.timelist):
                            if time <= time_at_pause:
                                last_time_index = i
                            else:
                                break

                        if last_time_index != -1:
                            finished_time = v.timelist[last_time_index]
                            period_val = v.lastperiod[last_time_index]
                            period_str = f"{period_val:.3f} EY"
                            time_str = f"{finished_time:.3f} EY"
                        else:
                            period_str = "In progress..."
                            time_str = "None yet"

                        print(f"{k.capitalize()} last orbit = {period_str} at t = {time_str}")

                print("EY: Earth Years")
                print("Press [Space] to resume...")

            else:
                # Resume animation
                self.anim.event_source.start()
                self.paused = False
                print("\n>>> Simulation Resumed\n")

    def run(self):
        """
        Start the animation.
        """
        stride = 5 #skipping frames for the simulation visualization if needed
        self.anim = FuncAnimation(
            self.fig,
            self.animate_all,
            frames= range (0, self.max_frame, 5),
            interval=15, # if want faster animation lower the intervals
            blit=True,
            repeat=False
        )

        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)

        return self.anim