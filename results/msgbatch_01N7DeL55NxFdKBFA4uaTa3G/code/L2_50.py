import cadquery as cq

# Stepped shaft dimensions (along X axis)
L1, D1 = 30.0, 20.0   # left section
L2, D2 = 40.0, 30.0   # middle section
L3, D3 = 30.0, 20.0   # right section
L = L1 + L2 + L3

# Half profile in XY plane (x = axis, y = radius), revolved about X axis
pts = [
    (0, 0),
    (0, D1 / 2),
    (L1, D1 / 2),
    (L1, D2 / 2),
    (L1 + L2, D2 / 2),
    (L1 + L2, D3 / 2),
    (L, D3 / 2),
    (L, 0),
]
shaft = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .revolve(360, (0, 0, 0), (1, 0, 0))
)

# Tangent plane on top of middle cylinder, straight slot 20 x 6, cut 3.5 deep
key = (
    cq.Workplane("XY", origin=(L1 + L2 / 2, 0, D2 / 2))
    .slot2D(20, 6, 0)
    .extrude(-3.5)
)
shaft = shaft.cut(key)

# Center holes on both end faces: dia 5, depth 10
hole_left = cq.Workplane("YZ", origin=(0, 0, 0)).circle(2.5).extrude(10)
hole_right = cq.Workplane("YZ", origin=(L, 0, 0)).circle(2.5).extrude(-10)
shaft = shaft.cut(hole_left).cut(hole_right)

result = shaft
