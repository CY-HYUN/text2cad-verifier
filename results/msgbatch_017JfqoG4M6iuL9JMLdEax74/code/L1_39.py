import cadquery as cq

L = 60.0
W = 40.0
T = 10.0
R = W / 2

result = (
    cq.Workplane("XY")
    .moveTo(0, -R)
    .lineTo(L, -R)
    .threePointArc((L + R, 0), (L, R))
    .lineTo(0, R)
    .close()
    .extrude(T)
)
