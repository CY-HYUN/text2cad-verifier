import cadquery as cq
import math

H = 80.0
n = 40

# outer solid profile: parabola shifted radially by 5 (outer radius 85 at the top)
outer_pts = [(5 + i * 80.0 / n, (i * 80.0 / n) ** 2 / 80.0) for i in range(n + 1)]
outer = (cq.Workplane("XZ").moveTo(0, 0).lineTo(5, 0)
         .spline(outer_pts[1:], includeCurrent=True)
         .lineTo(0, H).close()
         .revolve(360, (0, 0, 0), (0, 1, 0)))

# inner cavity: Z = R^2/80
inner_pts = [(i * 80.0 / n, (i * 80.0 / n) ** 2 / 80.0) for i in range(n + 1)]
inner = (cq.Workplane("XZ").moveTo(0, 0)
         .spline(inner_pts[1:], includeCurrent=True)
         .lineTo(0, H + 1).lineTo(0, H).close()
         .revolve(360, (0, 0, 0), (0, 1, 0)))

shell = outer.cut(inner)

# flange z 80..85, outer radius 95
flange = (cq.Workplane("XY").workplane(offset=H).circle(95).circle(80).extrude(5))
body = shell.union(flange)

# central light source hole, dia 10
hole = cq.Workplane("XY").workplane(offset=-1).circle(5).extrude(10)
body = body.cut(hole)

# 4 mounting holes dia 5 at radius 90, one on +Y
pts = [(90 * math.cos(math.radians(90 + 90 * k)), 90 * math.sin(math.radians(90 + 90 * k))) for k in range(4)]
mh = (cq.Workplane("XY").workplane(offset=H - 1).pushPoints(pts).circle(2.5).extrude(8))
body = body.cut(mh)

result = body
