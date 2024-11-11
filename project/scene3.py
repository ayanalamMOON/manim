from manim import *

class ComplexRotation(Scene):
    def construct(self):
        # Create a plane for complex numbers
        plane = ComplexPlane().scale(2)
        self.play(Create(plane))
        
        # Create our main circle
        circle = Circle(radius=1, color=BLUE)
        dot = Dot(color=YELLOW)
        
        # Create path for the dot to follow
        path = ParametricFunction(
            lambda t: np.array([
                np.cos(t) + 0.5 * np.cos(3*t),
                np.sin(t) + 0.5 * np.sin(3*t),
                0
            ]),
            t_range=[0, TAU],
            color=YELLOW_A
        )
        
        # Create text labels
        title = Text("Complex Motion", font_size=42)
        title.to_edge(UP)
        
        formula = MathTex(
            "z(t) = e^{it} + \\frac{1}{2}e^{3it}",
            font_size=36
        )
        formula.next_to(title, DOWN)
        
        # Animation sequence
        self.play(
            Write(title),
            Write(formula),
            Create(circle),
            Create(dot)
        )
        
        # Create smaller circles that will rotate
        small_circles = VGroup(*[
            Circle(radius=0.2, color=BLUE_A).shift(
                np.array([np.cos(i*TAU/5), np.sin(i*TAU/5), 0])
            )
            for i in range(5)
        ])
        
        self.play(Create(small_circles))
        
        # Animate the dot following the path
        self.play(
            MoveAlongPath(dot, path),
            Rotate(small_circles, angle=TAU, about_point=ORIGIN),
            run_time=4,
            rate_func=linear
        )
        
        # Create spiral effect
        spiral = ParametricFunction(
            lambda t: np.array([
                t * np.cos(3*t),
                t * np.sin(3*t),
                0
            ]) * 0.25,
            t_range=[0, 4*TAU],
            color=RED
        )
        
        self.play(
            Create(spiral),
            small_circles.animate.fade(0.5),
            run_time=3
        )
        
        # Final flourish - everything spins
        everything = VGroup(circle, small_circles, spiral, dot)
        self.play(
            Rotate(everything, angle=-TAU/2),
            run_time=2
        )
        
        self.wait()

if __name__ == "__main__":
    with tempconfig({"quality": "medium_quality"}):
        scene = ComplexRotation()
        scene.render()