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
            "l": PURPLE,   # Planck Length
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
        self.play(FadeOut(spacetime_visual), run_time=1.5)
        self.stop_ambient_camera_rotation()
        self.play(new_premise.animate.move_to(ORIGIN))
        self.wait(1)


class WhatIsEntropy(Scene):
    def glow_effect(self, mobject, color=TEAL, layers=5, radius=0.08, opacity_step=0.15):
        glows = VGroup()
        for i in range(layers):
            glow = mobject.copy()
            glow.set_color(color)
            glow.set_opacity(opacity_step * (1 - i / layers))
            glow.scale(1 + radius * (i + 1))
            glows.add(glow)
        return glows

    def construct(self):
        colors = {
            "S": RED,
            "k_B": BLUE,
            "A": GREEN,
            "l": PURPLE,
            r"\Omega": ORANGE,
        }

        # STEP 1: Add title and formula
        entropy_title = Text("Black Hole Entropy", font_size=46, t2c={"Entropy": TEAL})
        entr = MathTex(r"S=", substrings_to_isolate="S")
        bh_formula = MathTex("k_B", "A", r"\over", "4", r"l", r"^2", font_size=46)
        entr.set_color_by_tex("S", colors["S"])
        bh_formula.set_color_by_tex("k_B", colors["k_B"])
        bh_formula.set_color_by_tex("A", colors["A"])
        bh_formula.set_color_by_tex("l", colors["l"])
        bh_formula.next_to(entr, RIGHT)
        bh_formula_entr = VGroup(entr, bh_formula)
        title_group = VGroup(entropy_title, bh_formula_entr).arrange(DOWN, buff=0.6)
        self.add(title_group)
        self.wait(1)

        # STEP 2: Isolate and move "Entropy" to center
        entropy_only = title_group[0][-7:]
        self.play(
            FadeOut(title_group[1], *title_group[0][:-7]),
            entropy_only.animate.move_to(ORIGIN)
        )

        # STEP 3: Glow fade in
        glow = self.glow_effect(entropy_only, color=TEAL)
        self.play(LaggedStart(*[FadeIn(layer) for layer in glow], lag_ratio=0.1))
        self.wait(0.6)

        # STEP 4: Glow fade out
        self.play(LaggedStart(*[FadeOut(layer) for layer in glow], lag_ratio=0.05))

        # STEP 5: Move Entropy to top
        self.play(entropy_only.animate.to_edge(UP))
        self.wait(1)

        # STEP 5: Show the coin microstates as a table
        headers = ["Penny", "Nickel", "Dime"]
        rows = [
            ["H", "H", "H"],
            ["H", "H", "T"],
            ["H", "T", "H"],
            ["T", "H", "H"],
            ["H", "T", "T"],
            ["T", "H", "T"],
            ["T", "T", "H"],
            ["T", "T", "T"],
        ]

        table = VGroup()
        header_row = VGroup(*[Text(h, font_size=30).set_color(YELLOW) for h in headers]).arrange(RIGHT, buff=0.8)
        table.add(header_row)

        for r in rows:
            # Create Text objects with color based on content
            colored_cells = []
            for cell in r:
                if cell == "H":
                    colored_cells.append(Text(cell, font_size=30).set_color(BLUE))
                elif cell == "T":
                    colored_cells.append(Text(cell, font_size=30).set_color(RED))
                else:
                    colored_cells.append(Text(cell, font_size=30))
            row = VGroup(*colored_cells).arrange(RIGHT, buff=1.5)
            table.add(row)
        table.arrange(DOWN, buff=0.4)
        table.move_to(ORIGIN)

        self.play(FadeOut(entropy_only), run_time=1)
        self.play(
            LaggedStart(*[FadeIn(mob) for mob in table], lag_ratio=0.05),
            run_time=2
        )

        self.wait(0.7)

        # STEP 6: Move table to the left
        self.play(table.animate.to_edge(LEFT, buff=1), run_time=1.5)
        self.wait(0.5)

        # STEP 7: Show multiplicities on the right
        getting_eqs = VGroup(
            MathTex(r"\text{getting }", "3", r"\text{ heads}", r"=1", r"\text{ way}"),
            MathTex(r"\text{getting }", "2", r"\text{ heads}", r"=3", r"\text{ ways}"),
            MathTex(r"\text{getting }", "1", r"\text{ heads}", r"=3", r"\text{ ways}"),
            MathTex(r"\text{getting }", "0", r"\text{ heads}", r"=1", r"\text{ way}")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).to_edge(RIGHT, buff=2)

        omega_eqs = VGroup(
            MathTex(r"\Omega", r"(3\text{ heads}) = 1"),
            MathTex(r"\Omega(2\text{ heads}) = 3"),
            MathTex(r"\Omega(1\text{ heads})  = 3"),
            MathTex(r"\Omega(0\text{ heads}) = 1"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).to_edge(RIGHT, buff=3)

        self.play(LaggedStartMap(FadeIn, getting_eqs, lag_ratio=0.3), run_time=3)
        self.wait(2)
        self.play(
            LaggedStart(*[
                FadeOut(getting_eq, shift=LEFT) for getting_eq in getting_eqs
            ], lag_ratio=0.2),
            LaggedStart(*[
                FadeIn(omega_eq, shift=RIGHT) for omega_eq in omega_eqs
            ], lag_ratio=0.2),
            run_time=3
        )

        self.wait(2)


        # Draw rectangle and write "Multiplicity"
        rect = SurroundingRectangle(omega_eqs[0][0], color=YELLOW, buff=0.1)
        multiplicity_label = Text("Multiplicity", font_size=30).next_to(rect, UP)

        self.play(Create(rect), FadeIn(multiplicity_label))
        self.wait(2)

        # Clear the rectangle and label
        self.play(FadeOut(rect), FadeOut(multiplicity_label))
        self.wait(1)

        # --- Step 1: Highlight one microstate row ---
        microstate_rect = SurroundingRectangle(table[1], color=ORANGE, buff=0.15)
        microstate_label = Text("Microstate", font_size=28, color=ORANGE).next_to(microstate_rect, RIGHT)

        self.play(Create(microstate_rect), FadeIn(microstate_label))
        self.wait(1)

        # --- Step 2: Flash rectangles quickly around other microstate rows ---
        for i in range(2, len(table)):
            rect = SurroundingRectangle(table[i], color=ORANGE, buff=0.15)
            self.play(FadeIn(rect), run_time=0.4)
            self.play(FadeOut(rect), run_time=0.4)

        self.wait(0.5)

        self.play(FadeOut(microstate_label), FadeOut(microstate_rect))

        # --- Step 3: Add vertical "Microstates" label on left of table ---
        microstates_vertical = Text("Microstates", font_size=36, color=ORANGE).rotate(90)
        microstates_vertical.next_to(table, LEFT, buff=1)
        self.play(FadeIn(microstates_vertical))
        self.wait(1)

        # --- Step 4: Highlight one macrostate row (omega_eqs) ---
        macrostate_rect = SurroundingRectangle(omega_eqs[0], color=PURPLE, buff=0.15)
        macrostate_label = Text("Macrostate", font_size=28, color=PURPLE).next_to(macrostate_rect, RIGHT)

        self.play(Create(macrostate_rect), FadeIn(macrostate_label))
        self.wait(1)

        # --- Step 5: Flash rectangles around other macrostates quickly ---
        for i in range(1, len(omega_eqs)):
            rect = SurroundingRectangle(omega_eqs[i], color=PURPLE, buff=0.15)
            self.play(FadeIn(rect), run_time=0.4)
            self.play(FadeOut(rect), run_time=0.4)

        self.wait(0.5)

        self.play(FadeOut(macrostate_label), FadeOut(macrostate_rect))

        # --- Step 6: Add vertical "Macrostates" label on right of omega_eqs ---
        macrostates_vertical = Text("Macrostates", font_size=30, color=PURPLE).rotate(PI/2)
        macrostates_vertical.next_to(omega_eqs, LEFT, buff=0.5)

        microstates_vertical = Text("Microstates", font_size=30, color=ORANGE).rotate(PI/2)
        microstates_vertical.next_to(table, LEFT, buff=0.2)
        
        self.play(FadeIn(macrostates_vertical, microstates_vertical))
        self.wait(2)

        # --- STEP 8: Show explosion of microstates for larger system ---
        large_system_title = MathTex(r"\text{Now Imagine }100\text{ Coins...}", font_size=40).to_edge(UP)

        # Right side (microstates info)
        micro_expr = MathTex(r"2^{100}", font_size=44)
        micro_label = Text("microstates", font_size=28)
        micro_group = VGroup(micro_expr, micro_label).arrange(DOWN, buff=0.3).move_to(RIGHT * 3)

        # Left side (macrostates info)
        macro_expr = Tex(r"101", font_size=40)
        macro_label = Text("macrostates", font_size=28)
        macro_group = VGroup(macro_expr, macro_label).arrange(DOWN, buff=0.3).move_to(LEFT * 3)

        # Below macro_group: the range 0,1,2,...,100
        macro_mult = MathTex(r"0,\,1,\,2,\,\ldots,\,100", font_size=26).next_to(macro_group, DOWN, buff=0.3)

        # Below micro_group: something like 2 \times 2 \times ... (to indicate exponential)
        micro_range = MathTex(r"2 \times 2 \times \cdots \times 2", font_size=26).next_to(micro_group, DOWN, buff=0.3)

        # Replacement for micro_expr (approximation)
        micro_approx = MathTex(r"\approx 1.27 \times 10^{30}", font_size=44).move_to(micro_expr.get_center())

        # Animation
        self.play(FadeOut(table), FadeOut(omega_eqs), FadeOut(macrostates_vertical), FadeOut(microstates_vertical))
        self.play(Write(large_system_title))
        self.wait(0.5)

        self.play(Write(macro_group), Write(micro_group))
        self.wait(1)

        self.play(Write(macro_mult), Write(micro_range))
        self.wait(1)

        # Transform 2^100 into the approximation
        self.play(Transform(micro_expr, micro_approx))
        self.wait(1.5)



        # --- STEP 9: Show motivation for logarithm ---
        # Initial equation
        too_big = MathTex(r"S", r"\propto", r"\Omega", font_size=46).move_to(ORIGIN)
        too_big.set_color_by_tex(r"S", RED)

        # Initial appearance
        self.play(
            FadeOut(large_system_title, shift=UP),
            FadeOut(micro_group, micro_range, shift=RIGHT),
            FadeOut(macro_group, macro_mult, shift=LEFT),
            FadeIn(too_big)
        )
        self.wait(2)

        # First transformation: Omega -> log Omega
        log_form = MathTex(r"S", r"\propto", r"\log \Omega", font_size=46).move_to(ORIGIN)
        log_form.set_color_by_tex(r"S", RED)
        self.play(Transform(too_big, log_form))
        self.wait(2)

        # Second transformation: log Omega -> k_B log Omega
        final_form = MathTex(r"S", r"=", r"k_B", r"\log \Omega", font_size=46, substrings_to_isolate=["k_B"]).move_to(ORIGIN)
        final_form.set_color_by_tex(r"k_B", BLUE)
        final_form.set_color_by_tex(r"S", RED)
        self.play(Transform(too_big, final_form))
        self.wait(2)

        final_form_2 = MathTex(r"S", r"=", r"k_B", r"\log m^N", font_size=46, substrings_to_isolate=["k_B"]).move_to(ORIGIN)
        final_form_2.set_color_by_tex(r"k_B", BLUE)
        final_form_2.set_color_by_tex(r"S", RED)
        self.play(Transform(too_big, final_form_2))
        self.wait(2)

        final_form_2 = MathTex(r"S", r"=", r"k_B", r"N", font_size=46, substrings_to_isolate=["k_B"]).move_to(ORIGIN)
        final_form_2.set_color_by_tex(r"k_B", BLUE)
        final_form_2.set_color_by_tex(r"S", RED)
        self.play(Transform(too_big, final_form_2))
        self.wait(2)


class TwoDBlackHole(Scene):
    def construct(self):
        entropy_eq = MathTex(r"S", r"=", r"k_B", r"N", font_size=46, substrings_to_isolate=["k_B"]).move_to(ORIGIN)
        entropy_eq.set_color_by_tex(r"k_B", BLUE)
        entropy_eq.set_color_by_tex(r"S", RED)
        self.add(entropy_eq)
        self.wait(2)
        self.play(entropy_eq.animate.to_edge(UP))

        # STEP 2: 2D Circular Grid Setup - extend lines to frame edges
        grid = VGroup()
        max_length = config.frame_width / 2 * 1.2  # 20% padding beyond frame half-width
        num_radial = 20
        num_circular = 15  # more circles for better gradation

        # Radial lines, opacity fades with distance
        for i in range(num_radial):
            angle = i * TAU / num_radial
            direction = np.array([np.cos(angle), np.sin(angle), 0])
            end = direction * max_length
            # Opacity fades from 1 near center to ~0 at edge
            line = Line(ORIGIN, end, color=WHITE, stroke_width=1.2)
            # Use a custom updater to set opacity based on distance from origin
            # But since it's a line, just fade it overall based on length:
            # Let's set a linear opacity gradient manually (approximate)
            # Here simpler: just fixed low opacity for distant lines
            line.set_stroke(opacity=0.15)
            grid.add(line)

        # Concentric circles with fading opacity by radius
        for j in range(1, num_circular + 1):
            r = j * max_length / num_circular
            opacity = max(0.02, 0.3 * (1 - r / max_length))  # fades from 0.3 near center to 0.02 outer edge
            circle = Circle(radius=r, color=WHITE, stroke_width=1.2, stroke_opacity=opacity)
            grid.add(circle)

        grid.move_to(ORIGIN)

        # STEP 3: Black Hole Circle (with subtle glow)
        black_hole = Circle(radius=0.6, fill_color=BLACK, stroke_color=WHITE, stroke_opacity=0.15, stroke_width=1.5, fill_opacity=1)

        glow = Circle(radius=1.1, color=BLUE_E, fill_opacity=0.1, stroke_opacity=0)
        glow.set_z_index(-1)

        black_hole_group = VGroup(glow, black_hole)

        # STEP 4: Animate
        self.play(
            LaggedStartMap(Create, grid, lag_ratio=0.05),
            run_time=2.5
        )
        self.wait(0.3)
        self.play(FadeIn(black_hole_group, scale=0.95), run_time=1.2)

        # Optional: Label
        label = Text("Black Hole", font_size=28, color=GRAY).next_to(black_hole, DOWN, buff=0.25)
        self.play(FadeIn(label), run_time=0.8)
        self.wait(1.5)