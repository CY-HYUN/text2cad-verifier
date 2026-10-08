import cadquery as cq
import math

P0 = (0.0, 0.0, 0.0)
P1 = (0.0, 0.0, 60.0)
P2 = (60.0, 0.0, 60.0)
P3 = (60.0, 0.0, 120.0)

def bez(t):
    u = 1 - t
    return tuple(u**3*P0[i] + 3*u*u*t*P1[i] + 3*u*t*t*P2[i] + t**3*P3[i] for i in range(3))

def bez_d(t):
    u = 1 - t
    return tuple(3*u*u*(P1[i]-P0[i]) + 6*u*t*(P2[i]-P1[i]) + 3*t*t*(P3[i]-P2[i]) for i in range(3))

def tilt(t):
    # tilt angle (about Y) of section plane: follows tangent in first half, 45 deg at the top
    d = bez_d(t)
    a = math.atan2(d[0], d[2])
    if t >= 0.5:
        a = math.radians(45.0)
    return a

def smooth(t):
    return t*t*(3 - 2*t)

def section(origin, a, rx, ry):
    xdir = cq.Vector(math.cos(a), 0, -math.sin(a))
    n = cq.Vector(math.sin(a), 0, math.cos(a))
    pl = cq.Plane(origin=cq.Vector(*origin), xDir=xdir, normal=n)
    if abs(rx - ry) < 1e-6:
        return cq.Wire.makeCircle(rx, pl.origin, n)
    return cq.Workplane(pl).ellipse(rx, ry).val()

ts = [i / 10.0 for i in range(11)]
wall = 3.0
outer, inner = [], []
for t in ts:
    s = smooth(t)
    rx = 60 + (30 - 60) * s
    ry = 40 + (30 - 40) * s
    p = bez(t)
    a = tilt(t)
    outer.append(section(p, a, rx, ry))
    inner.append(section(p, a, rx - wall, ry - wall))

# extend inner cutter slightly beyond both ends
a0 = tilt(0.0); a1 = tilt(1.0)
n0 = (math.sin(a0), 0, math.cos(a0))
n1 = (math.sin(a1), 0, math.cos(a1))
pre = tuple(P0[i] - 1.0 * n0[i] for i in range(3))
post = tuple(P3[i] + 1.0 * n1[i] for i in range(3))
inner = [section(pre, a0, 60 - wall, 40 - wall)] + inner + [section(post, a1, 30 - wall, 30 - wall)]

outer_solid = cq.Solid.makeLoft(outer, False)
inner_solid = cq.Solid.makeLoft(inner, False)

body = cq.Workplane("XY").add(outer_solid).cut(cq.Workplane("XY").add(inner_solid))

# flange lip at the top inclined port
top_plane = cq.Plane(origin=cq.Vector(*P3),
                     xDir=cq.Vector(math.cos(a1), 0, -math.sin(a1)),
                     normal=cq.Vector(*n1))
flange = cq.Workplane(top_plane).circle(35.0).circle(30.0 - wall).extrude(-2.0)

result = body.union(flange)
