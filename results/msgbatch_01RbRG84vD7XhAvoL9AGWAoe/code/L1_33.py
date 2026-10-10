import cadquery as cq

L = 100.0
R_out = 30.0
R_in = 20.0

# Full tube along X
tube = (
    cq.Workplane("YZ")
    .circle(R_out)
    .circle(R_in)
    .extrude(L)
)

# Keep only the half with z >= 0
keep = cq.Workplane("XY").box(L, 2 * R_out + 2, R_out + 1, centered=(False, True, False))

result = tube.intersect(keep)
