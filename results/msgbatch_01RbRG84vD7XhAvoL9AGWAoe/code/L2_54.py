import cadquery as cq
import math

B = 40.0   # base edge
H = 40.0   # height
t = 4.0    # wall thickness at base (horizontal)

# Outer square pyramid
outer = (
    cq.Workplane("XY")
    .rect(B, B)
    .workplane(offset=H)
    .rect(0.01, 0.01)
    .loft(combine=True)
)

# Inner cavity pyramid (same slope), opening from the base
b2 = B - 2 * t
h2 = H * b2 / B
inner = (
    cq.Workplane("XY")
    .workplane(offset=-0.01)
    .rect(b2, b2)
    .workplane(offset=h2 + 0.01)
    .rect(0.01, 0.01)
    .loft(combine=True)
)

body = outer.cut(inner)

# Triangular through-holes on side faces (projected triangle in XZ)
tri = [(-12.0, 4.0), (12.0, 4.0), (0.0, 28.0)]
prismY = (
    cq.Workplane("XZ")
    .polyline(tri).close()
    .extrude(30, both=True)
)
prismX = prismY.rotate((0, 0, 0), (0, 0, 1), 90)

result = body.cut(prismY).cut(prismX)
