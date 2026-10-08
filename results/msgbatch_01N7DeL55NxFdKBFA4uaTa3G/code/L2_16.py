import cadquery as cq
import math

R = 25.0          # sphere radius
rc = 15.0         # boss cylinder radius
L = 20.0          # boss length
rh = 10.0         # through-hole radius
rp = 10.0         # top platform radius

# Sphere by revolving a half-circle profile
sphere = (cq.Workplane("XZ")
          .moveTo(0, -R)
          .threePointArc((R, 0), (0, R))
          .close()
          .revolve(360, (0, 0, 0), (0, 1, 0)))

body = sphere

# Start of bosses where cylinder radius meets the sphere surface
x0 = math.sqrt(R**2 - rc**2)

for d in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0)]:
    cyl = cq.Solid.makeCylinder(rc, L + x0,
                                cq.Vector(0, 0, 0),
                                cq.Vector(*d))
    body = body.union(cq.Workplane().add(cyl))

# Through holes along X and Y
span = 2 * (x0 + L) + 10
hx = cq.Solid.makeCylinder(rh, span, cq.Vector(-span / 2, 0, 0), cq.Vector(1, 0, 0))
hy = cq.Solid.makeCylinder(rh, span, cq.Vector(0, -span / 2, 0), cq.Vector(0, 1, 0))
body = body.cut(cq.Workplane().add(hx)).cut(cq.Workplane().add(hy))

# Flat circular platform on top, diameter 20
zc = math.sqrt(R**2 - rp**2)
cutter = cq.Workplane("XY").workplane(offset=zc).rect(100, 100).extrude(R)
body = body.cut(cutter)

result = body
