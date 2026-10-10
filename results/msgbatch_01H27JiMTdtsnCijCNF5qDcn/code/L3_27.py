import cadquery as cq
import math

# Base block with heavily rounded corners
body = cq.Workplane("XY").box(60, 60, 60).edges().fillet(15)

def cyl(d, z0, z1):
    return cq.Workplane("XY").workplane(offset=z0).circle(d / 2).extrude(z1 - z0)

# Solid branch along +Z (top pipe with square flange)
def top_solid():
    p = cyl(40, 0, 60)
    fl = cq.Workplane("XY").workplane(offset=50).rect(60, 60).extrude(10)
    return p.union(fl)

def top_cut():
    c = cyl(24, 0, 61)
    for sx in (-22, 22):
        for sy in (-22, 22):
            c = c.union(cq.Workplane("XY").workplane(offset=48)
                        .center(sx, sy).circle(3.2).extrude(13))
    return c

# Side branch along +Z (circular flange)
def side_solid():
    p = cyl(30, 0, 55)
    fl = cyl(50, 47, 55)
    return p.union(fl)

def side_cut():
    c = cyl(18, 0, 56)
    r = 20
    for i in range(4):
        a = math.radians(45 + 90 * i)
        c = c.union(cq.Workplane("XY").workplane(offset=45)
                    .center(r * math.cos(a), r * math.sin(a))
                    .circle(2.7).extrude(11))
    return c

# Orientations mapping +Z to six directions
def orient(w, k):
    if k == 0:
        return w
    if k == 1:
        return w.rotate((0, 0, 0), (1, 0, 0), 180)
    if k == 2:
        return w.rotate((0, 0, 0), (0, 1, 0), 90)
    if k == 3:
        return w.rotate((0, 0, 0), (0, 1, 0), -90)
    if k == 4:
        return w.rotate((0, 0, 0), (1, 0, 0), -90)
    return w.rotate((0, 0, 0), (1, 0, 0), 90)

solids = [(top_solid, 0), (top_solid, 1)] + [(side_solid, k) for k in (2, 3, 4, 5)]
for f, k in solids:
    body = body.union(orient(f(), k))

# Triangular reinforcement plates around top and bottom pipes
rib_pts = [(16, 26), (29, 26), (16, 48)]
rib = cq.Workplane("XZ").polyline(rib_pts).close().extrude(2, both=True)
for zi in range(2):
    for a in (0, 90, 180, 270):
        r = rib.rotate((0, 0, 0), (0, 0, 1), a)
        if zi:
            r = r.mirror("XY")
        body = body.union(r)

# Central spherical cavity
body = body.cut(cq.Workplane("XY").sphere(20))

# Flow bores and bolt holes
cuts = [(top_cut, 0), (top_cut, 1)] + [(side_cut, k) for k in (2, 3, 4, 5)]
for f, k in cuts:
    body = body.cut(orient(f(), k))

result = body
