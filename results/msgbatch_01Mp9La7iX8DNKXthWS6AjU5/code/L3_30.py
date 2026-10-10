import cadquery as cq
import math

# Base
base = cq.Workplane("XY").box(150, 100, 30, centered=(True, True, False))

# Dovetail guide
dx = 15 * math.tan(math.radians(30))
pts = [(-30, 30), (30, 30), (30 - dx, 45), (-30 + dx, 45)]
dove = (cq.Workplane("YZ", origin=(-75, 0, 0))
        .polyline(pts).close().extrude(150))
result = base.union(dove)

# Oil grooves
for s in (1, -1):
    g = (cq.Workplane("XY")
         .box(150, 2, 1, centered=(True, True, False))
         .translate((0, s * 31, 29)))
    result = result.cut(g)

# Side T-slots
for s in (1, -1):
    neck = (cq.Workplane("XY").box(150, 6, 10)
            .translate((0, s * 47, 15)))
    wide = (cq.Workplane("XY").box(150, 6, 16)
            .translate((0, s * 41, 15)))
    result = result.cut(neck).cut(wide)

# Central through hole and counterbore
hole = cq.Workplane("XY").circle(15).extrude(45)
cb = cq.Workplane("XY").workplane(offset=40).circle(20).extrude(5)
result = result.cut(hole).cut(cb)
