import cadquery as cq
import math

# Bezier guide curve
P0 = cq.Vector(0, 0, 0)
P1 = cq.Vector(0, 0, 60)
P2 = cq.Vector(60, 0, 60)
P3 = cq.Vector(60, 0, 120)

def bez(t):
    u = 1 - t
    return (P0 * (u**3) + P1 * (3 * u * u * t) + P2 * (3 * u * t * t) + P3 * (t**3))

def tan(t):
    u = 1 - t
    d = (P1 - P0) * (3 * u * u) + (P2 - P1) * (6 * u * t) + (P3 - P2) * (3 * t * t)
    return d.normalized()

n_top = cq.Vector(math.sin(math.radians(45)), 0, math.cos(math.radians(45)))

def frame(t):
    c = bez(t)
    n = (tan(t) * (1 - t) + n_top * t).normalized()
    x = cq.Vector(1, 0, 0)
    x = (x - n * x.dot(n)).normalized()
    return c, n, x

def section(t, off):
    s = t * t * (3 - 2 * t)
    a = 60 + (30 - 60) * s - off
    b = 40 + (30 - 40) * s - off
    c, n, x = frame(t)
    return cq.Wire.makeEllipse(a, b, c, n, x)

ts = [i / 6 for i in range(7)]
outer = cq.Solid.makeLoft([section(t, 0) for t in ts])
inner = cq.Solid.makeLoft([section(t, 3) for t in ts])

body = cq.Workplane("XY").add(outer).cut(cq.Workplane("XY").add(inner))

# flange lip at the tilted top port
c, n, x = frame(1.0)
pl = cq.Plane(origin=(c.x, c.y, c.z), xDir=(x.x, x.y, x.z), normal=(n.x, n.y, n.z))
flange = cq.Workplane(pl).circle(35).circle(27).extrude(-2)

result = body.union(flange)
