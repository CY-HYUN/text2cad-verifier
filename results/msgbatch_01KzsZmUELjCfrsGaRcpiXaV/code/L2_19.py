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
# Each plate runs the full length of the tube, but fits within the inner diameter

# First rectangular plate (along X-axis direction, in YZ plane)
plate1 = cq.Workplane("XY").box(
    length=cross_thickness,
    width=inner_diameter,
    height=length,
    centered=True
)

# Second rectangular plate (along Y-axis direction, in XZ plane)
plate2 = cq.Workplane("XY").box(
    length=inner_diameter,
    width=cross_thickness,
    height=length,
    centered=True
)

# Combine the two plates to form the cross
cross_divider = plate1.union(plate2)

# Subtract the inner cavity from the outer cylinder
tube = outer_cylinder.cut(inner_cylinder)

# Add the cross divider to create the channels
result = tube.union(cross_divider)
