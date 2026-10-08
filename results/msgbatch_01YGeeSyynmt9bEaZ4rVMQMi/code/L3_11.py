import cadquery as cq
import math

P0 = (0.0, 0.0, 0.0)
P1 = (0.0, 0.0, 60.0)
P2 = (60.0, 0.0, 60.0)
P3 = (60.0, 0.0, 120.0)

def bez(t):
    u = 1 - t
    c = (u**3, 3*u*u*t, 3*u*t*t, t**3)
    return tuple(sum(c[i]*[P0, P1, P2, P3][i][k] for i in range(4)) for k in range(3))

def tan(t):
    u = 1 - t
    d = [3*u*u*(P1[k]-P0[k]) + 6*u*t*(P2[k]-P1[k]) + 3*t*t*(P3[k]-P2[k]) for k in range(3)]
    L = math.sqrt(sum(x*x for x in d))
    return tuple(x/L for x in d)

def section(t, a, b, shift=0.0):
    p = bez(t)
    n = tan(t)
    c = cq.Vector(*p) + cq.Vector(*n) * shift
    nv = cq.Vector(*n)
    xd = cq.Vector(n[2], 0, -n[0])
    if abs(a - b) < 1e-6:
        return cq.Wire.makeCircle(a, c, nv)
    return cq.Wire.makeEllipse(a, b, c, nv, xd)

ts = [i / 6.0 for i in range(7)]

def radii(t, off):
    a = 60.0 + (30.0 - 60.0) * t - off
    b = 40.0 + (30.0 - 40.0) * t - off
    if t > 0.999:
        b = a
    return a, b

outer_wires = [section(t, *radii(t, 0.0)) for t in ts]
outer = cq.Solid.makeLoft(outer_wires)

inner_wires = []
a0, b0 = radii(0.0, 3.0)
inner_wires.append(section(0.0, a0, b0, shift=-1.0))
for t in ts[1:-1]:
    inner_wires.append(section(t, *radii(t, 3.0)))
a1, b1 = radii(1.0, 3.0)
inner_wires.append(section(1.0, a1, a1, shift=1.0))
inner = cq.Solid.makeLoft(inner_wires)

body = cq.Workplane("XY").add(outer).cut(cq.Workplane("XY").add(inner))

# Top flange: ring from inner hole (dia 54) to dia 70, 2 mm outward along tangent
pt = bez(1.0)
nt = tan(1.0)
top_plane = cq.Plane(origin=pt, xDir=(nt[2], 0, -nt[0]), normal=nt)
flange = (
    cq.Workplane(top_plane)
    .circle(35.0)
    .circle(27.0)
    .extrude(2.0)
)

result = body.union(flange)
