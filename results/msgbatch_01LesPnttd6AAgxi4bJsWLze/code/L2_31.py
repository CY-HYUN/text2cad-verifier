import cadquery as cq
import math

# Create the base hollow sphere
outer_radius = 25  # outer diameter 50mm
inner_radius = 20  # inner diameter 40mm

# Create solid outer sphere
outer_sphere = cq.Workplane("XY").sphere(outer_radius)

# Create solid inner sphere to subtract
inner_sphere = cq.Workplane("XY").sphere(inner_radius)

# Create hollow spherical shell by subtracting inner from outer
hollow_sphere = outer_sphere.cut(inner_sphere)

# Create the square hole
# We need to cut a 20x20mm square through-hole along the X-axis
# The square will be positioned at the center of the sphere

square_size = 20
half_square = square_size / 2

# Create a square box that extends through the sphere along the X-axis
# The box needs to be large enough to cut through the entire sphere
cut_box = cq.Workplane("YZ").box(
    length=2 * outer_radius + 10,  # extend well beyond sphere in X direction
    xDim=square_size,              # square size in Y
    yDim=square_size               # square size in Z
).translate((0, 0, 0))

# Cut the square hole from the hollow sphere
result = hollow_sphere.cut(cut_box)
