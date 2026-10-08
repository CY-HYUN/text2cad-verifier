import cadquery as cq
import math

def ellipsoid(a, c, n=60):
    # Half-ellipse profile closed along the vertical axis, revolved 360 degrees.
    pts = [(a * math.sin(math.pi * i / n), c * math.cos(math.pi * i / n)) for i in range(n + 1)]
    pts[0] = (0, c)
    pts[-1] = (0, -c)
    prof = (cq.Workplane("XZ")
            .moveTo(0, c)
            .spline(pts[1:], includeCurrent=True)
            .close())
    return prof.revolve(360, (0, 0, 0), (0, 1, 0))

outer = ellipsoid(40, 60)
inner = ellipsoid(37, 57)
shell = outer.cut(inner)

# Lattice pattern: 6 slabs through the centre give 12 ribs, plus 3 rings
pattern = None
for i in range(6):
    s = (cq.Workplane("XY").box(100, 4, 140)
         .rotate((0, 0, 0), (0, 0, 1), i * 30))
    pattern = s if pattern is None else pattern.union(s)
for z in (-30, 0, 30):
    ring = cq.Workplane("XY").box(100, 100, 4).translate((0, 0, z))
    pattern = pattern.union(ring)

lattice = shell.intersect(pattern)

# Top wiring hole
hole = cq.Workplane("XY").circle(5).extrude(40).translate((0, 0, 40))
lattice = lattice.cut(hole)

# Bottom opening: remove everything below z = -50
bottom = cq.Workplane("XY").box(120, 120, 40).translate((0, 0, -70))
lattice = lattice.cut(bottom)

result = lattice
