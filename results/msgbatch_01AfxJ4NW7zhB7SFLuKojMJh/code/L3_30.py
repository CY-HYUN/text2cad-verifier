import cadquery as cq
import math

L, W, H = 150.0, 100.0, 30.0

# Base block
base = cq.Workplane("XY").box(L, W, H, centered=(True, True, False))

# Dovetail rail along X (profile in YZ plane)
rh = 15.0
bw = 60.0
off = rh / math.tan(math.radians(60))
rail_pts = [(-bw/2, H), (bw/2, H), (bw/2 + off, H + rh), (-bw/2 - off, H + rh)]
rail = cq.Workplane("YZ").polyline(rail_pts).close().extrude(L/2, both=True)
body = base.union(rail)

# T-slots on both side faces, running full length
def tslot(sign):
    pts = [(51, 10), (46, 10), (46, 7), (42, 7), (42, 23), (46, 23), (46, 20), (51, 20)]
    pts = [(sign*y, z) for y, z in pts]
    return cq.Workplane("YZ").polyline(pts).close().extrude(L/2 + 1, both=True)

body = body.cut(tslot(1)).cut(tslot(-1))

# Central counterbored hole from rail top
top = H + rh
body = (body.faces(">Z").workplane(centerOption="CenterOfBoundBox")
        .center(0, 0).cboreHole(30.0, 40.0, 5.0))

# Corner countersunk mounting holes from base top
for sx in (-1, 1):
    for sy in (-1, 1):
        csk = (cq.Workplane("XY").workplane(offset=H)
               .center(sx*65, sy*40)
               .circle(4.0).extrude(-H))
        cone = cq.Solid.makeCone(4.0, 7.0, 3.0, pnt=cq.Vector(sx*65, sy*40, H-3), dir=cq.Vector(0, 0, 1))
        body = body.cut(csk).cut(cq.Workplane("XY").add(cone))

# Oil / relief grooves at rail root on both sides
for s in (-1, 1):
    g = (cq.Workplane("XY")
         .box(L, 2.0, 1.0, centered=(True, True, False))
         .translate((0, s*(bw/2 + 1.0), H - 1.0)))
    body = body.cut(g)

result = body
