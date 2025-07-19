# To render this scene, run the following command in your terminal:
# manim -pql black_hole_physical_lattice.py PhysicalBlackHoleLattice

from manim import *
import numpy as np

class PhysicalBlackHoleLattice(ThreeDScene):
    """
    An animation of a 3D spacetime lattice being warped by a central mass.
    This version uses a warp function derived directly from the Schwarzschild
    metric, providing a more physically meaningful visualization.
    
    V3: Line colors now grade from White (intense warp) to Blue (flat space).
    """
    def construct(self):
        # 1. --- CONFIGURATION ---
        
        # Physical and Grid properties
        SCHWARZSCHILD_RADIUS = 0.75
        GRID_BOUNDS = 4.0
        GRID_STEP = 1.0
        WARP_AMPLITUDE = 1.2
        
        # --- CHANGE --- New color scheme for a better physical metaphor.
        # White for high-energy/warp areas, blue for calm, flat space.
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
            # The color and opacity logic now uses the new WHITE -> BLUE gradient.
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