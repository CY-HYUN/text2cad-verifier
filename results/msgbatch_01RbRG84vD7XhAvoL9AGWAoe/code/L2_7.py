import cadquery as cq

# Ring parameters
ring_od = 60.0
ring_id = 30.0
thk = 15.0
hole_offset = 5.0  # inner hole offset toward the rod (+X)

# Rod parameters
rod_w = 20.0
rod_len = 80.0
rod_start = ring_od / 2.0  # starts at outer side of ring
small_hole_d = 10.0

# Ring body
ring = cq.Workplane("XY").circle(ring_od / 2.0).extrude(thk)

# Rod (slight overlap into ring for solid union)
overlap = 5.0
rod = (
    cq.Workplane("XY")
    .center(rod_start + rod_len / 2.0 - overlap / 2.0, 0)
    .rect(rod_len + overlap, rod_w)
    .extrude(thk)
)

body = ring.union(rod)

# Eccentric inner hole of the ring
body = body.cut(
    cq.Workplane("XY").center(hole_offset, 0).circle(ring_id / 2.0).extrude(thk)
)

# Through-hole at far end of rod
end_x = rod_start + rod_len - rod_w / 2.0
body = body.cut(
    cq.Workplane("XY").center(end_x, 0).circle(small_hole_d / 2.0).extrude(thk)
)

result = body
