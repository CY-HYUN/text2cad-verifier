import cadquery as cq
import math

# Create the outer hollow cube (60mm edge length)
outer_cube = cq.Workplane("XY").box(60, 60, 60)

# Create a slightly smaller cube to subtract (making it hollow)
# We'll subtract a cube that's slightly smaller to create walls
inner_void = cq.Workplane("XY").box(56, 56, 56)

# Create the hollow outer cube by subtracting
hollow_outer = outer_cube.cut(inner_void)

# Create the small solid cube at the center (20mm edge length)
small_cube = cq.Workplane("XY").box(20, 20, 20)

# Create cylindrical rods connecting the small cube to the outer shell
# The rods connect from the center of each face of the small cube to the inner wall
# Small cube faces are at distance 10mm from center
# Inner wall of outer cube is at distance 28mm from center
# Rod length = 28 - 10 = 18mm

rod_diameter = 2
rod_radius = rod_diameter / 2
rod_length = 18  # Distance from small cube face to inner wall

# Create rods along the 6 faces (±X, ±Y, ±Z directions)
rods = cq.Workplane("XY")

# Rod along +X direction
rod_x_pos = cq.Workplane("XY").moveTo(0, 0).cylinder(rod_length, rod_radius, centered=False).translate((10, 0, 0))
rods = rods.union(rod_x_pos)

# Rod along -X direction
rod_x_neg = cq.Workplane("XY").moveTo(0, 0).cylinder(rod_length, rod_radius, centered=False).translate((-10, 0, 0)).rotateAboutCenter((0, 1, 0), 180)
rods = rods.union(rod_x_neg)

# Rod along +Y direction
rod_y_pos = cq.Workplane("XY").moveTo(0, 0).cylinder(rod_length, rod_radius, centered=False).translate((0, 10, 0)).rotateAboutCenter((1, 0, 0), 90)
rods = rods.union(rod_y_pos)

# Rod along -Y direction
rod_y_neg = cq.Workplane("XY").moveTo(0, 0).cylinder(rod_length, rod_radius, centered=False).translate((0, -10, 0)).rotateAboutCenter((1, 0, 0), 90)
rods = rods.union(rod_y_neg)

# Rod along +Z direction
rod_z_pos = cq.Workplane("XY").moveTo(0, 0).cylinder(rod_length, rod_radius, centered=False).translate((0, 0, 10)).rotateAboutCenter((1, 0, 0), 90)
rods = rods.union(rod_z_pos)

# Rod along -Z direction
rod_z_neg = cq.Workplane("XY").moveTo(0, 0).cylinder(rod_length, rod_radius, centered=False).translate((0, 0, -10)).rotateAboutCenter((1, 0, 0), 90)
rods = rods.union(rod_z_neg)

# Combine the structure: hollow outer cube + small cube + connecting rods
result = hollow_outer.union(small_cube).union(rods)
