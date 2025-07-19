# To render this scene, run the following command in your terminal:
# manim -pql bh_scene.py PhysicalBlackHoleLattice BlackHoleEntropySketch

from manim import *
import numpy as np

class PhysicalBlackHoleLattice(ThreeDScene):
    """
    An animation of a 3D spacetime lattice being warped by a central mass.
    This version uses a warp function derived directly from the Schwarzschild
    metric, providing a more physically meaningful visualization.
    
    V4: Text is now a 2D overlay for perfect readability, fixing the perspective issue.
    """
    def construct(self):
        # 1. --- CONFIGURATION ---
        
        # Physical and Grid properties
        SCHWARZSCHILD_RADIUS = 0.75
        GRID_BOUNDS = 4.0
        GRID_STEP = 1.0
        WARP_AMPLITUDE = 1.2
        
        # Color scheme for the lattice
        INNER_COLOR = WHITE
        OUTER_COLOR = BLUE_D
        STROKE_WIDTH = 1.5

        # 2. --- SCENE SETUP ---
        self.set_camera_orientation(phi=70 * DEGREES, theta=-120 * DEGREES, zoom=0.6)
        self.camera.light_source.move_to([-10, -10, 20])

        # 3. --- CORE LOGIC: THE PHYSICAL WARP FUNCTION ---
        
        def warp_space_physical(point):
            r = np.linalg.norm(point)
            if r == 0:
                return point
            if r < SCHWARZSCHILD_RADIUS:
                return point * (SCHWARZSCHILD_RADIUS / r)

            warp_factor = 1 - np.sqrt(1 - SCHWARZSCHILD_RADIUS / r)
            displacement = WARP_AMPLITUDE * warp_factor
            new_radius = r - displacement
            new_radius = max(SCHWARZSCHILD_RADIUS, new_radius)
            
            return point * (new_radius / r)
            
        # 4. --- OBJECT CREATION ---

        black_hole = Sphere(
            radius=SCHWARZSCHILD_RADIUS, resolution=(48, 48), color=BLACK
        )

        print("Constructing physically warped lattice...")
        grid = VGroup()
        coords = np.arange(-GRID_BOUNDS, GRID_BOUNDS + GRID_STEP, GRID_STEP)
        
        def add_colored_warped_line(start, end, vgroup):
            flat_midpoint = interpolate(start, end, 0.5)
            warped_midpoint = warp_space_physical(flat_midpoint)
            distance = np.linalg.norm(warped_midpoint)
            
            alpha = min(1, distance / (GRID_BOUNDS * 1.2))
            line_color = interpolate_color(INNER_COLOR, OUTER_COLOR, alpha)
            line_opacity = 1 - (alpha**2)

            line = ParametricFunction(
                lambda t: warp_space_physical(interpolate(start, end, t)),
                t_range=[0, 1],
                color=line_color,
                stroke_width=STROKE_WIDTH,
                stroke_opacity=line_opacity
            )
            vgroup.add(line)

        # Generate lines
        for i in coords:
            for j in coords:
                add_colored_warped_line(np.array([i, j, -GRID_BOUNDS]), np.array([i, j, GRID_BOUNDS]), grid)
                add_colored_warped_line(np.array([i, -GRID_BOUNDS, j]), np.array([i, GRID_BOUNDS, j]), grid)
                add_colored_warped_line(np.array([-GRID_BOUNDS, i, j]), np.array([GRID_BOUNDS, i, j]), grid)

        print("Lattice construction complete.")
        
        # 5. --- ANIMATION SEQUENCE ---
        self.add(black_hole)
        self.play(Create(grid, lag_ratio=0.05, rate_func=smooth), run_time=6)
        self.wait(1)
        
        self.move_camera(
            phi=60 * DEGREES,
            theta=-45 * DEGREES,
            zoom=0.75,
            run_time=8,
            rate_func=smooth
        )
        self.wait(2)

        # -----------------------------------------------------------
        # --- REVEAL SECTION (UPDATED) ---
        # -----------------------------------------------------------

        # Group 3D objects to animate them together
        spacetime_visual = VGroup(black_hole, grid)

        # Start a slow, continuous ambient rotation for dramatic effect
        self.begin_ambient_camera_rotation(rate=0.04, about="phi")

        # Animate the 3D visual to the left to make space for the text
        self.play(spacetime_visual.animate.scale(0.7).to_edge(LEFT, buff=0.5), run_time=3)

        TEXT_ANCHOR_X = 4.0
        text_anchor_point = RIGHT * TEXT_ANCHOR_X

        # Define the "hard math" concepts with adjusted font sizes
        einstein_eq = MathTex(r"R_{\mu\nu} - \frac{1}{2} R g_{\mu\nu} = \frac{8\pi G}{c^4} T_{\mu\nu}", font_size=38) # Slightly smaller
        tensors = MathTex(r"g_{\mu\nu}", r"\text{ (Spacetime Tensors)}", font_size=44) # Slightly larger than Einstein
        geometry = MathTex(r"\Gamma^{\lambda}_{\mu\nu}", r"\text{ (Differential Geometry)}", font_size=44)
        
        # Position all math concepts at the calculated anchor point
        math_concepts = VGroup(einstein_eq, tensors, geometry).arrange(DOWN, buff=0.7).move_to(text_anchor_point)
        
        self.add_fixed_in_frame_mobjects(math_concepts)
        math_concepts.set_opacity(0) # Start transparent

        # Animate through the "hard math" one by one
        self.play(einstein_eq.animate.set_opacity(1), run_time=1.5); self.wait(1.5)
        self.play(einstein_eq.animate.set_opacity(0), tensors.animate.set_opacity(1), run_time=1.5); self.wait(1.5)
        self.play(tensors.animate.set_opacity(0), geometry.animate.set_opacity(1), run_time=1.5); self.wait(1.5)
        
        # --- THE BIG REVEAL ---
        
        colors = {
            "S": RED,      # Entropy
            "k_B": BLUE,   # Boltzmann Constant
            "A": GREEN,    # Area
            "l": PURPLE, # Planck Length
        }

        entropy_title = Text("Black Hole Entropy", font_size=46, t2c={"Entropy":TEAL})

        entr = MathTex(r"S=", substrings_to_isolate="S")
        bh_formula = MathTex(
            "k_B",
            "A",
            r"\over",
            "4",
            r"l",                       
            r"^2",                        
            font_size=46,
        )

        entr.set_color_by_tex(r"S", colors["S"])
        bh_formula.set_color_by_tex("k_B", colors["k_B"])
        bh_formula.set_color_by_tex("A", colors["A"])
        bh_formula.set_color_by_tex(r"l", colors["l"])
        bh_formula.next_to(entr, RIGHT)
        bh_formula_entr = VGroup(bh_formula, entr)

        new_premise = VGroup(entropy_title, bh_formula_entr).arrange(DOWN, buff=0.6)

        # Arrange the new text elements; default arrange is center-aligned.
        new_premise.move_to(text_anchor_point) # Position the whole group at the anchor

        self.add_fixed_in_frame_mobjects(new_premise)
        new_premise.set_opacity(0) # Start transparent

        # Animate the final, powerful transition
        self.play(FadeOut(geometry, shift=DOWN), new_premise.animate.set_opacity(1), run_time=2.5)

        self.wait(4)
        self.play(FadeOut(spacetime_visual), FadeOut(new_premise), run_time=1.5)
        self.stop_ambient_camera_rotation()

