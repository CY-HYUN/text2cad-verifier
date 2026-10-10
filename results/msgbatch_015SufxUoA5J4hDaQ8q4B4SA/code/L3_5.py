import cadquery as cq
import math

R = 100.0
t = 10.0
h_cyl = 50.0
dome_h = 50.0   # semi-minor axis: cylinder 50 + dome 50 = 100 total head depth

def solid(a, b, z_start):
    prof = (cq.Workplane("XZ")
            .moveTo(0, z_start)
            .lineTo(a, z_start)
            .lineTo(a, h_cyl)
            .ellipseArc(a, b, 0, 90)
            .close())
    return prof.revolve(360, (0, 0, 0), (0, 1, 0))

outer = solid(R, dome_h, 0)
inner = solid(R - t, dome_h - t, -1)
shell = outer.cut(inner)

apex = h_cyl + dome_h  # 100
nozzle = (cq.Workplane("XY").workplane(offset=apex - 10)
          .circle(20).extrude(40))  # top at z = 130
result = shell.union(nozzle)
bore = (cq.Workplane("XY").workplane(offset=apex - 15)
        .circle(15).extrude(50))
result = result.cut(bore)
