import cadquery as cq
import math

P0 = (0.0, 0.0, 0.0)
P1 = (0.0, 0.0, 60.0)
P2 = (60.0, 0.0, 60.0)
P3 = (60.0, 0.0, 120.0)

def bez(t):
    u = 1 - t
    return tuple(u**3*P0[i] + 3*u*u*t*P1[i] + 3*u*t*t*P2[i] + t**3*P3[i] for i in range(3))

def tan(t):
    u = 1 - t
    return tuple(3*(u*u*(P1[i]-P0[i]) + 2*u*t*(P2[i]-P1[i]) + t*t*(P3[i]-P2[i])) for i in range(3))

def make_plane(t):
    o = bez(t)
    if t >= 1.0:
        th = math.radians(45)
    else:
        tx, _, tz = tan(t)
        th = math.atan2(tx, tz)
    n = (math.sin(th), 0, math.cos(th))
    xd = (math.cos(th), 0, -math.sin(th))
    return cq.Plane(origin=o, xDir=xd, normal=n)

def radii(t):
    s = t * t * (3 - 2 * t)
    return 60 + (30 - 60) * s, 40 + (30 - 40) * s

def loft_solid(offset):
    wires = []
    N = 8
    for i in range(N + 1):
        t = i / N
        a, b = radii(t)
        a -= offset
        b -= offset
        w = cq.Workplane(make_plane(t)).ellipse(a, b).val()
        wires.append(w)
    return cq.Solid.makeLoft(wires, False)

outer = cq.Workplane("XY").add(loft_solid(0))
inner = cq.Workplane("XY").add(loft_solid(3))

# flange lip at the tilted top port (5 wide, 2 thick, extending back along the pipe)
top_plane = make_plane(1.0)
flange = cq.Workplane(top_plane).circle(35).extrude(-2)
outer = outer.union(flange)

# extensions of the bore to guarantee open ends
bot_plane = make_plane(0.0)
bot_ext = cq.Workplane(bot_plane).ellipse(57, 37).extrude(-2)
top_ext = cq.Workplane(top_plane).circle(27).extrude(2)
inner = inner.union(bot_ext).union(top_ext)

result = outer.cut(inner)
