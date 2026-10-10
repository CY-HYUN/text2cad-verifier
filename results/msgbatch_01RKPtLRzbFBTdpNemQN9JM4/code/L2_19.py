import cadquery as cq

# Tube: OD 40, ID 30, length 50
tube = cq.Workplane("XY").circle(20).circle(15).extrude(50)

# Cross plates: 2 mm thick, spanning the inner diameter, full length
# Extend slightly into the wall (to 20) to ensure a fused solid
plate1 = cq.Workplane("XY").rect(30.0 + 2, 2).extrude(50)
plate2 = cq.Workplane("XY").rect(2, 30.0 + 2).extrude(50)

# Intersect cross with outer cylinder to keep within tube bounds
cross = plate1.union(plate2)
outer = cq.Workplane("XY").circle(20).extrude(50)
cross = cross.intersect(outer)

result = tube.union(cross)
