import cadquery as cq
import math

L = 50.0

outer = (cq.Workplane("XY").circle(40).circle(35).extrude(L))
inner = (cq.Workplane("XY").circle(20).circle(15).extrude(L))

# Ribs span from inner tube wall to outer tube wall (overlapping slightly for solid union)
rib_len = 35.0 - 20.0 + 2.0  # from r=19 to r=36 overlap into walls
r_start = 19.0
r_end = 36.0
rib_len = r_end - r_start
rib_center = (r_start + r_end) / 2.0

result = outer.union(inner)
for i in range(4):
    ang = i * 90.0
    rib = (cq.Workplane("XY")
           .box(rib_len, 5.0, L, centered=(True, True, False))
           .translate((rib_center, 0, 0))
           .rotate((0, 0, 0), (0, 0, 1), ang))
    result = result.union(rib)
