import cadquery as cq
import math

# Create a 3D part with an outer circle, inner circle, and cross brace
# Outer diameter: 40mm, Inner diameter: 30mm, Height: 50mm

# Start with a solid cylinder (outer circle)
outer_radius = 20  # 40mm diameter
inner_radius = 15  # 30mm diameter
height = 50
brace_thickness = 2  # Thickness of the cross brace

# Create the outer cylinder
result = cq.Workplane("XY").circle(outer_radius).extrude(height)

# Subtract the inner cylinder to create the hollow tube
result = result.faces(">Z").workplane().circle(inner_radius).cutThruAll()

# Create the cross brace as two rectangles that connect the inner and outer walls
# The cross divides the inner cavity into 4 independent channels
# Brace width (total width of the cross at the center)
brace_width = brace_thickness * 2

# Create first rectangle of the cross (along X-axis)
# It extends from -outer_radius to +outer_radius, with thickness in Y
brace1 = (
    cq.Workplane("XY")
    .rect(outer_radius * 2, brace_width)
    .extrude(height)
)

# Create second rectangle of the cross (along Y-axis)
# It extends from -outer_radius to +outer_radius, with thickness in X
brace2 = (
    cq.Workplane("XY")
    .rect(brace_width, outer_radius * 2)
    .extrude(height)
)

# Combine the two braces
cross_brace = brace1.union(brace2)

# Intersect the cross brace with the hollow cylinder to keep only the part inside
cross_brace = cross_brace.intersect(cq.Workplane("XY").circle(outer_radius).extrude(height))

# Add the cross brace to the hollow cylinder
result = result.union(cross_brace)

# Ensure the result is a single solid
result = result.val()
