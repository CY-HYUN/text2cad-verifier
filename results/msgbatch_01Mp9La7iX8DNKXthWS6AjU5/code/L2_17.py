import cadquery as cq
import math

# Dimensions (assumed)
inner_tube_ri = 20.0
inner_tube_ro = 25.0
outer_tube_ri = 55.0
outer_tube_ro = 60.0
rib_t = 4.0
height = 50.0

# Inner ring
inner_ring = (cq.Workplane("XY").circle(inner_tube_ro).circle(inner_tube_ri).extrude(height))
# Outer ring
outer_ring = (cq.Workplane("XY").circle(outer_tube_ro).circle(outer_tube_ri).extrude(height))

# Four rectangular stiffeners spanning from the inner tube to the outer tube (overlapping into walls)
rib_len = outer_tube_ri - inner_tube_ro + 2.0  # slight overlap into both tubes
rib_center = (outer_tube_ri + inner_tube_ro) / 2.0

result = inner_ring.union(outer_ring)
for i in range(4):
    ang = i * 90.0
    rib = (cq.Workplane("XY")
           .center(rib_center, 0)
           .rect(rib_len, rib_t)
           .extrude(height)
           .rotate((0, 0, 0), (0, 0, 1), ang))
    result = result.union(rib)

result = result.clean()
