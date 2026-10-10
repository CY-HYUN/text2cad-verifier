import cadquery as cq
import math

# Profile sketched on XZ plane (local x = X, local y = radius)
inner_spline_pts = [(x, 5 + x**2 / 320.0) for x in (0, 10, 20, 30, 40, 50, 60, 70, 80)]
inner_arc_mid = (-10, 30 - math.sqrt(625 - 100))

outer_pts = [(-20, 20), (-10, 23), (0, 24), (20, 24.8), (40, 26.5), (60, 28.3), (80, 30)]

# Wall solid (closed region between inner and outer profiles)
wall = (
    cq.Workplane("XZ")
    .moveTo(-20, 15)
    .threePointArc(inner_arc_mid, (0, 5))
    .spline(inner_spline_pts[1:], includeCurrent=True)
    .lineTo(80, 30)
    .spline(list(reversed(outer_pts))[1:], includeCurrent=True)
    .close()
    .revolve(360, (0, 0, 0), (1, 0, 0))
)

# Flanges (full disks, then bored by the flow path)
fl_in = (
    cq.Workplane("YZ").workplane(offset=-20).circle(32).extrude(6)
)
fl_out = (
    cq.Workplane("YZ").workplane(offset=74).circle(42).extrude(6)
)

# Flow-path solid for the bore
flow = (
    cq.Workplane("XZ")
    .moveTo(-20, 0)
    .lineTo(-20, 15)
    .threePointArc(inner_arc_mid, (0, 5))
    .spline(inner_spline_pts[1:], includeCurrent=True)
    .lineTo(80, 0)
    .close()
    .revolve(360, (0, 0, 0), (1, 0, 0))
)

result = wall.union(fl_in).union(fl_out).cut(flow)
