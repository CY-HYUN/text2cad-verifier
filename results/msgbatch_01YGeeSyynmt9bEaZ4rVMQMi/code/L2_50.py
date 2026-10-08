import cadquery as cq

# Stepped shaft dimensions (axis along X)
# Left section: D20 x 30, Middle: D30 x 40, Right: D20 x 30
L1, D1 = 30.0, 20.0
L2, D2 = 40.0, 30.0
L3, D3 = 30.0, 20.0
Ltot = L1 + L2 + L3

# Half-profile in XY plane (x along axis, y = radius), revolve about X axis
pts = [
    (0, 0),
    (0, D1 / 2),
    (L1, D1 / 2),
    (L1, D2 / 2),
    (L1 + L2, D2 / 2),
    (L1 + L2, D3 / 2),
    (Ltot, D3 / 2),
    (Ltot, 0),
]
shaft = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .revolve(360, (0, 0, 0), (1, 0, 0))
)

# Keyway: tangent plane on top of middle cylinder (z = R2), slot 20 x 6, cut 3.5 deep
keyway = (
    cq.Workplane("XY")
    .workplane(offset=D2 / 2)
    .center(L1 + L2 / 2, 0)
    .slot2D(20, 6, 0)
    .extrude(-3.5)
)
shaft = shaft.cut(keyway)

# Center holes on both end faces: D5, depth 10
hole_left = cq.Workplane("YZ").circle(2.5).extrude(10)
hole_right = cq.Workplane("YZ").workplane(offset=Ltot - 10).circle(2.5).extrude(10)
shaft = shaft.cut(hole_left).cut(hole_right)

result = shaft
