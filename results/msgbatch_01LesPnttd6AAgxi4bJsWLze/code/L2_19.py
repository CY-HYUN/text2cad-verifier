import cadquery as cq
import math

# Create the main tube
outer_diameter = 40
inner_diameter = 30
length = 50
cross_thickness = 2

# Start with the outer cylinder
outer_cylinder = cq.Workplane("XY").cylinder(height=length, radius=outer_diameter/2, centered=True)

# Create the inner cavity (to be subtracted)
inner_cylinder = cq.Workplane("XY").cylinder(height=length, radius=inner_diameter/2, centered=True)

# Create the cross-shaped divider plate
# The cross consists of two rectangular plates intersecting at 90 degrees
# Each plate runs the full length of the tube

# First rectangular plate (along X-axis)
plate1 = cq.Workplane("XY").box(
    length=length,
    width=cross_thickness,
    height=inner_diameter,
    centered=True
)

# Second rectangular plate (along Y-axis)
plate2 = cq.Workplane("XY").box(
    length=length,
    width=inner_diameter,
    height=cross_thickness,
    centered=True
)

# Combine the two plates to form the cross
cross_divider = plate1.union(plate2)

# Subtract the inner cavity from the outer cylinder
tube = outer_cylinder.cut(inner_cylinder)

# Add the cross divider to create the channels
# The cross divider should be positioned so it divides the inner cavity
result = tube.union(cross_divider)

