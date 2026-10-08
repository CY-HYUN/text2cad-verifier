import cadquery as cq
import math

# Outer profile: straight flange (100,0)->(100,50), then quarter ellipse a=100, b=50 centred at (0,50)
N = 40
outer_pts = [(100 * math.cos(t), 50 + 50 * math.sin(t))
             for t in [i * (math.pi / 2) / N for i in range(N + 1)]]
# Inner profile (offset 10 mm inward): x=90 straight, ellipse a=90, b=40
inner_pts = [(90 * math.cos(t), 50 + 40 * math.sin(t))
             for t in [i * (math.pi / 2) / N for i in range(N + 1)]]

prof = (cq.Workplane("XY")
        .moveTo(90, 0)
        .lineTo(100, 0)
        .lineTo(100, 50)
        .spline(outer_pts[1:], includeCurrent=True)
        .lineTo(0, 90)
        .spline(list(reversed(inner_pts[:-1])), includeCurrent=True)
        .close())

head = prof.revolve(360, (0, 0, 0), (0, 1, 0))

# Nozzle: ring OD40 / ID30, from tangent plane at top (y=100) extruded 30 mm outward,
# extended slightly downward to fuse with the curved shell
y0 = 95.0
h = 130.0 - y0
outer_c = cq.Solid.makeCylinder(20, h, cq.Vector(0, y0, 0), cq.Vector(0, 1, 0))
inner_c = cq.Solid.makeCylinder(15, h, cq.Vector(0, y0, 0), cq.Vector(0, 1, 0))
nozzle = cq.Workplane("XY").add(outer_c.cut(inner_c))

result = head.union(nozzle)
