import cadquery as cq
import math

L, W, H = 150.0, 100.0, 30.0

# Rectangular base, bottom at Z=0, top at Z=30
base = cq.Workplane("XY").box(L, W, H).translate((0, 0, H / 2))

# Dovetail guide: trapezoid in the YZ plane, extruded along X
hb = 60.0 / 2
dh = 15.0
ht = hb - dh * math.tan(math.radians(30))  # ~21.34
dovetail = (
    cq.Workplane("YZ", origin=(-L / 2, 0, 0))
    .polyline([(-hb, H), (hb, H), (ht, H + dh), (-ht, H + dh)])
    .close()
    .extrude(L)
)
body = base.union(dovetail)

# Oil grooves at the dovetail/base junction: 2 mm wide, 1 mm deep, full length
for s in (1, -1):
    g = cq.Workplane("XY").box(L, 2.0, 1.0).translate((0, s * (hb + 1.0), H - 0.5))
    body = body.cut(g)

# Side T-slots along X, centred at Z=15
for s in (1, -1):
    neck = cq.Workplane("XY").box(L, 6.0, 10.0).translate((0, s * (W / 2 - 3.0), 15))
    wide = cq.Workplane("XY").box(L, 6.0, 16.0).translate((0, s * (W / 2 - 9.0), 15))
    body = body.cut(neck).cut(wide)

# Central through hole, 30 mm diameter
hole = cq.Workplane("XY").circle(15.0).extrude(H + dh + 2).translate((0, 0, -1))
body = body.cut(hole)

# Counterbore, 40 mm diameter, 5 mm deep from Z=45
cb = cq.Workplane("XY").workplane(offset=H + dh - 5.0).circle(20.0).extrude(6.0)
body = body.cut(cb)

result = body
