import cadquery as cq
import math

R = 15.0
L = 60.0
pitch = 2 * math.pi * R   # ~45 degree helix for a diamond pattern
ext = 5.0
H = L + 2 * ext
starts = 10
depth = 0.8

cyl = cq.Workplane("XY").circle(R).extrude(L)

def groove(lefthand):
    helix = cq.Wire.makeHelix(pitch, H, R, center=cq.Vector(0, 0, -ext), lefthand=lefthand)
    z0 = -ext
    pts = [(R - depth, z0), (R + 0.7, z0 - 1.0), (R + 0.7, z0 + 1.0)]
    prof = cq.Workplane("XZ").polyline(pts).close()
    return prof.sweep(cq.Workplane(obj=helix), isFrenet=True).val()

solids = []
for lh in (False, True):
    g = groove(lh)
    for i in range(starts):
        solids.append(g.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), i * 360.0 / starts))

grooves = cq.Compound.makeCompound(solids)
result = cyl.cut(cq.Workplane(obj=grooves))
