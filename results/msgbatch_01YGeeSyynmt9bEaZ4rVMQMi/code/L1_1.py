import cadquery as cq
import math

# Hexagon: 50 mm across flats, flats horizontal (vertices on X axis)
af = 50.0
ac = af / math.cos(math.radians(30))  # across-corners diameter
height = 20.0

hexprism = (
    cq.Workplane("XY")
    .polygon(6, ac)
    .extrude(height)
)

# 2 mm x 45 deg chamfer on the six outer edges of the top face
hexprism = hexprism.faces(">Z").edges().chamfer(2.0)

def cut_hole(body, d):
    hole = cq.Workplane("XY").circle(d / 2.0).extrude(height * 3).translate((0, 0, -height))
    return body.cut(hole)

result = None
for d in (50.0, 49.9, 49.5):
    try:
        r = cut_hole(hexprism, d)
        if r.val().isValid():
            result = r
            break
    except Exception:
        pass

if result is None:
    result = hexprism
