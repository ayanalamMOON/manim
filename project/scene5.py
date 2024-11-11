from manim import *
import numpy as np
from datetime import datetime, timedelta

class ComprehensiveChaosSystem(Scene):
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
        return points, [dx, dy, dz]

    def create_derivation(self):
        derivation = VGroup(
            MathTex(r"\text{1. Conservation of momentum:}"),
            MathTex(r"\frac{\partial \mathbf{v}}{\partial t} + (\mathbf{v} \cdot \nabla)\mathbf{v} = -\frac{1}{\rho}\nabla p + \nu\nabla^2\mathbf{v} + \mathbf{g}"),
            MathTex(r"\text{2. Simplified to:}"),
            MathTex(r"\frac{dx}{dt} = \sigma(y-x)"),
            MathTex(r"\text{Where } \sigma \text{ is the Prandtl number:}"),
            MathTex(r"\sigma = \frac{\text{momentum diffusivity}}{\text{thermal diffusivity}}")
        ).arrange(DOWN, buff=0.3)
        return derivation.scale(0.7)

    def create_weather_example(self):
        weather = VGroup(
            Text("Weather Prediction Example:", font_size=24),
            Text("Initial Conditions:", font_size=20),
            MathTex(r"\text{Temperature: } 20°\text{C} \pm 0.1°\text{C}"),
            MathTex(r"\text{Pressure: } 1013 \text{ hPa} \pm 0.1 \text{ hPa}"),
            MathTex(r"\text{Wind: } 10 \text{ m/s} \pm 0.1 \text{ m/s}")
        ).arrange(DOWN, buff=0.2)
        return weather.scale(0.7)

    def create_timeline(self):
        events = VGroup(
            Text("1960: Lorenz discovers sensitivity while running weather simulations", font_size=20),
            Text("1963: Published 'Deterministic Nonperiodic Flow'", font_size=20),
            Text("1972: 'Butterfly Effect' term coined", font_size=20),
            Text("1963-Present: Applications in various fields", font_size=20)
        ).arrange(DOWN, buff=0.2)
        return events.scale(0.7)

    def create_applications(self):
        apps = VGroup(
            Text("Modern Applications:", font_size=24),
            Text("• Weather Forecasting", font_size=20),
            Text("• Financial Market Analysis", font_size=20),
            Text("• Population Dynamics", font_size=20),
            Text("• Neural Networks", font_size=20)
        ).arrange(DOWN, buff=0.2)
        return apps.scale(0.7)

    def construct(self):
        # Enhanced color scheme with gradients
        colors = [
            color_gradient([BLUE_E, BLUE_A, WHITE], 20),
            color_gradient([RED_E, RED_A, PINK], 20),
            color_gradient([GREEN_E, GREEN_A, WHITE], 20),
            color_gradient([PURPLE_E, PURPLE_A, PINK], 20),
            color_gradient([TEAL_E, TEAL_A, WHITE], 20)
        ]

        # Title sequence with interactive elements
        title = Text("The Mathematics of Chaos", font_size=48)
        subtitle = Text("From Weather Prediction to Modern Applications", font_size=36)
        
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))
        self.play(Write(subtitle.next_to(title, DOWN)))
        self.wait()

        # Mathematical Derivation Section
        derivation = self.create_derivation()
        derivation.to_edge(LEFT)
        
        self.play(
            subtitle.animate.scale(0.7).to_corner(UP + RIGHT),
            Write(derivation),
            run_time=3
        )
        self.wait()  # Pause for mathematical understanding

        # Weather Prediction Example
        weather = self.create_weather_example()
        weather.next_to(derivation, RIGHT, buff=1)
        
        self.play(Write(weather))
        self.wait()

        # Initialize Lorenz system with multiple starting conditions
        trajectories = []
        phase_points = []
        
        base_points = [
            [1, 1, 1],
            [1.001, 1, 1],
            [1, 1.001, 1],
            [0.999, 1, 1],
            [1, 0.999, 1]
        ]

        # Create enhanced visual trajectories
        for i, start_point in enumerate(base_points):
            points, derivatives = self.get_lorenz_points(start_point)
            scaled_points = [[p[0]/20, p[1]/20, p[2]/20 - 2] for p in points]
            
            # Create main trajectory
            path = VMobject()
            path.set_points_smoothly([np.array(p) for p in scaled_points])
            path.set_color_by_gradient(*colors[i])
            trajectories.append(path)
            
            # Add phase space point
            point = Sphere(radius=0.05).set_color(colors[i][0])
            point.move_to(path.get_start())
            phase_points.append(point)

        # Timeline and Historical Context
        timeline = self.create_timeline()
        timeline.to_edge(LEFT)
        
        self.play(
            *[FadeOut(mob) for mob in [derivation, weather]],
            Write(timeline)
        )
        self.wait()

        # Applications Section
        applications = self.create_applications()
        applications.next_to(timeline, RIGHT, buff=1)
        
        self.play(Write(applications))
        self.wait()

        # Create interactive visualization
        vis_group = VGroup()
        for i, (traj, point) in enumerate(zip(trajectories, phase_points)):
            self.play(
                Create(traj),
                Create(point),
                run_time=2,
                rate_func=smooth
            )
            vis_group.add(traj, point)

        # Add interactive elements showing sensitivity
        sensitivity_demo = VGroup(
            Arrow(LEFT * 3, RIGHT * 3, color=YELLOW),
            Text("Initial Difference: 0.001", font_size=24, color=YELLOW),
            Text("Final Difference: >>", font_size=24, color=YELLOW)
        ).arrange(DOWN)
        sensitivity_demo.next_to(vis_group, DOWN)
        
        self.play(Create(sensitivity_demo))
        self.wait()

        # Enhanced 3D rotation with path tracing
        self.play(
            Rotate(
                vis_group,
                angle=2*PI,
                axis=UP,
                run_time=6,
                rate_func=smooth
            )
        )

        # Weather prediction demonstration
        weather_pred = VGroup(
            Text("5-Day Forecast", font_size=24),
            Text("Accuracy: High", font_size=20, color=GREEN),
            Text("10-Day Forecast", font_size=24),
            Text("Accuracy: Medium", font_size=20, color=YELLOW),
            Text("15-Day Forecast", font_size=24),
            Text("Accuracy: Low", font_size=20, color=RED)
        ).arrange(DOWN)
        weather_pred.to_edge(RIGHT)

        self.play(
            Write(weather_pred),
            vis_group.animate.scale(0.7).to_edge(LEFT)
        )
        self.wait()

        # Final summary with key points
        summary = VGroup(
            Text("Key Insights:", font_size=32),
            Text("• Small changes can lead to large effects", font_size=24),
            Text("• Long-term prediction has fundamental limits", font_size=24),
            Text("• Chaos is deterministic but unpredictable", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT)
        summary.to_edge(DOWN)

        self.play(Write(summary))
        self.wait(2)

        # Elegant fade out
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        )

if __name__ == "__main__":
    with tempconfig({
        "quality": "high_quality",
        "preview": True,
        "frame_rate": 60,
        "pixel_width": 1920,
        "pixel_height": 1080,
    }):
        scene = ComprehensiveChaosSystem()
        scene.render()