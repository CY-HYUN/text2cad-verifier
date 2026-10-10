import cadquery as cq
import math

R = 15.0
L = 60.0
pitch = 60.0
n_starts = 10
z0 = -5.0
h = L + 10.0

body = cq.Workplane("XY").circle(R).extrude(L)

def groove(lefthand):
    helix = cq.Wire.makeHelix(pitch, h, R, center=cq.Vector(0, 0, z0),
                              dir=cq.Vector(0, 0, 1), lefthand=lefthand)
    pts = [(R + 0.6, -1.2), (R + 0.6, 1.2), (R - 1.0, 0.0)]
    pts = [(x, z0 + y) for x, y in pts]
    prof = cq.Workplane("XZ").polyline(pts).close()
    return prof.sweep(cq.Workplane(obj=helix), isFrenet=True).val()

def apply_set(base, lefthand):
    g = groove(lefthand)
    copies = [g.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), i * 360.0 / n_starts)
              for i in range(n_starts)]
    tool = cq.Compound.makeCompound(copies)
    return base.cut(cq.Workplane(obj=tool))

result = apply_set(body, False)
result = apply_set(result, True)
