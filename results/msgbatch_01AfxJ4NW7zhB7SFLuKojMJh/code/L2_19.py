import cadquery as cq
import math

L = 50.0
tube = cq.Workplane("XY").circle(20).circle(15).extrude(L)

# Cross plates spanning the inner bore (slightly overlapping into the wall for a solid union)
plate1 = cq.Workplane("XY").rect(30.0 + 2, 2).extrude(L)
plate2 = cq.Workplane("XY").rect(2, 30.0 + 2).extrude(L)

# Clip the plates to the outer cylinder so nothing protrudes
clip = cq.Workplane("XY").circle(20).extrude(L)
cross = plate1.union(plate2).intersect(clip)

result = tube.union(cross)
