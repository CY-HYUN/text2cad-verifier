import cadquery as cq
import math

ri, ro = 5.0, 25.0
ang = 30.0
h = 5.0

def pt(r, a):
    return (r * math.cos(math.radians(a)), r * math.sin(math.radians(a)))

def step():
    return (cq.Workplane("XY")
            .moveTo(*pt(ri, 0))
            .lineTo(*pt(ro, 0))
            .threePointArc(pt(ro, ang / 2), pt(ro, ang))
            .lineTo(*pt(ri, ang))
            .threePointArc(pt(ri, ang / 2), pt(ri, 0))
            .close()
            .extrude(h))

result = cq.Workplane("XY").circle(10).extrude(100)

for i in range(10):
    s = step().rotate((0, 0, 0), (0, 0, 1), i * 30).translate((0, 0, i * 10))
    result = result.union(s)
