import cadquery as cq

L = 100.0
Ro = 30.0
Ri = 20.0

# Full annular tube with axis along X (YZ workplane normal is +X)
tube = (cq.Workplane("YZ")
        .circle(Ro).circle(Ri)
        .extrude(L))

# Keep only the half with Z >= 0
keep = cq.Workplane("XY").box(L, 2 * Ro, Ro, centered=(False, True, False))

result = tube.intersect(keep)
