import cadquery as cq
import math

R = 100.0
T = 10.0
H_cyl = 50.0
B = 50.0  # semi-minor axis (2:1 head)

def head_solid(r, b, h):
    cyl = cq.Workplane("XY").circle(r).extrude(h)
    ell = (cq.Workplane("XZ").center(0, h).ellipse(r, b)
           .revolve(360, (0, 0, 0), (0, 1, 0)))
    box = cq.Workplane("XY").workplane(offset=h).rect(4*r, 4*r).extrude(b + 1)
    dome = ell.intersect(box)
    return cyl.union(dome)

outer = head_solid(R, B, H_cyl)
inner = head_solid(R - T, B - T, H_cyl)
shell = outer.cut(inner)

apex = H_cyl + B
nozzle = (cq.Workplane("XY").workplane(offset=apex - 5)
          .circle(20).extrude(30 + 5))
shell = shell.union(nozzle)
bore = (cq.Workplane("XY").workplane(offset=apex - 30)
        .circle(15).extrude(70))
result = shell.cut(bore)
