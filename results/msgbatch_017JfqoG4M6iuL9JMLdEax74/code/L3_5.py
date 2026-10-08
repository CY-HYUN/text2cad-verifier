import cadquery as cq
import math

R_out = 100.0
t = 10.0
H_flange = 50.0
b_out = 50.0  # 2:1 ellipsoidal head depth (D/4)

def half_ellipsoid(a, b, z0):
    prof = (cq.Workplane("XZ").moveTo(0, 0).lineTo(a, 0)
            .ellipseArc(a, b, 0, 90, startAtCurrent=True).close())
    return prof.revolve(360, (0, 0, 0), (0, 1, 0)).translate((0, 0, z0))

outer = (cq.Workplane("XY").circle(R_out).extrude(H_flange)
         .union(half_ellipsoid(R_out, b_out, H_flange)))
inner = (cq.Workplane("XY").workplane(offset=-1).circle(R_out - t).extrude(H_flange + 1)
         .union(half_ellipsoid(R_out - t, b_out - t, H_flange)))
head = outer.cut(inner)

apex = H_flange + b_out
nozzle_bottom = apex - 5
nozzle = (cq.Workplane("XY").workplane(offset=nozzle_bottom)
          .circle(20).extrude(apex + 30 - nozzle_bottom))
head = head.union(nozzle)
bore = (cq.Workplane("XY").workplane(offset=apex - 20)
        .circle(15).extrude(60))
result = head.cut(bore)
