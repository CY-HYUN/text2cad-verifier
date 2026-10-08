import cadquery as cq
import math

# Outer profile: line (100,0)-(100,50), quarter ellipse center (0,50), a=100, b=50
# Inner profile: offset 10 mm inward (approximated as line + ellipse a=90, b=40)
N = 24
outer_pts = [(100 * math.cos(t), 50 + 50 * math.sin(t))
             for t in [i * (math.pi / 2) / N for i in range(N + 1)]]
inner_pts = [(90 * math.cos(t), 50 + 40 * math.sin(t))
             for t in [i * (math.pi / 2) / N for i in range(N + 1)]]
inner_pts_rev = list(reversed(inner_pts))  # from (0,90) to (90,50)

prof = (
    cq.Workplane("XY")
    .moveTo(90, 0)
    .lineTo(100, 0)
    .lineTo(100, 50)
    .spline(outer_pts[1:], tangents=[(0, 1), (-1, 0)], includeCurrent=True)
    .lineTo(0, 90)
    .spline(inner_pts_rev[1:], tangents=[(1, 0), (0, -1)], includeCurrent=True)
    .lineTo(90, 0)
    .close()
)

head = prof.revolve(360, (0, 0, 0), (0, 1, 0))

# Nozzle: ring OD40 / ID30, extruded 30 mm above the top vertex (y=100)
# Start slightly below to fuse with the curved shell.
outer_cyl = cq.Solid.makeCylinder(20, 35, cq.Vector(0, 95, 0), cq.Vector(0, 1, 0))
head = head.union(cq.Workplane("XY").add(outer_cyl))

# Bore through the nozzle into the head interior
bore = cq.Solid.makeCylinder(15, 50, cq.Vector(0, 82, 0), cq.Vector(0, 1, 0))
result = head.cut(cq.Workplane("XY").add(bore))
