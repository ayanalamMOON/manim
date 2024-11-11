from manim import *
import numpy as np

class EnhancedPendulumAnimation(Scene):
    def construct(self):
        # Enhanced constants
        L = 3.5  # Increased length
        g = 9.81
        theta_0 = PI/3  # Larger initial angle
        omega = np.sqrt(g/L)
        damping = 0.1  # Added damping coefficient
        
        # Custom color scheme
        BACKGROUND_COLOR = "#1a1a1a"
        PENDULUM_COLOR = "#ff6b6b"  # Coral red
        TRAIL_COLOR = "#4ecdc4"     # Turquoise
        TEXT_COLOR = "#f7f7f7"      # Off-white
        
        self.camera.background_color = BACKGROUND_COLOR
        
        # Create coordinate system
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            axis_config={"color": GRAY}
        )
        self.add(axes)
        
        # Create pivot point with glow effect
        pivot = Dot(point=ORIGIN, color=WHITE)
        pivot_glow = pivot.copy().scale(1.5).set_opacity(0.3)
        self.add(pivot, pivot_glow)
        
        # Create pendulum bob and rod
        bob = Dot(point=DOWN * L, color=PENDULUM_COLOR, radius=0.15)
        bob_glow = bob.copy().scale(1.5).set_opacity(0.3)
        rod = Line(pivot.get_center(), bob.get_center(), color=GRAY)
        
        # Create path trace with gradient
        path = VMobject(stroke_width=2)
        path.set_points_as_corners([bob.get_center(), bob.get_center()])
        path.set_color(color=[TRAIL_COLOR, BLUE_A])
        
        # Energy indicators
        potential_bar = Rectangle(
            height=4, width=0.3,
            fill_opacity=0.3,
            color=GREEN
        ).to_edge(RIGHT)
        kinetic_bar = Rectangle(
            height=4, width=0.3,
            fill_opacity=0.3,
            color=RED
        ).next_to(potential_bar, LEFT, buff=0.2)
        
        energy_labels = VGroup(
            Text("PE", color=GREEN, font_size=24),
            Text("KE", color=RED, font_size=24)
        )
        energy_labels[0].next_to(potential_bar, UP)
        energy_labels[1].next_to(kinetic_bar, UP)
        
        # Add everything to scene
        self.add(rod, bob, bob_glow, path, potential_bar, kinetic_bar, energy_labels)
        
        # Variables for phase space
        phase_point = Dot(color=YELLOW)
        phase_trail = VMobject(stroke_width=2, color=YELLOW)
        phase_trail.set_points_as_corners([ORIGIN, ORIGIN])
        self.add(phase_point, phase_trail)

        # Initialize time
        self.time = 0

        # Animation updater function
        def update_pendulum(dt):
            self.time += dt
            t = self.time
            
            # Damped oscillation
            theta = theta_0 * np.exp(-damping * t) * np.cos(omega * t)
            theta_dot = theta_0 * np.exp(-damping * t) * (-damping * np.cos(omega * t) - omega * np.sin(omega * t))
            
            x = L * np.sin(theta)
            y = -L * np.cos(theta)
            
            # Update bob and rod
            new_bob_pos = np.array([x, y, 0])
            bob.move_to(new_bob_pos)
            bob_glow.move_to(new_bob_pos)
            rod.put_start_and_end_on(pivot.get_center(), bob.get_center())
            
            # Update path with gradient
            path.add_points_as_corners([bob.get_center()])
            if len(path.points) > 150:
                path.points = path.points[-150:]
            
            # Update energy bars
            PE = (1 - np.cos(theta)) * 2  # Normalized potential energy
            KE = (theta_dot/omega)**2 * 2  # Normalized kinetic energy
            potential_bar.stretch_to_fit_height(PE, about_edge=DOWN)
            kinetic_bar.stretch_to_fit_height(KE, about_edge=DOWN)
            
            # Update phase space point
            phase_x = theta * 2  # Scale for visibility
            phase_y = theta_dot
            phase_point.move_to(np.array([phase_x + 5, phase_y, 0]))  # Offset to the right
            phase_trail.add_points_as_corners([phase_point.get_center()])
            if len(phase_trail.points) > 150:
                phase_trail.points = phase_trail.points[-150:]
        
        # Add updater to scene
        self.on_frame_end_callback = update_pendulum
        
        # Add educational elements
        title = Text("Damped Harmonic Oscillator", font_size=36, color=TEXT_COLOR)
        title.to_edge(UP)
        
        equation = MathTex(
            r"\theta(t) = \theta_0 e^{-\gamma t} \cos(\omega t)",
            color=TEXT_COLOR
        )
        equation.next_to(title, DOWN)
        
        parameters = VGroup(
            Text("Parameters:", font_size=24, color=TEXT_COLOR),
            MathTex(r"\gamma = " + str(damping), color=TEXT_COLOR),
            MathTex(r"\omega = \sqrt{\frac{g}{L}} = " + f"{omega:.2f}", color=TEXT_COLOR),
            MathTex(r"\theta_0 = " + f"{theta_0:.2f}", color=TEXT_COLOR)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(LEFT).shift(UP)
        
        # Animate educational elements
        self.play(
            Write(title),
            Write(equation),
            Write(parameters)
        )
        self.wait(10)