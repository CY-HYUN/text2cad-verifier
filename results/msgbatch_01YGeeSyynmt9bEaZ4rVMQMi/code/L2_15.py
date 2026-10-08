import cadquery as cq
import math

R = 40.0
T = 10.0

# Base disc
disc = cq.Workplane("XY").circle(R).extrude(T)

# Build the tools for one feature pair
w = 8.0          # U-groove width
r_in = 24.0      # inner end (center of rounded end) of U-groove
groove = (
    cq.Workplane("XY")
    .center((r_in + R + 5) / 2, 0)
    .rect(R + 5 - r_in, w)
    .extrude(T)
    .union(cq.Workplane("XY").center(r_in, 0).circle(w / 2).extrude(T))
)

# Semicircular edge cutout (circle of radius 20 centered on the rim, adjacent quadrant at 45°)
a = math.radians(45)
semi = cq.Workplane("XY").center(R * math.cos(a), R * math.sin(a)).circle(20).extrude(T)

feature = groove.union(semi)

result = disc
for i in range(4):
    result = result.cut(feature.rotate((0, 0, 0), (0, 0, 1), 90 * i))

# Center hole
result = result.cut(cq.Workplane("XY").circle(5).extrude(T))
