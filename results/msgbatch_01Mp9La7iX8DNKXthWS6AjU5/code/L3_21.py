import cadquery as cq
import math

# Inner flow path: arc (tangent to axis direction at throat) then parabola
# arc center (0,30), R=25 -> passes (-20,15) and (0,5)
mid_arc = (-10.0, 30 - math.sqrt(25**2 - 10**2))

a = 20.0 / 6400.0
par_pts = [(x, 5 + a * x * x) for x in [10, 20, 30, 40, 50, 60, 70, 80]]

# Outer elliptical profile: center (80,10), semi-axes 115.47 (x), 20 (y)
ea = 100.0 / math.sqrt(0.75)
eb = 20.0
ell_pts = []
xs = [80, 70, 60, 50, 40, 30, 20, 10, 0, -10, -20]
for x in xs:
    y = 10 + eb * math.sqrt(max(0.0, 1 - ((x - 80) / ea) ** 2))
    ell_pts.append((x, y))
ell_pts[-1] = (-20, 20.0)  # exact inlet outer point (ellipse gives 20)

profile = (
    cq.Workplane("XZ")
    .moveTo(-20, 15)
    .threePointArc(mid_arc, (0, 5))
    .spline(par_pts, includeCurrent=True)
    .lineTo(80, 30)
    .spline(ell_pts[1:], includeCurrent=True)
    .close()
)

body = profile.revolve(360, (0, 0, 0), (1, 0, 0))

# Flanges (annular disks) on the end faces, extruded outward
fl_t = 8.0
fl_R = 35.0
inlet_flange = (
    cq.Workplane("YZ").workplane(offset=-20 - fl_t)
    .circle(fl_R).circle(15).extrude(fl_t)
)
outlet_flange = (
    cq.Workplane("YZ").workplane(offset=80)
    .circle(fl_R).circle(25).extrude(fl_t)
)

result = body.union(inlet_flange).union(outlet_flange)
