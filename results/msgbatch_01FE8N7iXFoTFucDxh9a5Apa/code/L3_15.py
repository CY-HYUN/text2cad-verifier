import cadquery as cq
import math

a_in, b_in = 100.0, 50.0      # inner semi-ellipse (2:1)
t = 8.0
a_out, b_out = a_in + t, b_in + t
h_str = 25.0

def ellipse_pts(a, b, n=40):
    pts = []
    for i in range(1, n):
        th = (math.pi / 2) * i / n
        pts.append((a * math.cos(th), b * math.sin(th)))
    return pts

def profile_solid(a, b):
    wp = (cq.Workplane("XZ")
          .moveTo(0, -h_str)
          .lineTo(a, -h_str)
          .lineTo(a, 0)
          .spline(ellipse_pts(a, b) + [(0, b)], includeCurrent=True)
          .close())
    return wp.revolve(360, (0, 0, 0), (0, 1, 0))

outer = profile_solid(a_out, b_out)
inner = profile_solid(a_in, b_in)
head = outer.cut(inner)

# Pressure gauge nozzle at vertex
nz_od, nz_id, nz_h = 40.0, 30.0, 30.0
nozzle = (cq.Workplane("XY").workplane(offset=b_in + 1)
          .circle(nz_od / 2).extrude(b_out + nz_h - (b_in + 1)))
head = head.union(nozzle)
hole = (cq.Workplane("XY").workplane(offset=b_in - 5)
        .circle(nz_id / 2).extrude(b_out + nz_h - b_in + 10))
result = head.cut(hole)
