import cadquery as cq
import math

L = 50.0

outer = (cq.Workplane("XY").circle(40).circle(35).extrude(L))
inner = (cq.Workplane("XY").circle(20).circle(15).extrude(L))

# Ribs span from inner tube wall to outer tube wall (overlap slightly into the walls for a solid union)
r_in = 17.5   # within inner tube wall (15..20)
r_out = 37.5  # within outer tube wall (35..40)
rib_len = r_out - r_in
rib_center = (r_in + r_out) / 2.0

result = outer.union(inner)
for i in range(4):
    ang = i * 90.0
    rib = (cq.Workplane("XY")
           .box(rib_len, 5, L, centered=(True, True, False))
           .translate((rib_center, 0, 0))
           .rotate((0, 0, 0), (0, 0, 1), ang))
    result = result.union(rib)

# Ensure the bores remain clear (ribs only occupy the gap and wall regions)
result = result.cut(cq.Workplane("XY").circle(15).extrude(L))
