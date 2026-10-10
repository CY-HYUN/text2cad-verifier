import cadquery as cq
import math

# Create Ring A (horizontal ring)
# Outer diameter 40, inner diameter 30, so outer radius 20, inner radius 15
# We'll make it with a rectangular cross-section for the torus
ring_a = cq.Workplane("XY").circle(17.5).circle(15).extrude(5)

# Create a torus-like ring A by using a circular path
center_radius_a = 17.5
wire_radius_a = 2.5

# Build Ring A as a torus (horizontal, in XY plane)
ring_a = (
    cq.Workplane("XY")
    .circle(wire_radius_a)
    .revolve(angle=360, axisStart=(center_radius_a, 0, 0), axisEnd=(center_radius_a, 0, 5))
)

# Create Ring B (vertical ring) - positioned to pass through Ring A
# Ring B should be in the YZ plane, offset so it passes through A's hole
center_radius_b = 17.5
wire_radius_b = 2.5

# Build Ring B as a torus (vertical, in YZ plane)
ring_b = (
    cq.Workplane("YZ")
    .circle(wire_radius_b)
    .revolve(angle=360, axisStart=(0, center_radius_b, 0), axisEnd=(0, center_radius_b, 5))
)

# Combine both rings into a single compound
result = ring_a.union(ring_b)
