import cadquery as cq
import math

P0 = (0.0, 0.0, 0.0)
P1 = (0.0, 0.0, 60.0)
P2 = (60.0, 0.0, 60.0)
P3 = (60.0, 0.0, 120.0)

def bez(t):
    u = 1 - t
    return tuple(u**3*P0[i] + 3*u*u*t*P1[i] + 3*u*t*t*P2[i] + t**3*P3[i] for i in range(3))

def dbez(t):
    u = 1 - t
    return tuple(3*(u*u*(P1[i]-P0[i]) + 2*u*t*(P2[i]-P1[i]) + t*t*(P3[i]-P2[i])) for i in range(3))

def norm(v):
    l = math.sqrt(sum(c*c for c in v))
    return tuple(c/l for c in v)

top_n = norm((math.sin(math.radians(45)), 0.0, math.cos(math.radians(45))))

ts = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]

def frame(t):
    c = bez(t)
    n = top_n if t >= 1.0 else norm(dbez(t))
    # xDir: global X projected perpendicular to n
    d = n[0]
    xd = norm((1 - d*n[0], -d*n[1], -d*n[2]))
    return c, n, xd

def section(t, off, shift=0.0):
    s = t*t*(3 - 2*t)
    a = 60.0 + (30.0 - 60.0)*s - off
    b = 40.0 + (30.0 - 40.0)*s - off
    c, n, xd = frame(t)
    cv = cq.Vector(*c) + cq.Vector(*n)*shift
    if abs(a - b) < 1e-6:
        return cq.Wire.makeCircle(a, cv, cq.Vector(*n))
    return cq.Wire.makeEllipse(a, b, cv, cq.Vector(*n), cq.Vector(*xd))

outer_wires = [section(t, 0.0) for t in ts]
outer = cq.Solid.makeLoft(outer_wires, False)

inner_wires = [section(0.0, 3.0, -3.0)] + [section(t, 3.0) for t in ts] + [section(1.0, 3.0, 3.0)]
inner = cq.Solid.makeLoft(inner_wires, False)

# Flange lip at top inclined port
c, n, xd = frame(1.0)
top_plane = cq.Plane(origin=cq.Vector(*c), xDir=cq.Vector(*xd), normal=cq.Vector(*n))
flange = cq.Workplane(top_plane).circle(35.0).circle(27.0).extrude(-2.0)

body = cq.Workplane("XY").add(outer).union(flange)
result = body.cut(cq.Workplane("XY").add(inner))
