import cadquery as cq
import math

L, W, H = 150.0, 100.0, 30.0
dt_bot = 60.0
dt_h = 15.0
dt_top = dt_bot - 2 * dt_h * math.tan(math.radians(30))

# Base
base = cq.Workplane("XY").box(L, W, H, centered=(True, True, False))

# Dovetail guide (trapezoid in YZ, extruded along X)
dove = (
    cq.Workplane("YZ", origin=(-L / 2, 0, 0))
    .polyline([(-dt_bot / 2, H), (dt_bot / 2, H),
               (dt_top / 2, H + dt_h), (-dt_top / 2, H + dt_h)])
    .close()
    .extrude(L)
)
result = base.union(dove)

# Oil grooves at the dovetail/base junction
for s in (1, -1):
    yc = s * (dt_bot / 2 + 1.0)
    groove = cq.Workplane("XY").box(L + 2, 2.0, 1.0).translate((0, yc, H - 0.5))
    result = result.cut(groove)

# Side T-slots
zc = 15.0
for s in (1, -1):
    neck = cq.Workplane("XY").box(L + 2, 6.0, 10.0).translate((0, s * (W / 2 - 3.0), zc))
    wide = cq.Workplane("XY").box(L + 2, 6.0, 16.0).translate((0, s * (W / 2 - 9.0), zc))
    result = result.cut(neck).cut(wide)

# Central through hole
hole = cq.Workplane("XY").circle(15.0).extrude(H + dt_h + 2).translate((0, 0, -1))
result = result.cut(hole)

# Counterbore
cbore = cq.Workplane("XY", origin=(0, 0, H + dt_h - 5.0)).circle(20.0).extrude(6.0)
result = result.cut(cbore)
