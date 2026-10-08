import cadquery as cq
import math

# ---------------- Inner flow path ----------------
# Arc from inlet (-20,15) to throat (0,5), tangent horizontal at throat
# Circle centre (0,30), R=25 -> intermediate point at x=-10
R = 25.0
mid_arc = (-10.0, 30.0 - math.sqrt(R**2 - 10.0**2))

# Parabola y = 5 + k x^2 through (80,25)
k = 20.0 / 80.0**2
para_pts = [(x, 5.0 + k * x * x) for x in [10, 20, 30, 40, 50, 60, 70, 80]]

# ---------------- Outer profile (thickest at throat) ----------------
outer_pts_rev = [(40.0, 21.0), (0.0, 17.0), (-20.0, 20.0)]  # from outlet back to inlet

profile = (
    cq.Workplane("XY")
    .moveTo(-20.0, 15.0)
    .threePointArc(mid_arc, (0.0, 5.0))
    .spline(para_pts, tangents=[(1, 0), (1, 2 * k * 80.0)], includeCurrent=True)
    .lineTo(80.0, 30.0)
    .spline(outer_pts_rev, includeCurrent=True)
    .close()
)

nozzle = profile.revolve(360.0, (0, 0, 0), (1, 0, 0))

# ---------------- Flanges ----------------
flange_t = 6.0
inlet_flange = (
    cq.Workplane("YZ").workplane(offset=-20.0 - flange_t)
    .circle(35.0).circle(15.0).extrude(flange_t)
)
outlet_flange = (
    cq.Workplane("YZ").workplane(offset=80.0)
    .circle(45.0).circle(25.0).extrude(flange_t)
)

result = nozzle.union(inlet_flange).union(outlet_flange)
