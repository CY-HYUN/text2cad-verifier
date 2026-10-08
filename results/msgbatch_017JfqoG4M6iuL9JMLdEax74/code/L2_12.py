import cadquery as cq
import math

# Base disc
disc_d = 100.0
disc_t = 10.0
result = cq.Workplane("XY").circle(disc_d / 2).extrude(disc_t)

# Frustum parameters
r_base = 10.0
r_top = 5.0
h = 15.0
hole_d = 5.0
pcd_r = 30.0

positions = []
for i in range(3):
    a = math.radians(90 + i * 120)
    positions.append((pcd_r * math.cos(a), pcd_r * math.sin(a)))

for (x, y) in positions:
    cone = cq.Solid.makeCone(r_base, r_top, h,
                             pnt=cq.Vector(x, y, disc_t),
                             dir=cq.Vector(0, 0, 1))
    result = result.union(cq.Workplane("XY").add(cone))

# Through holes through frustum and disc
holes = (cq.Workplane("XY").workplane(offset=-1)
         .pushPoints(positions)
         .circle(hole_d / 2)
         .extrude(disc_t + h + 2))
result = result.cut(holes)
