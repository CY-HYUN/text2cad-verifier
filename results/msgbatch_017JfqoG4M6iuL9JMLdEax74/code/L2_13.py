import cadquery as cq
import math

phi = (1 + math.sqrt(5)) / 2
R = 30.0
a = 4 * R / (math.sqrt(3) * (1 + math.sqrt(5)))          # edge length
r_in = a * math.sqrt(250 + 110 * math.sqrt(5)) / 20       # inradius
r_face = a / (2 * math.tan(math.radians(36)))             # pentagon inradius

axes = [(0, 1, phi), (0, 1, -phi), (1, phi, 0), (1, -phi, 0), (phi, 0, 1), (-phi, 0, 1)]
axes = [cq.Vector(*v).normalized() for v in axes]

def dodeca(rr):
    s = None
    for n in axes:
        c = cq.Solid.makeCylinder(200, 2 * rr, n * (-rr), n)
        s = c if s is None else s.intersect(c)
    return s

outer = dodeca(r_in)
inner = dodeca(r_in - 3.0)
body = outer.cut(inner)

hole_r = r_face - 3.5
for n in axes:
    h = cq.Solid.makeCylinder(hole_r, 4 * R, n * (-2 * R), n)
    body = body.cut(h)

result = cq.Workplane("XY").add(body)
