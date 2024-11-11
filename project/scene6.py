from manim import *
import numpy as np
from datetime import datetime, timedelta

class AdvancedChaosSystem(Scene):
    def __init__(self):
        super().__init__()
        # Define standard spacing and layout parameters
        self.STANDARD_PADDING = 0.5
        self.SECTION_PADDING = 1.0
        self.TEXT_SCALE = 0.7
        self.ANIMATION_SCALE = 0.6

    def get_lorenz_points(self, xyz, *, sigma=10, rho=28, beta=8/3, dt=0.01, num_points=2000):
        points = []
        derivatives = []
        x, y, z = xyz
        for _ in range(num_points):
            dx = sigma * (y - x)
            dy = x * (rho - z) - y
            dz = x * y - beta * z
            derivatives.append([dx, dy, dz])
            x += dx * dt
            y += dy * dt
            z += dz * dt
            points.append([x, y, z])
        return points, derivatives

    def create_layout_grid(self):
        # Create a 3x3 grid for organized layout
        return Rectangle().get_grid(3, 3, height=config.frame_height - 1, width=config.frame_width - 1)

    def create_enhanced_derivation(self):
        # More detailed mathematical derivation with proper spacing
        derivation = VGroup(
            Text("Mathematical Foundation", font_size=32, color=BLUE),
            MathTex(r"\text{1. Navier-Stokes Equations}"),
            MathTex(r"\frac{\partial \mathbf{v}}{\partial t} + (\mathbf{v} \cdot \nabla)\mathbf{v} = -\frac{1}{\rho}\nabla p + \nu\nabla^2\mathbf{v}"),
            MathTex(r"\text{2. Temperature Diffusion}"),
            MathTex(r"\frac{\partial T}{\partial t} + (\mathbf{v} \cdot \nabla)T = \kappa\nabla^2T"),
            MathTex(r"\text{3. Lorenz Simplification}"),
            MathTex(r"\dot{x} = \sigma(y-x)"),
            MathTex(r"\dot{y} = x(\rho-z)-y"),
            MathTex(r"\dot{z} = xy-\beta z")
        ).arrange(DOWN, buff=0.3)
        
        # Add explanation boxes
        explanations = VGroup(
            Text("σ: Prandtl number", font_size=20),
            Text("ρ: Rayleigh number", font_size=20),
            Text("β: Geometric factor", font_size=20)
        ).arrange(DOWN, buff=0.2)
        
        return VGroup(derivation, explanations).arrange(RIGHT, buff=1)

    def create_weather_data_visualization(self):
        # Create mock weather data visualization
        weather_data = VGroup(
            Text("Weather Prediction Accuracy", font_size=28, color=BLUE),
            self.create_accuracy_graph(),
            self.create_uncertainty_cone()
        ).arrange(DOWN, buff=0.5)
        return weather_data

    def create_accuracy_graph(self):
        # Create a graph showing prediction accuracy over time
        axes = Axes(
            x_range=[0, 14, 2],
            y_range=[0, 100, 20],
            axis_config={"include_tip": True},
            x_axis_config={"label": "Days"},
            y_axis_config={"label": "Accuracy (%)"}
        )
        
        accuracy_curve = axes.plot(
            lambda x: 100 * np.exp(-0.15 * x),
            color=BLUE
        )
        
        return VGroup(axes, accuracy_curve)

    def create_uncertainty_cone(self):
        # Create an uncertainty cone visualization
        start_point = np.array([-3, 0, 0])
        end_points = [np.array([3, y, 0]) for y in np.linspace(-2, 2, 10)]
        
        lines = VGroup(*[
            Line(start_point, end_point, stroke_opacity=0.5)
            for end_point in end_points
        ])
        
        cone = Polygon(
            start_point,
            end_points[0],
            end_points[-1],
            fill_opacity=0.2,
            fill_color=BLUE,
            stroke_opacity=0
        )
        
        return VGroup(cone, lines)

    def create_applications_section(self):
        # Create organized applications section
        applications = VGroup(
            Text("Applications of Chaos Theory", font_size=32, color=GREEN),
            VGroup(
                self.create_application_box("Weather", "• Global forecasting\n• Climate modeling"),
                self.create_application_box("Finance", "• Market prediction\n• Risk analysis"),
                self.create_application_box("Biology", "• Population dynamics\n• Neural activity"),
                self.create_application_box("Engineering", "• Control systems\n• Robotics")
            ).arrange(RIGHT, buff=0.5)
        ).arrange(DOWN, buff=0.5)
        return applications

    def create_application_box(self, title, content):
        box = VGroup(
            Text(title, font_size=24),
            Text(content, font_size=20)
        ).arrange(DOWN, buff=0.2)
        return SurroundingRectangle(box, buff=0.2, color=GREEN_A)

    def create_interactive_demonstration(self):
        # Create interactive butterfly effect demonstration
        demo = VGroup(
            Text("Interactive Demonstration", font_size=32, color=YELLOW),
            self.create_butterfly_effect_visual(),
            self.create_sensitivity_controls()
        ).arrange(DOWN, buff=0.5)
        return demo

    def create_butterfly_effect_visual(self):
        # Create butterfly effect visualization
        initial_points = [np.array([0, 0, 0]), np.array([0.01, 0, 0])]
        paths = VGroup(*[
            self.create_trajectory(point)
            for point in initial_points
        ])
        return paths

    def create_trajectory(self, start_point):
        points, _ = self.get_lorenz_points(start_point)
        path = VMobject()
        path.set_points_smoothly([np.array(p) for p in points])
        return path

    def create_sensitivity_controls(self):
        # Create interactive controls visualization
        controls = VGroup(
            Text("Initial Condition Sensitivity", font_size=24),
            Arrow(LEFT * 2, RIGHT * 2),
            Text("Δx = 0.01", font_size=20)
        ).arrange(DOWN, buff=0.3)
        return controls

    def construct(self):
        # Create main layout grid
        grid = self.create_layout_grid()
        
        # Title sequence
        title = Text("Advanced Chaos Theory", font_size=48)
        subtitle = Text("Mathematics, Weather, and Applications", font_size=36)
        title_group = VGroup(title, subtitle).arrange(DOWN)
        
        self.play(Write(title_group))
        self.wait()
        self.play(title_group.animate.scale(0.6).to_edge(UP))

        # Mathematical section
        math_section = self.create_enhanced_derivation()
        math_section.scale(0.8).move_to(grid[0])
        
        self.play(Write(math_section), run_time=3)
        self.wait()

        # Weather data visualization
        weather_section = self.create_weather_data_visualization()
        weather_section.scale(0.8).move_to(grid[4])
        
        self.play(Create(weather_section), run_time=3)
        self.wait()

        # Applications section
        applications = self.create_applications_section()
        applications.scale(0.8).move_to(grid[8])
        
        self.play(Create(applications), run_time=2)
        self.wait()

        # Interactive demonstration
        demo = self.create_interactive_demonstration()
        demo.scale(0.8).move_to(grid[5])
        
        self.play(Create(demo), run_time=2)
        
        # Create enhanced 3D visualization
        self.play(
            Rotate(
                demo,
                angle=PI/2,
                axis=UP,
                run_time=3,
                rate_func=smooth
            )
        )
        
        # Add final summary
        summary = VGroup(
            Text("Key Insights:", font_size=32, color=GOLD),
            Text("• Deterministic chaos exists in many systems", font_size=24),
            Text("• Small changes can have large effects", font_size=24),
            Text("• Prediction accuracy decreases over time", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT)
        summary.scale(0.8).to_edge(DOWN)
        
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
        scene = AdvancedChaosSystem()
        scene.render()