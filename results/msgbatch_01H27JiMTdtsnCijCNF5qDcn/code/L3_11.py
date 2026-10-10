import cadquery as cq
import math

# Bottom ellipse (120 x 80) on XY plane
w1 = cq.Workplane("XY").ellipse(60, 40).val()

# Tilted plane at the curve end point (normal at 45 deg to horizontal)
end = cq.Vector(60, 0, 120)
n = cq.Vector(1, 0, 1).normalized()
plane = cq.Plane(origin=(60, 0, 120), xDir=(1, 0, -1), normal=(n.x, n.y, n.z))

# Top circle, diameter 60
w2 = cq.Workplane(plane).circle(30).val()

# Loft between the two profiles
solid = cq.Solid.makeLoft([w1, w2])
body = cq.Workplane("XY").add(solid)

# Shell: remove planar end faces, 3 mm wall inward
shelled = body.faces("%PLANE").shell(-3.0)

# Top flange ring: outer dia 70, inner = hole edge (dia 54), 2 mm outward
flange = cq.Workplane(plane).circle(35).circle(27).extrude(2.0)

result = shelled.union(flange)
