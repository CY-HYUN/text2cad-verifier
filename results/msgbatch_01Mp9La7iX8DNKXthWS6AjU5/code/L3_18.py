import cadquery as cq
import math

a, b = 40.0, 60.0   # semi-minor (X), semi-major (Y)
t = 3.0             # rib radial thickness
w = 4.0             # rib width

# Meridional rib: shell between two ellipses (half profile), thickened symmetrically in Z
outer = cq.Workplane("XY").ellipse(a, b).extrude(w / 2, both=True)
inner = cq.Workplane("XY").ellipse(a - t, b - t).extrude(w / 2, both=True)
half_box = cq.Workplane("XY").box(a + 10, 2 * b + 20, 20, centered=(False, True, True))
rib = outer.cut(inner).intersect(half_box)

# Circular pattern of 12 ribs around the Y axis
ribs = rib
for i in range(1, 12):
    ribs = ribs.union(rib.rotate((0, 0, 0), (0, 1, 0), i * 30))

result = ribs

# Latitudinal rings at Y = 30, 0, -30
for y in (30.0, 0.0, -30.0):
    ro = a * math.sqrt(1 - (y / b) ** 2)
    ri = ro - t
    ring = (
        cq.Workplane("XZ")
        .workplane(offset=-y)
        .circle(ro)
        .circle(ri)
        .extrude(2.0, both=True)
    )
    result = result.union(ring)

# Top through-hole along Y
hole = cq.Workplane("XZ").workplane(offset=-35).circle(8).extrude(-35)
result = result.cut(hole)
