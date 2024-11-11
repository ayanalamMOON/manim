from manim import *
import numpy as np

class LorenzSystem(Scene):
    def get_lorenz_points(self, xyz, *, sigma=10, rho=28, beta=8/3, dt=0.01, num_points=2000):
        points = []
        x, y, z = xyz
        for _ in range(num_points):
            dx = sigma * (y - x)
            dy = x * (rho - z) - y
            dz = x * y - beta * z
            x += dx * dt
            y += dy * dt
            z += dz * dt
            points.append([x, y, z])
        return points

    def construct(self):
        # Title and description
        title = Text("Chaos Theory", font_size=48)
        subtitle = Text("The Lorenz Attractor", font_size=36)
        subtitle.next_to(title, DOWN)
        
        # Initial setup
        self.play(Write(title), Write(subtitle))
        self.wait(1)
        self.play(
            title.animate.scale(0.6).to_edge(UP),
            subtitle.animate.scale(0.6).next_to(title, DOWN)
        )

        # Create multiple trajectories with slightly different initial conditions
        colors = [BLUE, RED, GREEN, YELLOW, PURPLE]
        trajectories = []
        
        # Starting points very close to each other
        base_point = [10, 10, 10]
        deltas = [
            [0, 0, 0],
            [0.01, 0, 0],
            [0, 0.01, 0],
            [-0.01, 0, 0],
            [0, -0.01, 0]
        ]

        # Create paths for each trajectory
        for i, delta in enumerate(deltas):
            start_point = [b + d for b, d in zip(base_point, delta)]
            points = self.get_lorenz_points(start_point)
            
            # Scale points to fit screen better
            scaled_points = [[p[0]/20, p[1]/20, p[2]/20 - 2] for p in points]
            
            path = VMobject(color=colors[i])
            path.set_points_smoothly([np.array(p) for p in scaled_points])
            trajectories.append(path)

        # Create labels for the system parameters
        params = MathTex(
            r"\sigma = 10,\quad \rho = 28,\quad \beta = \frac{8}{3}",
            font_size=32
        )
        params.to_edge(DOWN)

        # Animate each trajectory with increasing speed
        self.play(Write(params))
        
        # Create growing paths with trailing effect
        for i, trajectory in enumerate(trajectories):
            rate = 1 - i * 0.1  # Each subsequent path draws slightly faster
            self.play(
                Create(trajectory),
                run_time=4 * rate,
                rate_func=smooth
            )

        # Add labels for key features
        butterfly_label = Text("Butterfly Effect", font_size=24, color=YELLOW)
        butterfly_label.to_edge(RIGHT)
        arrow = Arrow(butterfly_label.get_left(), trajectories[0].get_center())

        self.play(
            Write(butterfly_label),
            Create(arrow)
        )

        # Create pulsing effect to highlight sensitivity
        self.play(
            *[
                trajectory.animate.set_stroke(width=5)
                for trajectory in trajectories
            ],
            run_time=1
        )
        self.play(
            *[
                trajectory.animate.set_stroke(width=2)
                for trajectory in trajectories
            ],
            run_time=1
        )

        # Final rotation to show 3D nature
        everything = Group(*trajectories, arrow, butterfly_label)
        self.play(
            Rotate(
                everything,
                angle=PI/3,
                axis=UP,
                run_time=3,
                rate_func=there_and_back
            )
        )

        # Fade out
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        )

if __name__ == "__main__":
    with tempconfig({"quality": "high_quality"}):
        scene = LorenzSystem()
        scene.render()