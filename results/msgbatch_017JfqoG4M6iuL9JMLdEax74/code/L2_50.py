import cadquery as cq

# Stepped shaft along X axis
left = cq.Workplane("YZ").circle(20).extrude(30)
mid = cq.Workplane("YZ").workplane(offset=30).circle(15).extrude(40)
right = cq.Workplane("YZ").workplane(offset=70).circle(10).extrude(30)

shaft = left.union(mid).union(right)

# Keyway on top of middle section: 20 long, 6 wide, 3.5 deep
key_len, key_w, key_d = 20.0, 6.0, 3.5
keyway = (
    cq.Workplane("XY")
    .box(key_len, key_w, key_d + 1.0, centered=(True, True, False))
    .translate((50, 0, 15 - key_d))
)
shaft = shaft.cut(keyway)

# Center holes at both ends: dia 5, depth 10
hole_left = cq.Workplane("YZ").circle(2.5).extrude(10)
hole_right = cq.Workplane("YZ").workplane(offset=90).circle(2.5).extrude(10)
shaft = shaft.cut(hole_left).cut(hole_right)

result = shaft
