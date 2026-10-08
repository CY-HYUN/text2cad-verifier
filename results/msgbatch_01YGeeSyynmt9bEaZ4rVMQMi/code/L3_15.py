import cadquery as cq
import math

# Ellipse parameters
a_o, b_o = 100.0, 50.0   # outer semi-axes
t = 8.0
a_i, b_i = a_o - t, b_o - t  # inner semi-axes (offset inward)
flange = 25.0

N = 24
outer_pts = [(a_o * math.sin(th), b_o * math.cos(th))
             for th in [i * (math.pi / 2) / N for i in range(N + 1)]]
inner_pts = [(a_i * math.sin(th), b_i * math.cos(th))
             for th in [i * (math.pi / 2) / N for i in range(N + 1)]][::-1]

profile = (
    cq.Workplane("XZ")
    .moveTo(0, b_o)
    .spline(outer_pts[1:], includeCurrent=True)
    .lineTo(a_o, -flange)
    .lineTo(a_i, -flange)
    .lineTo(a_i, 0)
    .spline(inner_pts[1:], includeCurrent=True)
    .close()
)

head = profile.revolve(360, (0, 0, 0), (0, 1, 0))

# Top nozzle: OD 40, ID 30, extends 30 mm above apex (z = 50)
nozzle_top = b_o + 30.0
nozzle_base = 45.0  # start inside the wall so it fuses with the curved shell
boss = (
    cq.Workplane("XY")
    .workplane(offset=nozzle_base)
    .circle(20.0)
    .extrude(nozzle_top - nozzle_base)
)
result = head.union(boss)

bore = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .circle(15.0)
    .extrude(nozzle_top + 1.0)
)
result = result.cut(bore)
