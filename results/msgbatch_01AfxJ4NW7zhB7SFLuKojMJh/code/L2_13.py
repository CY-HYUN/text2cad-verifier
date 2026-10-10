import cadquery as cq
import math

R = 30.0
phi = (1 + math.sqrt(5)) / 2
a = R * 4 / (math.sqrt(3) * (1 + math.sqrt(5)))
ri = a * math.sqrt((25 + 11 * math.sqrt(5)) / 10) / 2  # face distance from center

def unit(v):
    l = math.sqrt(sum(c * c for c in v))
    return cq.Vector(v[0] / l, v[1] / l, v[2] / l)

def perp(n):
    t = cq.Vector(1, 0, 0) if abs(n.x) < 0.9 else cq.Vector(0, 1, 0)
    return n.cross(t).normalized()

# all 12 face normals
normals = []
for s1 in (1, -1):
    for s2 in (1, -1):
        normals.append(unit((0, s1 * 1, s2 * phi)))
        normals.append(unit((s1 * 1, s2 * phi, 0)))
        normals.append(unit((s1 * phi, 0, s2 * 1)))

body = cq.Workplane("XY").box(120, 120, 120)
for n in normals:
    pl = cq.Plane(origin=n * ri, xDir=perp(n), normal=n)
    cutter = cq.Workplane(pl).rect(300, 300).extrude(150)
    body = body.cut(cutter)

# through holes along the 6 face axes
axes = [unit((0, 1, phi)), unit((0, 1, -phi)),
        unit((1, phi, 0)), unit((1, -phi, 0)),
        unit((phi, 0, 1)), unit((-phi, 0, 1))]
hole_r = 12.0
for n in axes:
    pl = cq.Plane(origin=n * (-60), xDir=perp(n), normal=n)
    cyl = cq.Workplane(pl).circle(hole_r).extrude(120)
    body = body.cut(cyl)

result = body
