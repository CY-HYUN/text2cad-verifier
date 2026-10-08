import cadquery as cq
import math

a, b = 40.0, 60.0      # semi-minor (X), semi-major (Y)
t = 3.0                # rib radial thickness
w = 4.0                # rib width
n_ribs = 12

def half_ellipse_solid(ra, rb):
    return (cq.Workplane("XY")
            .moveTo(0, -rb)
            .ellipseArc(ra, rb, angle1=-90, angle2=90)
            .close()
            .revolve(360, (0, 0, 0), (0, 1, 0)))

# Reference ellipsoid shell (outer minus inner)
outer = half_ellipse_solid(a, b)
inner = half_ellipse_solid(a - t, b - t)
shell = outer.cut(inner)

# Meridional ribs: each slab through the Y axis yields two opposite ribs
ribs = None
for i in range(n_ribs // 2):
    ang = i * 360.0 / n_ribs
    slab = (cq.Workplane("XY").box(w, 2.5 * b, 2.5 * b)
            .rotate((0, 0, 0), (0, 1, 0), ang))
    rib = shell.intersect(slab)
    ribs = rib if ribs is None else ribs.union(rib)

result = ribs

# Latitudinal rings at Y = 30, 0, -30
for y in (30.0, 0.0, -30.0):
    r = a * math.sqrt(1 - (y / b) ** 2)
    ring = (cq.Workplane("XZ", origin=(0, y, 0))
            .circle(r).circle(r - 1.5)
            .extrude(2.0, both=True))
    result = result.union(ring)

# Top through-hole
hole = cq.Workplane(obj=cq.Solid.makeCylinder(
    6.0, 40.0, cq.Vector(0, 35, 0), cq.Vector(0, 1, 0)))
result = result.cut(hole)
