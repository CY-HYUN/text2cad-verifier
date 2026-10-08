import cadquery as cq

# Parameters
ring_od = 60.0
ring_id = 30.0
thk = 15.0
rod_w = 20.0
rod_len = 80.0
hole_d = 10.0
ecc = 5.0  # offset of inner bore toward rod

r_out = ring_od / 2.0

# Main ring disc (outer cylinder centered at origin)
ring = cq.Workplane("XY").circle(r_out).extrude(thk)

# Rod extending radially along +X from the outer side of the ring
rod_start = r_out - 5.0  # slight overlap into ring for clean fusion
rod_end = r_out + rod_len
rod = (
    cq.Workplane("XY")
    .center((rod_start + rod_end) / 2.0, 0)
    .rect(rod_end - rod_start, rod_w)
    .extrude(thk)
)

body = ring.union(rod)

# Eccentric inner bore, offset 5mm toward the rod
bore = (
    cq.Workplane("XY")
    .center(ecc, 0)
    .circle(ring_id / 2.0)
    .extrude(thk)
)
body = body.cut(bore)

# Through-hole at the far end of the rod, axis parallel to ring axis
hole_x = rod_end - rod_w / 2.0
hole = (
    cq.Workplane("XY")
    .center(hole_x, 0)
    .circle(hole_d / 2.0)
    .extrude(thk)
)
result = body.cut(hole)
