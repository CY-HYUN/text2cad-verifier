import cadquery as cq
import math

# Base cube with filleted corners
body = cq.Workplane("XY").box(60, 60, 60).edges().fillet(12)

def z_branch_solid():
    cyl = cq.Workplane("XY").workplane(offset=30).circle(20).extrude(30)
    fl = cq.Workplane("XY").workplane(offset=50).rect(60, 60).extrude(10)
    return cyl.union(fl)

def side_branch_solid():
    cyl = cq.Workplane("XY").workplane(offset=30).circle(15).extrude(25)
    fl = cq.Workplane("XY").workplane(offset=47).circle(25).extrude(8)
    return cyl.union(fl)

def z_holes():
    b = cq.Workplane("XY").workplane(offset=-70).circle(10).extrude(140)
    pts = [(22, 22), (-22, 22), (22, -22), (-22, -22)]
    bolts = (cq.Workplane("XY").workplane(offset=45).pushPoints(pts)
             .circle(3.2).extrude(20))
    return b, bolts

def side_bolts():
    pts = [(19, 0), (-19, 0), (0, 19), (0, -19)]
    return (cq.Workplane("XY").workplane(offset=44).pushPoints(pts)
            .circle(2.6).extrude(14))

# Branches
top = z_branch_solid()
bottom = z_branch_solid().rotate((0, 0, 0), (1, 0, 0), 180)
body = body.union(top).union(bottom)

side = side_branch_solid()
for axis, ang in [((0, 1, 0), 90), ((0, 1, 0), -90), ((1, 0, 0), -90), ((1, 0, 0), 90)]:
    body = body.union(side.rotate((0, 0, 0), axis, ang))

# Triangular reinforcement ribs (4 top, 4 bottom) at diagonal corners
rib = (cq.Workplane("XZ")
       .polyline([(15, 26), (28, 26), (15, 48)]).close()
       .extrude(3, both=True))
for k in range(4):
    r = rib.rotate((0, 0, 0), (0, 0, 1), 45 + 90 * k)
    body = body.union(r)
    body = body.union(r.rotate((0, 0, 0), (1, 0, 0), 180))

# Central spherical cavity
body = body.cut(cq.Workplane("XY").sphere(20))

# Through bores and bolt holes
bore, zb = z_holes()
body = body.cut(bore)
body = body.cut(zb)
body = body.cut(zb.rotate((0, 0, 0), (1, 0, 0), 180))

bore_x = cq.Workplane("YZ").workplane(offset=-70).circle(10).extrude(140)
bore_y = cq.Workplane("XZ").workplane(offset=-70).circle(10).extrude(140)
body = body.cut(bore_x).cut(bore_y)

sb = side_bolts()
for axis, ang in [((0, 1, 0), 90), ((0, 1, 0), -90), ((1, 0, 0), -90), ((1, 0, 0), 90)]:
    body = body.cut(sb.rotate((0, 0, 0), axis, ang))

result = body
