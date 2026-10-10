import cadquery as cq
import math

a_out, c_out = 40.0, 60.0
t = 3.0
a_in, c_in = a_out - t, c_out - t

def ellipsoid(a, c):
    return (cq.Workplane("XZ")
            .ellipseArc(a, c, angle1=-90, angle2=90, sense=1, startAtCurrent=False)
            .close()
            .revolve(360, (0, 0, 0), (0, 1, 0)))

outer = ellipsoid(a_out, c_out)
inner = ellipsoid(a_in, c_in)
shell = outer.cut(inner)

# lattice generator: 12 ribs + 3 rings
lattice = None
for i in range(12):
    rib = (cq.Workplane("XY")
           .box(50, 4, 140, centered=(False, True, True))
           .rotate((0, 0, 0), (0, 0, 1), i * 30))
    lattice = rib if lattice is None else lattice.union(rib)

for z in (-30, 0, 30):
    ring = (cq.Workplane("XY").workplane(offset=z - 2)
            .circle(50).extrude(4))
    lattice = lattice.union(ring)

result = shell.intersect(lattice)

# top wiring hole, 10 mm diameter
hole = cq.Workplane("XY").workplane(offset=40).circle(5).extrude(40)
result = result.cut(hole)

# cut off the bottom below z = -50
bottom = cq.Workplane("XY").workplane(offset=-100).rect(200, 200).extrude(50)
result = result.cut(bottom)
