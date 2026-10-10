import cadquery as cq
import math

L, W, H = 150.0, 100.0, 30.0

# Base
base = cq.Workplane("XY").box(L, W, H, centered=(True, True, False))

# Dovetail guide (trapezoid in YZ plane, extruded along X)
dh = 15.0
lb = 60.0
off = dh * math.tan(math.radians(30))
ub = lb - 2 * off
dove = (
    cq.Workplane("YZ")
    .polyline([(-lb / 2, H), (lb / 2, H), (ub / 2, H + dh), (-ub / 2, H + dh)])
    .close()
    .extrude(L / 2, both=True)
)
body = base.union(dove)

# Oil grooves at junction of dovetail and base top (2 wide, 1 deep)
for s in (1, -1):
    g = (
        cq.Workplane("XY")
        .box(L + 2, 2.0, 1.0, centered=(True, True, False))
        .translate((0, s * (lb / 2 + 1.0), H - 1.0))
    )
    body = body.cut(g)

# Side T-slots
zc = 15.0
for s in (1, -1):
    opening = (
        cq.Workplane("XY")
        .box(L + 2, 6.0, 10.0)
        .translate((0, s * (W / 2 - 3.0), zc))
    )
    wide = (
        cq.Workplane("XY")
        .box(L + 2, 6.0, 16.0)
        .translate((0, s * (W / 2 - 9.0), zc))
    )
    body = body.cut(opening).cut(wide)

# Central through hole
hole = cq.Workplane("XY").circle(15.0).extrude(H + dh + 2).translate((0, 0, -1))
body = body.cut(hole)

# Counterbore
cb = cq.Workplane("XY").circle(20.0).extrude(6.0).translate((0, 0, H + dh - 5.0))
body = body.cut(cb)

result = body
