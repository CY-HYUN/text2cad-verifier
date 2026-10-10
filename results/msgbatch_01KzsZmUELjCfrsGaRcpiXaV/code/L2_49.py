import cadquery as cq
import math

# Create Ring A (horizontal ring in XY plane)
# Build using a circular sketch revolved around a center point
center_radius = 17.5
wire_radius = 2.5

# Ring A: horizontal torus created by revolving a circle around the Z axis
ring_a = (
    cq.Workplane("XY")
    .circle(wire_radius)
    .revolve(360, (center_radius, 0, 0), (center_radius, 0, 1))
)

# Ring B: vertical torus created by revolving a circle around the Y axis
# Position it so it passes through the hole of Ring A
ring_b = (
    cq.Workplane("YZ")
    .circle(wire_radius)
    .revolve(360, (0, center_radius, 0), (0, center_radius, 1))
)

# Union the two rings together
result = ring_a.union(ring_b)
