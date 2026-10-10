import cadquery as cq
import math

# Base block: 60 mm cube with corners rounded by intersecting with a sphere
block = cq.Workplane("XY").box(60, 60, 60)
block = block.intersect(cq.Workplane("XY").sphere(42))

def make_port(kind):
    # Built along +Z, starting inside the block
    if kind == "main":
        pipe = cq.Workplane("XY").workplane(offset=25).circle(20).extrude(35)
        fl = (cq.Workplane("XY").workplane(offset=54)
              .rect(60, 60).extrude(6))
        bore = cq.Workplane("XY").circle(12).extrude(61)
        pts = [(22, 22), (-22, 22), (22, -22), (-22, -22)]
        holes = (cq.Workplane("XY").workplane(offset=50)
                 .pushPoints(pts).circle(3.2).extrude(12))
    else:
        pipe = cq.Workplane("XY").workplane(offset=25).circle(15).extrude(30)
        fl = (cq.Workplane("XY").workplane(offset=50)
              .circle(25).extrude(5))
        bore = cq.Workplane("XY").circle(9).extrude(56)
        r = 19
        pts = [(r, 0), (-r, 0), (0, r), (0, -r)]
        holes = (cq.Workplane("XY").workplane(offset=46)
                 .pushPoints(pts).circle(2.7).extrude(12))
    return pipe.union(fl), bore.union(holes)

body = block
cutters = cq.Workplane("XY").sphere(20)

def place(shape, kind_dir):
    axis, ang = kind_dir
    if axis is None:
        return shape
    return shape.rotate((0, 0, 0), axis, ang)

orients_main = [(None, 0), ((1, 0, 0), 180)]
orients_side = [((0, 1, 0), 90), ((0, 1, 0), -90),
                ((1, 0, 0), -90), ((1, 0, 0), 90)]

for o in orients_main:
    s, c = make_port("main")
    body = body.union(place(s, o))
    cutters = cutters.union(place(c, o))
for o in orients_side:
    s, c = make_port("side")
    body = body.union(place(s, o))
    cutters = cutters.union(place(c, o))

# Triangular ribs at top and bottom pipe/block junctions
rib = (cq.Workplane("XZ").polyline([(19, 30), (30, 30), (19, 46)]).close()
       .extrude(2, both=True))
for i in range(4):
    r = rib.rotate((0, 0, 0), (0, 0, 1), 90 * i)
    body = body.union(r)
    body = body.union(r.mirror("XY"))

result = body.cut(cutters)
