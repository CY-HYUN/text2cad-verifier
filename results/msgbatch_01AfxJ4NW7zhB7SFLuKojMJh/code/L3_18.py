import cadquery as cq
import math

def ellipsoid(a, c):
    return (cq.Workplane("XZ")
            .ellipseArc(a, c, -90, 90, startAtCurrent=False)
            .close()
            .revolve(360, (0, 0, 0), (0, 1, 0)))

outer = ellipsoid(40, 60)
inner = ellipsoid(37, 57)
shell = outer.cut(inner)

# lattice mask: 12 meridian ribs + 3 rings
mask = None
for k in range(12):
    rib = (cq.Workplane("XY")
           .box(60, 4, 140, centered=(False, True, True))
           .rotate((0, 0, 0), (0, 0, 1), k * 30))
    mask = rib if mask is None else mask.union(rib)

for z in (-30, 0, 30):
    ring = cq.Workplane("XY").box(200, 200, 4).translate((0, 0, z))
    mask = mask.union(ring)

lattice = shell.intersect(mask)

# top wiring hole
hole = cq.Workplane("XY").circle(5).extrude(80)
lattice = lattice.cut(hole)

# cut off bottom below z=-50
bottom = cq.Workplane("XY").box(200, 200, 100, centered=(True, True, False)).translate((0, 0, -150))
lattice = lattice.cut(bottom)

result = lattice
