# To render this scene, run the following command in your terminal:
# manim -pql black_hole_physical_lattice.py PhysicalBlackHoleLattice

from manim import *
import numpy as np

class PhysicalBlackHoleLattice(ThreeDScene):
    """
    An animation of a 3D spacetime lattice being warped by a central mass.
    This version uses a warp function derived directly from the Schwarzschild
    metric, providing a more physically meaningful visualization.
    """
    def construct(self):
        # 1. --- CONFIGURATION ---
        
        # Physical and Grid properties
        SCHWARZSCHILD_RADIUS = 0.75  # The radius of the event horizon (Rs)
        GRID_BOUNDS = 4.0           # How large the flat grid is
        GRID_STEP = 1.0             # Spacing between grid lines
        
        # This is now our main artistic control parameter. It scales the
        # physical effect to make it more or less visually pronounced.
        WARP_AMPLITUDE = 1.2
        
        # Colors
        INNER_COLOR = GREEN_B
        OUTER_COLOR = BLUE_D
        STROKE_WIDTH = 2.5

        # 2. --- SCENE SETUP ---
        self.set_camera_orientation(phi=70 * DEGREES, theta=-120 * DEGREES, zoom=0.6)
        self.camera.light_source.move_to([-10, -10, 20])

        # 3. --- CORE LOGIC: THE PHYSICAL WARP FUNCTION ---
        
        def warp_space_physical(point):
            """
            Deforms a point in 3D space based on the Schwarzschild metric.
            This version explicitly handles the origin to prevent runtime warnings.
            """
            r = np.linalg.norm(point) # The point's distance from the center in "flat" space
            
            # --- FIX ---
            # Handle the special case of the origin (r=0) immediately.
            # If the point is the origin, it doesn't move. This prevents division by zero.
            if r == 0:
                return point # Return [0, 0, 0]

            # If inside the event horizon (but not at the origin), clamp to the surface.
            # This branch is now safe because we know r > 0.
            if r < SCHWARZSCHILD_RADIUS:
                return point * (SCHWARZSCHILD_RADIUS / r)

            # --- Physical Calculation for points outside the event horizon ---
            # The time dilation factor is sqrt(1 - Rs/r).
            # We define a "warp factor" from 0 (at infinity) to 1 (at Rs).
            warp_factor = 1 - np.sqrt(1 - SCHWARZSCHILD_RADIUS / r)
            
            # The total inward displacement is this physical factor scaled by our amplitude.
            displacement = WARP_AMPLITUDE * warp_factor
            
            # Calculate the new, warped radius.
            new_radius = r - displacement
            
            # Clamp again in case a large amplitude pulls a point inside the horizon
            new_radius = max(SCHWARZSCHILD_RADIUS, new_radius)
            
            # Return the original point vector, scaled to its new length.
            return point * (new_radius / r)
        # 4. --- OBJECT CREATION ---

        # A true black hole is perfectly black.
        black_hole = Sphere(
            radius=SCHWARZSCHILD_RADIUS, resolution=(48, 48), color=BLACK
        )

        print("Constructing physically warped lattice...")
        grid = VGroup()
        coords = np.arange(-GRID_BOUNDS, GRID_BOUNDS + GRID_STEP, GRID_STEP)
        
        def add_colored_warped_line(start, end, vgroup):
            # Midpoint logic remains the same
            flat_midpoint = interpolate(start, end, 0.5)
            warped_midpoint = warp_space_physical(flat_midpoint)
            distance = np.linalg.norm(warped_midpoint)
            alpha = min(1, distance / (GRID_BOUNDS * 1.2))
            line_color = interpolate_color(INNER_COLOR, OUTER_COLOR, alpha)
            
            # Create the line using the new physical warp function
            line = ParametricFunction(
                lambda t: warp_space_physical(interpolate(start, end, t)),
                t_range=[0, 1],
                color=line_color,
                stroke_width=STROKE_WIDTH
            )
            vgroup.add(line)

        # Generate lines (same as before, but using the new warp logic)
        for i in coords:
            for j in coords:
                add_colored_warped_line(np.array([i, j, -GRID_BOUNDS]), np.array([i, j, GRID_BOUNDS]), grid)
                add_colored_warped_line(np.array([i, -GRID_BOUNDS, j]), np.array([i, GRID_BOUNDS, j]), grid)
                add_colored_warped_line(np.array([-GRID_BOUNDS, i, j]), np.array([GRID_BOUNDS, i, j]), grid)

        print("Lattice construction complete.")
        
        # 5. --- ANIMATION SEQUENCE ---
        self.add(black_hole) # Add the black hole instantly so it's there
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