import cadquery as cq
import math

# Base disc
disc_d = 100.0
disc_t = 10.0
result = cq.Workplane("XY").circle(disc_d / 2).extrude(disc_t)

# Frustum parameters
fr_base_d = 20.0
fr_top_d = 10.0
fr_h = 15.0
hole_d = 5.0
pitch_r = 30.0

positions = []
for i in range(3):
    a = math.radians(90 + i * 120)
    positions.append((pitch_r * math.cos(a), pitch_r * math.sin(a)))

for (x, y) in positions:
    cone = cq.Solid.makeCone(
        fr_base_d / 2, fr_top_d / 2, fr_h,
        pnt=cq.Vector(x, y, disc_t), dir=cq.Vector(0, 0, 1)
    )
    result = result.union(cq.Workplane("XY").add(cone))

# Through holes through frustums and disc
total_h = disc_t + fr_h
holes = (
    cq.Workplane("XY")
    .workplane(offset=-1)
    .pushPoints(positions)
    .circle(hole_d / 2)
    .extrude(total_h + 2)
)
result = result.cut(holes)
