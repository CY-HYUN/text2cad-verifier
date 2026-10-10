import cadquery as cq
import math

# Base block: 60 mm cube with rounded corners (intersected with a sphere)
cube = cq.Workplane("XY").box(60, 60, 60)
sph = cq.Workplane("XY").sphere(42)
body = cube.intersect(sph)

# Top port (along +Z): pipe OD40 to z=60, square flange 60x60x8
def top_port():
    pipe = cq.Workplane("XY").circle(20).extrude(60)
    fl = cq.Workplane("XY").workplane(offset=52).rect(60, 60).extrude(8)
    p = pipe.union(fl)
    holes = (cq.Workplane("XY").workplane(offset=50)
             .pushPoints([(22, 22), (-22, 22), (22, -22), (-22, -22)])
             .circle(3).extrude(12))
    return p.cut(holes)

# Side port (along +Z before rotation): pipe OD30 to z=55, round flange D50 x 6
def side_port():
    pipe = cq.Workplane("XY").circle(15).extrude(55)
    fl = cq.Workplane("XY").workplane(offset=49).circle(25).extrude(6)
    p = pipe.union(fl)
    d = 20 / math.sqrt(2)
    holes = (cq.Workplane("XY").workplane(offset=47)
             .pushPoints([(d, d), (-d, d), (d, -d), (-d, -d)])
             .circle(2.5).extrude(10))
    return p.cut(holes)

# Triangular ribs at the top pipe base
def ribs_top():
    r = None
    for a in (0, 90, 180, 270):
        rib = (cq.Workplane("XZ")
               .polyline([(18, 29), (29, 29), (18, 46)]).close()
               .extrude(2, both=True)
               .rotate((0, 0, 0), (0, 0, 1), a))
        r = rib if r is None else r.union(rib)
    return r

top = top_port()
rt = ribs_top()
top = top.union(rt)
bottom = top.rotate((0, 0, 0), (1, 0, 0), 180)

result = body.union(top).union(bottom)

sp = side_port()
for axis, ang in [((0, 1, 0), 90), ((0, 1, 0), -90), ((1, 0, 0), -90), ((1, 0, 0), 90)]:
    result = result.union(sp.rotate((0, 0, 0), axis, ang))

# Internal channels: spherical cavity D40 and bores
result = result.cut(cq.Workplane("XY").sphere(20))
result = result.cut(cq.Workplane("XY").circle(14).extrude(70, both=True))
result = result.cut(cq.Workplane("XY").circle(10).extrude(70, both=True)
                    .rotate((0, 0, 0), (1, 0, 0), 90))
result = result.cut(cq.Workplane("XY").circle(10).extrude(70, both=True)
                    .rotate((0, 0, 0), (0, 1, 0), 90))
