import cadquery as cq
import math

def ellipsoid(a, b):
    # half-ellipse in XY plane (x>=0), revolved about Y axis
    return (cq.Workplane("XY")
            .ellipseArc(a, b, -90, 90, startAtCurrent=False)
            .close()
            .revolve(360, (0, 0, 0), (0, 1, 0)))

T = 3.0
outer = ellipsoid(40, 60)
inner = ellipsoid(40 - T, 60 - T)
shell = outer.cut(inner)

# single meridional rib: shell portion in a 4 mm wide slab on the XY plane (x>0)
slab = cq.Workplane("XY").box(60, 140, 4, centered=(False, True, True))
rib = shell.intersect(slab)

ribs = rib
for i in range(1, 12):
    ribs = ribs.union(rib.rotate((0, 0, 0), (0, 1, 0), 30 * i))

result = ribs

# latitudinal rings at Y = 30, 0, -30
for y in (30, 0, -30):
    ro = 40 * math.sqrt(1 - (y / 60.0) ** 2)
    ri = ro - T
    ring = (cq.Workplane("XZ").workplane(offset=-(y - 2))
            .circle(ro).circle(ri).extrude(-4))
    result = result.union(ring)

# top through-hole
hole = (cq.Workplane("XZ").workplane(offset=-35).circle(8).extrude(-40))
result = result.cut(hole)
