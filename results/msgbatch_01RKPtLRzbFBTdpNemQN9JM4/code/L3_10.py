import cadquery as cq
import math

# Outer profile: inner parabola z = r^2/80 offset by 5 mm along its normal
pts_out = []
N = 40
for i in range(N + 1):
    r = 80.0 * i / N
    z = r * r / 80.0
    s = r / 40.0
    L = math.sqrt(1 + s * s)
    pts_out.append((r + 5 * s / L, z - 5 / L))

outer_pts = pts_out + [(85.0, pts_out[-1][1]), (85.0, 80.0), (0, 80.0)]
outer = (cq.Workplane("XZ").polyline(outer_pts).close()
         .revolve(360, (0, 0, 0), (0, 1, 0)))

# Flange ring
flange = (cq.Workplane("XY").workplane(offset=75)
          .circle(85).circle(78).extrude(5))
body = outer.union(flange)

# Inner paraboloid cavity
inner_pts = [(80.0 * i / N, (80.0 * i / N) ** 2 / 80.0) for i in range(N + 1)]
inner_pts += [(0, 80.0 + 1)]
inner_pts[-2] = (80.0, 80.0)
cavity_pts = inner_pts[:-1] + [(80.0, 81.0), (0, 81.0)]
cavity = (cq.Workplane("XZ").polyline(cavity_pts).close()
          .revolve(360, (0, 0, 0), (0, 1, 0)))
body = body.cut(cavity)

# Central through hole dia 10
hole = cq.Workplane("XY").workplane(offset=-10).circle(5).extrude(30)
body = body.cut(hole)

# Four mounting holes dia 5 on flange, one on +Y
mh = (cq.Workplane("XY").workplane(offset=70)
      .polarArray(82.5, 90, 360, 4).circle(2.5).extrude(15))
body = body.cut(mh)

result = body
