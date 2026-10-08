import cadquery as cq
import math

A = 40.0   # semi-minor (X)
B = 60.0   # semi-major (Y)
T = 3.0    # rib thickness (radial)
W = 4.0    # rib width (tangential)

def ellipsoid(a, b):
    return (cq.Workplane("XY")
            .ellipseArc(a, b, -90, 90, startAtCurrent=False)
            .close()
            .revolve(360, (0, 0, 0), (0, 1, 0)))

# Reference ellipsoidal shell (rib material envelope)
shell = ellipsoid(A, B).cut(ellipsoid(A - T, B - T))

# Single meridional rib: slab through Y axis intersected with the shell
slab = cq.Workplane("XY").box(A + 10, 2 * B + 20, W).translate(((A + 10) / 2, 0, 0))
rib = shell.intersect(slab)

# Circular pattern of 12 ribs about Y
ribs = rib
for i in range(1, 12):
    ribs = ribs.union(rib.rotate((0, 0, 0), (0, 1, 0), i * 30))

result = ribs

# Latitudinal rings at Y = 30, 0, -30
ring_h = 4.0
for y in (30.0, 0.0, -30.0):
    r_out = A * math.sqrt(1 - (y / B) ** 2)
    r_in = r_out - 1.5
    outer = cq.Solid.makeCylinder(r_out, ring_h, cq.Vector(0, y - ring_h / 2, 0), cq.Vector(0, 1, 0))
    inner = cq.Solid.makeCylinder(r_in, ring_h, cq.Vector(0, y - ring_h / 2, 0), cq.Vector(0, 1, 0))
    ring = cq.Workplane("XY").add(outer.cut(inner))
    result = result.union(ring)

# Top through-hole
hole = cq.Solid.makeCylinder(6.0, 40.0, cq.Vector(0, B - 25, 0), cq.Vector(0, 1, 0))
result = result.cut(cq.Workplane("XY").add(hole))
