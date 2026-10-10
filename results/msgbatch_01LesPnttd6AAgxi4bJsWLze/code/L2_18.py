import cadquery as cq
import math

# Create the main body
main_body = cq.Workplane("XY").box(100, 40, 30)

# Create the semicircular slide (groove) on top surface
# The semicircle has a radius that spans most of the width
# We'll create a half-cylinder to subtract from the top
semicircle_radius = 20  # Half of the width (40mm)
half_cylinder = (
    cq.Workplane("XZ")
    .center(0, 15)  # Center at the top of the block
    .moveTo(0, 0)
    .transformed(offset=cq.Vector(0, -20, 0))
    .cylinder(100, semicircle_radius, centered=True)
)

# Subtract the semicircle (we need to cut only the top half)
# Create a semicircular groove by subtracting a half-cylinder
body_with_groove = main_body.cut(
    cq.Workplane("XY")
    .moveTo(0, 0)
    .cylinder(15, semicircle_radius, centered=True)
)

# Actually, let's use a different approach for the semicircular groove
# Create the main body first
result = cq.Workplane("XY").box(100, 40, 30)

# Create semicircular groove using a half-cylinder subtraction
# Position a cylinder at the top and subtract its upper half
groove = (
    cq.Workplane("XZ")
    .center(0, 15)  # At the top surface (height/2 = 15)
    .moveTo(0, -20)  # Move to the center of width
    .cylinder(100, 20, centered=True)  # 100mm long, 20mm radius
)

result = result.cut(groove)

# Create the two rectangular weight-reduction grooves on the sides
# Each groove: 60mm long, 10mm high, 5mm deep
# These are cut into the sides of the slide

# First weight-reduction groove on one side (negative Y direction)
groove1 = (
    cq.Workplane("XY")
    .moveTo(-20, -20)  # Start position (centered along length, at the edge)
    .rect(60, 10)  # 60mm long, 10mm high
    .extrude(-5)  # 5mm deep (into the block)
)

result = result.cut(groove1)

# Second weight-reduction groove on the other side (positive Y direction)
groove2 = (
    cq.Workplane("XY")
    .moveTo(-20, 20)  # Start position on opposite side
    .rect(60, 10)  # 60mm long, 10mm high
    .extrude(-5)  # 5mm deep (into the block)
)

result = result.cut(groove2)
