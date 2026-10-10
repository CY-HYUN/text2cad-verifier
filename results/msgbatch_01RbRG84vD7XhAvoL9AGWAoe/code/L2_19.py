import cadquery as cq

outer_d = 40.0
inner_d = 30.0
length = 50.0
plate_t = 2.0

# Tube
tube = (
    cq.Workplane("XY")
    .circle(outer_d / 2)
    .circle(inner_d / 2)
    .extrude(length)
)

# Cross plates spanning the inner bore (slightly overlapping into wall for fusion)
span = inner_d + 1.0
plate_x = cq.Workplane("XY").box(span, plate_t, length, centered=(True, True, False))
plate_y = cq.Workplane("XY").box(plate_t, span, length, centered=(True, True, False))
cross = plate_x.union(plate_y)

# Trim the cross to the outer cylinder
clip = cq.Workplane("XY").circle(outer_d / 2).extrude(length)
cross = cross.intersect(clip)

result = tube.union(cross).clean()
