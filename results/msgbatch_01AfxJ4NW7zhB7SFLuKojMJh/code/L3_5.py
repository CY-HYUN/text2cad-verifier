import cadquery as cq
import math

R = 100.0
t = 10.0
h_cyl = 50.0

def body(r, z0, z1):
    cyl = cq.Workplane("XY").workplane(offset=z0).circle(r).extrude(h_cyl - z0)
    sph = cq.Workplane("XY").sphere(r).translate((0, 0, h_cyl))
    b = cyl.union(sph)
    box = cq.Workplane("XY").box(400, 400, 400, centered=(True, True, False)).translate((0, 0, z0))
    return b.intersect(box)

outer = body(R, 0, 0)
inner = body(R - t, -1, 0)
shell = outer.cut(inner)

apex = h_cyl + R  # 150
nozzle = (cq.Workplane("XY").workplane(offset=apex - 10)
          .circle(20).extrude(40))  # to z=180 (30 above apex)
result = shell.union(nozzle)
bore = (cq.Workplane("XY").workplane(offset=apex - 30)
        .circle(15).extrude(80))
result = result.cut(bore)
