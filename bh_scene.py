from manim import *
import numpy as np

class PhysicalBlackHoleLattice(ThreeDScene):
    """
    An animation of a 3D spacetime lattice being warped by a central mass.
    This version uses a warp function derived directly from the Schwarzschild
    metric, providing a more physically meaningful visualization.
    
    V4: Text is now a 2D overlay for perfect readability, fixing the perspective issue.
    
    V5 (SYNCED): Timings adjusted to match narration from transcript.
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
        
        # 5. --- ANIMATION SEQUENCE (SYNCED) ---
        self.add(black_hole)
        
        # SYNC: Corresponds to narration from 00:00:00 to 00:11,560
        # "There are places in the universe... everything we know ends."
        self.play(Create(grid, lag_ratio=0.05, rate_func=smooth), run_time=11)
        
        # SYNC: Corresponds to narration from 00:11,560 to 00:21,900
        # "For a century we have studied them... we have seen their shadows."
        self.move_camera(
            phi=60 * DEGREES,
            theta=-45 * DEGREES,
            zoom=0.75,
            run_time=10, # Changed from 8
            rate_func=smooth
        )
        
        # SYNC: Corresponds to narration from 00:21,900 to 00:34,720
        # "But we were missing... read the message written on the outside."
        # This is a long pause for narration, so we just wait.
        self.wait(12) # Changed from wait(2) to cover this long narration segment.

        # -----------------------------------------------------------
        # --- REVEAL SECTION (SYNCED) ---
        # -----------------------------------------------------------

        spacetime_visual = VGroup(black_hole, grid)
        self.begin_ambient_camera_rotation(rate=0.04, about="phi")

        # SYNC: Corresponds to narration from 00:34,720 to 00:39,280
        # "To decipher this message, you'd think you would need the heavy machinery of physics"
        self.play(spacetime_visual.animate.scale(0.7).to_edge(LEFT, buff=0.5), run_time=4.5) # Changed from 3

        TEXT_ANCHOR_X = 4.0
        text_anchor_point = RIGHT * TEXT_ANCHOR_X

        einstein_eq = MathTex(r"R_{\mu\nu} - \frac{1}{2} R g_{\mu\nu} = \frac{8\pi G}{c^4} T_{\mu\nu}", font_size=38)
        tensors = MathTex(r"g_{\mu\nu}", r"\text{ (Spacetime Tensors)}", font_size=44)
        geometry = MathTex(r"\Gamma^{\lambda}_{\mu\nu}", r"\text{ (Differential Geometry)}", font_size=44)
        
        math_concepts = VGroup(einstein_eq, tensors, geometry).arrange(DOWN, buff=0.7).move_to(text_anchor_point)
        
        self.add_fixed_in_frame_mobjects(math_concepts)
        math_concepts.set_opacity(0)

        # SYNC: Corresponds to narration from 00:39,280 to 00:42,260 (approx)
        # "...Einstein's general relativity..."
        self.play(einstein_eq.animate.set_opacity(1), run_time=1.5); self.wait(1.5)
        
        # SYNC: Corresponds to narration from 00:42,260 to 00:45,240
        # "...the mind-bending math of spacetime tensors..."
        self.play(einstein_eq.animate.set_opacity(0), tensors.animate.set_opacity(1), run_time=1.5); self.wait(1.5)
        
        # SYNC: Corresponds to narration from 00:45,240 to 00:47,160
        # "...and differential geometry."
        self.play(tensors.animate.set_opacity(0), geometry.animate.set_opacity(1), run_time=1.5); self.wait(0.5) # Shortened wait
        
        # --- THE BIG REVEAL (SYNCED) ---
        
        colors = {"S": RED, "k_B": BLUE, "A": GREEN, "l": PURPLE}
        entropy_title = Text("Black Hole Entropy", font_size=46, t2c={"Entropy":TEAL})
        entr = MathTex(r"S=", substrings_to_isolate="S")
        bh_formula = MathTex("k_B", "A", r"\over", "4", r"l", r"^2", font_size=46)
        entr.set_color_by_tex(r"S", colors["S"])
        bh_formula.set_color_by_tex("k_B", colors["k_B"])
        bh_formula.set_color_by_tex("A", colors["A"])
        bh_formula.set_color_by_tex(r"l", colors["l"])
        bh_formula.next_to(entr, RIGHT)
        bh_formula_entr = VGroup(bh_formula, entr)
        new_premise = VGroup(entropy_title, bh_formula_entr).arrange(DOWN, buff=0.6)
        new_premise.move_to(text_anchor_point)

        self.add_fixed_in_frame_mobjects(new_premise)
        new_premise.set_opacity(0)

        # SYNC: Corresponds to narration from 00:47,160 to 00:52,560
        # "But what if I told you that we could understand one of the deepest truths..."
        self.play(FadeOut(geometry, shift=DOWN), new_premise.animate.set_opacity(1), run_time=5) # Changed from 2.5
        
        # SYNC: Corresponds to narration from 00:52,560 to 00:58,700
        # "...their entropy using nothing more than coin flips?"
        self.wait(6) # Changed from 4

        # SYNC: Corresponds to narration from 00:58,700 to 01:03,900
        # "But before we dive into the physics... What even is entropy?"
        # This is the transition to the next scene.
        self.play(FadeOut(spacetime_visual), run_time=1.5)
        self.stop_ambient_camera_rotation()
        self.play(new_premise.animate.move_to(ORIGIN), run_time=2) # Added explicit run_time
        self.wait(1.5) # Slightly longer wait for scene transition


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
        self.wait(6)

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
        self.play(FadeIn(table[0]), run_time=1)
        self.wait(5)
        self.play(
            LaggedStart(*[FadeIn(mob) for mob in table[1:]], lag_ratio=0.05),
            run_time=6
        )

        self.wait(1)

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
        self.wait(17)

        # --- Step 1: Highlight one microstate row ---
        microstate_rect = SurroundingRectangle(table[1], color=ORANGE, buff=0.15)
        microstate_label = Text("Microstate", font_size=28, color=ORANGE).next_to(microstate_rect, RIGHT)

        self.play(Create(microstate_rect), FadeIn(microstate_label))
        self.wait(2)
    
        # --- Step 2: Flash rectangles quickly around other microstate rows ---
        for i in range(2, len(table)):
            rect = SurroundingRectangle(table[i], color=ORANGE, buff=0.15)
            self.play(FadeIn(rect), run_time=0.4)
            self.play(FadeOut(rect), run_time=0.4)

        self.wait(1)

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
        self.wait(2)

        # --- Step 5: Flash rectangles around other macrostates quickly ---
        for i in range(1, len(omega_eqs)):
            rect = SurroundingRectangle(omega_eqs[i], color=PURPLE, buff=0.15)
            self.play(FadeIn(rect), run_time=0.4)
            self.play(FadeOut(rect), run_time=0.4)

        self.wait(1)

        self.play(FadeOut(macrostate_label), FadeOut(macrostate_rect))

        # --- Step 6: Add vertical "Macrostates" label on right of omega_eqs ---
        macrostates_vertical = Text("Macrostates", font_size=30, color=PURPLE).rotate(PI/2)
        macrostates_vertical.next_to(omega_eqs, LEFT, buff=0.5)

        microstates_vertical = Text("Microstates", font_size=30, color=ORANGE).rotate(PI/2)
        microstates_vertical.next_to(table, LEFT, buff=0.2)
        
        self.play(FadeIn(macrostates_vertical, microstates_vertical))
        self.wait(21)

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
        self.wait(3)

        self.play(Write(macro_group), Write(micro_group))
        self.wait(1)

        self.play(Write(macro_mult), Write(micro_range))
        self.wait(1)

        # Transform 2^100 into the approximation
        self.play(Transform(micro_expr, micro_approx))
        self.wait(10)


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
        self.wait(15)


        # First transformation: Omega -> log Omega
        log_form = MathTex(r"S", r"\propto", r"\log \Omega", font_size=46).move_to(ORIGIN)
        log_form.set_color_by_tex(r"S", RED)
        self.play(Transform(too_big, log_form))
        self.wait(16)

        # Second transformation: log Omega -> k_B log Omega
        final_form = MathTex(r"S", r"=", r"k_B", r"\log \Omega", font_size=46, substrings_to_isolate=["k_B"]).move_to(ORIGIN)
        final_form.set_color_by_tex(r"k_B", BLUE)
        final_form.set_color_by_tex(r"S", RED)
        self.play(Transform(too_big, final_form))
        self.wait(12)

        # Highlight effect using ShowPassingFlash and SurroundingRectangle
        rect = SurroundingRectangle(final_form, color=YELLOW, buff=0.15)
        self.play(ShowPassingFlash(rect, time_width=0.6, run_time=2))

        self.wait(26) 

        final_form_2 = MathTex(r"S", r"=", r"k_B", r"\log m^N", font_size=46, substrings_to_isolate=["k_B"]).move_to(ORIGIN)
        final_form_2.set_color_by_tex(r"k_B", BLUE)
        final_form_2.set_color_by_tex(r"S", RED)
        self.play(Transform(too_big, final_form_2))
        self.wait(12)

        final_form_2 = MathTex(r"S", r"=", r"k_B", r"N \log m", font_size=46, substrings_to_isolate=["k_B"]).move_to(ORIGIN)
        final_form_2.set_color_by_tex(r"k_B", BLUE)
        final_form_2.set_color_by_tex(r"S", RED)
        fo = MathTex(r"(\text{For our purposes, we can assume }\log m = 1 )").next_to(final_form_2, DOWN, buff=0.3)
        self.play(Transform(too_big, final_form_2), FadeIn(fo))

        self.wait(2)

        final_form_2 = MathTex(r"S", r"=", r"k_B", r"N", font_size=46, substrings_to_isolate=["k_B"]).move_to(ORIGIN)
        final_form_2.set_color_by_tex(r"k_B", BLUE)
        final_form_2.set_color_by_tex(r"S", RED)
        self.play(FadeOut(fo), Transform(too_big, final_form_2))
        self.wait(20)

class TwoDBlackHole(Scene):
    def construct(self):
        # Timestamps are relative to 04:55,560
        entropy_eq = MathTex(r"S", r"=", r"k_B", r"N", font_size=46, substrings_to_isolate=["k_B"]).move_to(ORIGIN)
        entropy_eq.set_color_by_tex(r"k_B", BLUE)
        entropy_eq.set_color_by_tex(r"S", RED)
        self.add(entropy_eq)
        self.play(entropy_eq.animate.to_edge(UP), run_time=2.0) # Changed: Animation time for moving the equation up.
        self.wait(5.16) # Changed: Synced with narration [05:07,520 -> 05:11,680] "But that ignorance is exactly what entropy measures."

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
            line = Line(ORIGIN, end, color=WHITE, stroke_width=1.2)
            line.set_stroke(opacity=0.15)
            grid.add(line)

        # Concentric circles with fading opacity by radius
        for j in range(1, num_circular + 1):
            r = j * max_length / num_circular
            opacity = max(0.02, 0.3 * (1 - r / max_length))
            circle = Circle(radius=r, color=WHITE, stroke_width=1.2, stroke_opacity=opacity)
            grid.add(circle)

        grid.move_to(ORIGIN)
        r_bh = 1.7
        # STEP 3: Black Hole Circle (with subtle glow)
        black_hole = Circle(radius=r_bh, fill_color=BLACK, stroke_color=WHITE, stroke_opacity=0.15, stroke_width=1.5, fill_opacity=1)

        glow = Circle(radius=r_bh+0.6, color=BLUE_E, fill_opacity=0.1, stroke_opacity=0)
        glow.set_z_index(-1)

        # STEP 4: Animate black hole creation
        # Narration [05:11,680 -> 05:26,800] "Since a black hole can be formed..."
        self.play(
            LaggedStartMap(Create, grid, lag_ratio=0.05),
            run_time=4.0 # Changed: Adjusted for narration pace.
        )
        self.wait(1.0) # Changed: Added pause for timing.
        self.play(FadeIn(glow, black_hole, scale=0.95), run_time=3.0) # Changed: Adjusted for narration pace.

        label = Text("Black Hole", font_size=28, color=LIGHT_GREY).next_to(black_hole, DOWN, buff=0.25)
        self.play(FadeIn(label), run_time=2.0) # Changed: Adjusted for narration pace.
        self.wait(5.12) # Changed: Wait for the remainder of the 15.12s narration segment.

        # Long wait for narration about entropy properties
        self.wait(26.16) # Changed: Synced with narration [05:26,800 -> 05:52,960] "For ordinary systems... total mass."

        # Wait for narration segment before photon is introduced
        self.wait(6.12) # Changed: Synced with narration [05:52,960 -> 05:59,080] "That means the entropy..."
        
        # NOTE: The following section has been re-ordered to match the narration's logic:
        # 1. Fade out label. 2. Introduce photon. 3. Introduce Schwarzschild radius.
        
        self.play(FadeOut(label, shift=DOWN), run_time=1.5) # Changed: Fading out label to introduce photon.
        self.wait(0.5) # Changed: Added pause for timing.

        # Sine-like photon oscillating horizontally inside the black hole
        sine_amplitude = 0.2 * r_bh
        sine_length =  2 * r_bh
        sine_waves = 1

        photon_curve = ParametricFunction(
            lambda t: np.array([t * sine_length - sine_length / 2, sine_amplitude * np.sin(2 * np.pi * sine_waves * t), 0]),
            t_range=[0, 1], color=YELLOW, stroke_width=3
        )
        photon_curve.move_to(ORIGIN)

        # Create photon as narration mentions it [05:59,080 -> 06:12,680]
        self.wait(30.08) # Changed: Synced with narration [06:12,680 -> 06:34,040] "Photons have energy... the black hole itself."
        self.play(Create(photon_curve), run_time=3.0) # Changed: Create photon animation.
        self.wait(1.88) # Changed: Remainder of narration segment.
        
        # Wait while narration explains photon properties
        self.wait(10.08) # Changed: Synced with narration [06:12,680 -> 06:34,040] "Photons have energy... the black hole itself."
        
        # STEP 6: Draw Schwarzschild radius as it's introduced in the narration
        angle = PI / 4
        r_s = DashedVMobject(Circle(radius=r_bh, color=RED), num_dashes=60)
        end_point = r_bh * np.array([np.cos(angle), np.sin(angle), 0])
        radius_line = Line(start=ORIGIN, end=end_point, color=RED)
        r_s_label = MathTex(r"r_s", color=RED).next_to(radius_line.get_end(), direction=radius_line.get_unit_vector(), buff=0.2)
        r_s_label.rotate(angle)

        self.play(Create(radius_line), Create(r_s), FadeIn(r_s_label), run_time=3.0) # Changed: Create r_s visual.
        
        self.wait(14.2) # Changed: Synced with narration [06:43,240 -> 06:57,560] "The Schwarzschild radius is... uncharged black hole."
        
        r_s.set_z_index(3)
        r_s_label.set_z_index(3)
        entropy_eq.set_z_index(3)
        black_hole.set_z_index(2)
        radius_line.set_z_index(3)
        photon_curve.set_z_index(4)
        
        # Clean up the scene for the derivation part
        self.play(FadeOut(*[m for m in self.mobjects if m not in (r_s, r_s_label, entropy_eq, radius_line, black_hole, photon_curve)]), run_time=1.0) # Changed: Fade out grid, keep BH elements.
         
        # Transition to the side panel for the derivation
        bh_2d = VGroup(r_s, radius_line, r_s_label, photon_curve, black_hole)
        panel = VGroup(bh_2d, entropy_eq)

        self.play(panel.animate.to_edge(LEFT), run_time=1.5) # Changed: Animation time.
        
        # Show Newtonian Gravity and Potential Energy equations
        grav_eq = MathTex(r"F = \frac{GMm}{r^2}").move_to(0.1*RIGHT + UP*2)
        self.play(Write(grav_eq), run_time=1.5) # Changed: Animation time.
        potential_eq = MathTex(r"U = -\frac{GMm}{r}").next_to(grav_eq, DOWN, buff=0.8)
        self.play(Write(potential_eq), run_time=1.5) # Changed: Animation time.
        
        energy_group = VGroup(grav_eq, potential_eq)
        brace = Brace(energy_group, LEFT, color=YELLOW)
        self.play(FadeIn(brace), run_time=0.5) # Changed: Animation time.
        self.wait(0.36) # Changed: Remainder of narration [06:57,560 -> 07:03,800]

        # Show derivation of escape velocity
        arrow = Arrow(start=0.9*LEFT, end=0.4*RIGHT, color=YELLOW).next_to(energy_group, RIGHT, buff=0.1)
        self.play(GrowArrow(arrow), run_time=0.5) # Changed: Animation time.
        solve1 = MathTex(r"\frac{1}{2}mv_e^2", "-", r"\frac{GMm}{r}", "=", "0").next_to(arrow, RIGHT, buff=0.2)
        self.play(Write(solve1), run_time=2.0) # Changed: Animation time.
        self.wait(4.26) # Changed: Remainder of narration [07:03,800 -> 07:10,560]

        # Simplify to escape velocity formula and then to Schwarzschild radius
        solve2 = MathTex(r"v_e^2 = \frac{2GM}{r}").move_to(solve1)
        self.play(Transform(solve1, solve2), run_time=1.5) # Changed: Animation time.
        
        self.play(FadeOut(arrow, brace, energy_group, shift=LEFT), solve1.animate.shift(LEFT * 2.5), run_time=1.5) # Changed: Animation time.

        solve3 = MathTex(r"c^2 = \frac{2GM}{r}").move_to(solve1)
        self.play(Transform(solve1, solve3), run_time=1.5) # Changed: Animation time.

        solve4 = MathTex(r"r_s = \frac{2GM}{c^2}").move_to(solve1)
        self.play(Transform(solve1, solve4), run_time=2.0) # Changed: Animation time.
        self.wait(8.46) # Changed: Synced with narration [07:10,560 -> 07:25,520] explaining the formula.
    
        # Relate wavelength to the radius
        solve5 = MathTex(r"\frac{\lambda}{2} = \frac{2GM}{c^2}").move_to(solve1)
        lambda_line = DashedLine(start=bh_2d.get_left(), end=bh_2d.get_right(), color=GRAY, stroke_width=2, dash_length=0.1).move_to(bh_2d.get_center())
        lambda_label = MathTex(r"\lambda", color=WHITE).next_to(lambda_line, DOWN, buff=0.2)

        self.play(Transform(solve1, solve5), Create(lambda_line), FadeIn(lambda_label), run_time=3.0) # Changed: Animation time.
        self.wait(3.84) # Changed: Synced with narration [07:25,520 -> 07:32,360]

        self.wait(8.88) # Changed: Synced with narration [07:32,360 -> 07:41,240] explaining the deduction.

        # Photon energy formula
        energy_eq = MathTex(r"\varepsilon = \frac{hc}{\lambda}", font_size=44).next_to(solve1, DOWN, buff=0.5)
        self.play(Write(energy_eq), run_time=2.0) # Changed: Animation time.
        self.wait(9.0) # Changed: Synced with narration [07:41,240 -> 07:52,240]

        # Total energy relation
        total_energy_eq = MathTex(r"N \varepsilon = M c^2", font_size=44).next_to(energy_eq, DOWN, buff=0.6)
        self.play(Write(total_energy_eq), run_time=3.0) # Changed: Animation time.
        self.wait(13.74) # Changed: Synced with narration [07:52,240 -> 08:08,980]

        # Derive N
        N_eq = MathTex(r"N = \frac{M c^2}{\varepsilon} = \frac{M c^2 \lambda}{h c}", font_size=44).move_to(ORIGIN+2*RIGHT)
        self.play(FadeOut(energy_eq, total_energy_eq, solve1), Write(N_eq), run_time=3.0) # Changed: Animation time.
        self.wait(1.0) # Changed: Added pause for timing.

        N_sub_eq = MathTex(r"N = \frac{M c^2}{\varepsilon} = \frac{M c^2 \cdot \frac{4GM}{c^2}}{h c} = \frac{4 G M^2}{h c}", font_size=44).move_to(N_eq)
        self.play(Transform(N_eq, N_sub_eq), run_time=4.0) # Changed: Animation time.
        self.wait(4.12) # Changed: Remainder of narration [08:08,980 -> 08:21,100]

        # Substitute N into the entropy formula
        N_sub_eq_2 = MathTex(r"N = \frac{4 G M^2}{h c}", font_size=44).move_to(N_sub_eq)
        self.play(Transform(N_eq, N_sub_eq_2), run_time=1.5) # Changed: Part of a sequence.
        self.wait(3)
        self.play(entropy_eq.animate.next_to(N_sub_eq_2, UP, buff=0.5), run_time=1.5) # Changed: Part of a sequence.
        self.wait(0.64) # Changed: Synced with narration [08:21,100 -> 08:24,740] "And now we return..."
        
        bh_formula = MathTex(r"S = \frac{4 k_B G M^2}{hc}", font_size=46)
        bh_2d_new = VGroup(bh_2d, lambda_label, lambda_line) # Group elements to be faded out.

        self.play(Transform(entropy_eq, bh_formula), FadeOut(N_eq), run_time=4.0) # Changed: Synced with narration [08:24,740 -> 08:31,540] "And we substitute..."
        self.wait(3) # Changed: Remainder of narration segment.

        self.play(FadeOut(bh_2d_new), run_time=1.0) # Changed: Fade out the side panel visuals.
        self.wait(6) # Changed: Synced with narration [08:31,540 -> 08:38,920] "And that depends only..."
        
class Outro(Scene):
    def construct(self):
        # Timestamps are relative to 00:09:32,900
        # Assume bh_formula is already on screen from the previous scene
        bh_formula = MathTex(
            r"S = \frac{k_B c^3 A}{4 G \hbar}", # This is the result from the previous class
            font_size=50,
            color=YELLOW_E
        ).to_edge(UP)

        # Start of user code, synchronized
        bh_formula_M = MathTex(   
            r"S = \frac{4 k_B G M^2}{\hbar c}",
            font_size=46,
        )
        self.add(bh_formula_M)
        self.wait(3.14) # Changed: Synced with narration [09:32,900 -> 09:36,040] "But there is one final..."

        # Step 2: Display the black hole area equation
        area = MathTex(
            r"A = 4\pi r_s^2 = 4\pi \left( \frac{2GM}{c^2} \right)^2 = \frac{16\pi G^2 M^2}{c^4}",
            font_size=44
        )
        self.play(bh_formula_M.animate.to_edge(UP), run_time=1.5) # Changed: Animation timing
        area.next_to(bh_formula_M, DOWN, buff=0.8)
        self.play(Write(area), run_time=2.5) # Changed: Animation timing
        self.wait(20) # Changed: Synced with narration [09:36,040 -> 09:42,640] "Physicists have defined..."

        # Step 3: Solve for M^2
        M2 = MathTex(
            r"M^2 = \frac{A c^4}{16\pi G^2}",
            font_size=44
        )
        M2.next_to(area, DOWN, buff=0.8)
        self.play(Write(M2), run_time=2.0) # Changed: Animation timing
        self.wait(5) # Changed: Synced with narration [09:42,640 -> 09:45,480] "It's called the Planck length."

        # Step 4: Substitute M^2 back into entropy formula
        new_s = MathTex(
            r"S = \frac{4 k_B G}{\hbar c} \cdot M^2 = "
            r"\frac{4 k_B G}{\hbar c} \cdot \frac{A c^4}{16\pi G^2} = "
            r"\frac{k_B c^3 A}{4 \pi G \hbar}",
            font_size=42
        ).next_to(M2, DOWN, buff=0.5) # Changed: buff adjusted
        self.play(Write(new_s), run_time=3.5) # Changed: Animation timing
        self.wait(4.74) # Changed: Synced with narration [09:45,480 -> 09:53,720] "And if you look closely..."

        # Step 5: Final simplified entropy formula
        final_s = MathTex(
            r"S = \frac{k_B c^3 A}{4 G \hbar}",
            font_size=50,
            color=YELLOW_E
        )

        # Step 6: Fade out all except final result
        self.play(
            FadeOut(bh_formula_M,shift=UP),
            FadeOut(area,shift=UP),
            FadeOut(M2,shift=DOWN),
            Transform(new_s, final_s.move_to(new_s.get_center())) # Changed: Transform for a smoother transition
        )
        self.play(new_s.animate.center()) # Changed: Center the final formula
        self.wait(20)

        # Step 7: Introduce Planck Length and simplify
        plank_length = MathTex(r"\ell_P^2 = \frac{\hbar G}{c^3}").next_to(new_s, DOWN, buff=1.0).scale(1.2) # Changed: buff adjusted

        self.play(Write(plank_length), run_time=3.0) # Changed: Animation timing

        bh_formula_entr = MathTex(r"S = \frac{k_B A}{4 \ell_P^2}", color = YELLOW_E).scale(1.2).move_to(new_s)
        self.play(Transform(new_s, bh_formula_entr), run_time=3.0) # Changed: Animation timing
        self.play(new_s.animate.move_to(ORIGIN), FadeOut(plank_length), run_time=2.0) # Changed: Animation timing
        self.play(new_s.animate.scale(1.1), run_time=1.5) # Changed: Animation timing
        self.wait(0.74) # Changed: Synced with narration [09:53,720 -> 10:03,960] "And so we arrive..."
        
        self.wait(55.16) # Changed: Synced with narration [10:03,960 -> 10:38,120] holding on the final formula.

        # Introduce the Holographic Principle
        holographic_text = Text("The Holographic Principle", font_size=48, color=YELLOW_D)
        self.play(FadeOut(new_s, shift=DOWN), run_time=2.0) # Changed: Fade out formula
        self.play(Write(holographic_text), run_time=3.0) # Changed: Fade in text
        self.wait(13.8) # Changed: Synced with narration [10:38,120 -> 10:56,920] "...the Holographic Principle."

        self.wait(31.48) # Changed: Synced with narration [10:56,920 -> 11:28,400] holding on the principle text.

        # Final fade out for credits
        self.play(FadeOut(holographic_text), run_time=2.0) # Changed: Fade out for the end.
        self.wait(10) # Changed: Wait for the rest of the outro audio.