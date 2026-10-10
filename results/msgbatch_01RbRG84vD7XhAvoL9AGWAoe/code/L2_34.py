import cadquery as cq

length = 50.0
radius = 10.0
groove_width = 5.0
groove_depth = 9.0
neck_radius = radius - groove_depth  # 1 mm, leaves a 2 mm diameter neck

# Main cylinder along the Z axis, from z = 0 to z = 50
shaft = cq.Workplane("XY").circle(radius).extrude(length)

# Circumferential groove: remove a ring at mid-length
z0 = length / 2 - groove_width / 2
ring = (
    cq.Workplane("XY")
    .workplane(offset=z0)
    .circle(radius + 1)
    .circle(neck_radius)
    .extrude(groove_width)
)

result = shaft.cut(ring)
