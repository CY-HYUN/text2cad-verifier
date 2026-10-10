import cadquery as cq
import math

# Ellipsoid parameters
a_out, c_out = 40.0, 60.0   # horizontal semi-axis, vertical semi-axis
t = 3.0
a_in, c_in = a_out - t, c_out - t

def ellipsoid(a, c):
    return (cq.Workplane("XZ")
            .ellipseArc(a, c, -90, 90, startAtCurrent=False)
            .close()
            .revolve(360, (0, 0, 0), (0, 1, 0)))

shell = ellipsoid(a_out, c_out).cut(ellipsoid(a_in, c_in))

# Lattice mask: 12 longitudinal ribs + 3 latitudinal rings
w = 4.0
mask = None
for i in range(12):
    rib = (cq.Workplane("XY")
           .box(50, w, 2 * c_out + 20)
           .translate((25, 0, 0))
           .rotate((0, 0, 0), (0, 0, 1), i * 30))
    mask = rib if mask is None else mask.union(rib)

for z in (-30.0, 0.0, 30.0):
    ring = cq.Workplane("XY").box(2 * a_out + 20, 2 * a_out + 20, w).translate((0, 0, z))
    mask = mask.union(ring)

lattice = shell.intersect(mask)

# Top wiring hole (10 mm dia)
hole = cq.Workplane("XY").circle(5).extrude(30).translate((0, 0, c_out - 20))
lattice = lattice.cut(hole)

# Bottom opening: cut everything below z = -50
bottom = cq.Workplane("XY").box(200, 200, 50).translate((0, 0, -50 - 25))
lattice = lattice.cut(bottom)

result = lattice
