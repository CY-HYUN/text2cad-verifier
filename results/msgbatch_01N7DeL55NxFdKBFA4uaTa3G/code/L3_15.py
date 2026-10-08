import cadquery as cq
import math

# Elliptical head parameters
a_out, b_out = 100.0, 50.0   # outer semi-axes (horizontal, vertical)
t = 8.0                      # wall thickness
a_in, b_in = a_out - t, b_out - t
flange = 25.0                # straight flange length

N = 24
outer_pts = [(a_out * math.sin(math.pi / 2 * i / N), b_out * math.cos(math.pi / 2 * i / N))
             for i in range(1, N + 1)]      # from near apex to (100,0)
inner_pts = [(a_in * math.cos(math.pi / 2 * i / N), b_in * math.sin(math.pi / 2 * i / N))
             for i in range(1, N + 1)]      # from near (92,0) to (0,42)
outer_pts[-1] = (a_out, 0.0)
inner_pts[-1] = (0.0, b_in)

profile = (
    cq.Workplane("XZ")
    .moveTo(0, b_out)
    .spline(outer_pts, tangents=[(1, 0), (0, -1)], includeCurrent=True)
    .lineTo(a_out, -flange)
    .lineTo(a_in, -flange)
    .lineTo(a_in, 0)
    .spline(inner_pts, tangents=[(0, 1), (-1, 0)], includeCurrent=True)
    .close()
)

head = profile.revolve(360, (0, 0, 0), (0, 1, 0))

# Top nozzle: ring OD40 / ID30, top 30 mm above apex, rooted into the wall
z_base = 44.0
z_top = b_out + 30.0
nozzle = (
    cq.Workplane("XY").workplane(offset=z_base)
    .circle(20.0).circle(15.0)
    .extrude(z_top - z_base)
)

result = head.union(nozzle)
