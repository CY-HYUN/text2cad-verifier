import cadquery as cq
import math

# Inner paraboloid: z = r^2/80 (focal length 20), top at z=80 -> r=80
def inner_pts(n=40, rmax=80.0):
    return [(rmax * i / n, (rmax * i / n) ** 2 / 80.0) for i in range(n + 1)]

# Outer surface: inner paraboloid offset 5 mm downward (z = r^2/80 - 5)
def outer_pts(rmax, n=40):
    return [(rmax * i / n, (rmax * i / n) ** 2 / 80.0 - 5.0) for i in range(n + 1)]

# Outer body with flange (flange z 75..80, width 10 beyond shell top)
r_top_outer = math.sqrt(85 * 80.0)    # outer radius at z=80
r_at_75 = math.sqrt(80 * 80.0)        # outer radius at z=75 (80)
flange_r = r_top_outer + 10.0

outer = (
    cq.Workplane("XZ")
    .moveTo(0, -5)
    .spline(outer_pts(r_at_75)[1:], includeCurrent=True)
    .lineTo(flange_r, 75)
    .lineTo(flange_r, 80)
    .lineTo(0, 80)
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)

# Inner cavity
cavity = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .spline(inner_pts()[1:], includeCurrent=True)
    .lineTo(80, 81)
    .lineTo(0, 81)
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)

body = outer.cut(cavity)

# Central through hole, diameter 10
center_hole = cq.Workplane("XY").workplane(offset=-10).circle(5).extrude(30)
body = body.cut(center_hole)

# Four mounting holes dia 5 on flange, one on +Y
hole_r = r_top_outer + 5.0
pts = [(hole_r * math.cos(math.radians(a)), hole_r * math.sin(math.radians(a)))
       for a in (90, 180, 270, 0)]
holes = (
    cq.Workplane("XY").workplane(offset=70)
    .pushPoints(pts).circle(2.5).extrude(15)
)
body = body.cut(holes)

result = body
