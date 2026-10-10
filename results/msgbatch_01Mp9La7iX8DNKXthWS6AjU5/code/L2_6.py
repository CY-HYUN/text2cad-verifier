import cadquery as cq
import math

R = 15.0
H = 80.0
pitch = 20.0

cyl = cq.Workplane("XY").circle(R).extrude(H)

helix = cq.Wire.makeHelix(pitch, H, R)

alpha = math.atan2(pitch, 2 * math.pi * R)
c, s = math.cos(alpha), math.sin(alpha)
t = cq.Vector(0, c, s)      # helix tangent at start (15,0,0)
w = cq.Vector(0, -s, c)     # in-plane direction along the cylinder surface, perpendicular to the tangent

plane = cq.Plane(origin=(R, 0, 0), xDir=w, normal=t)  # local y = +X (radial outward)

profile = (
    cq.Workplane(plane)
    .moveTo(-2, 0)
    .lineTo(2, 0)
    .threePointArc((0, -2), (-2, 0))  # arc toward the cylinder axis
    .close()
)

path = cq.Workplane("XY").newObject([helix])
groove = profile.sweep(path, isFrenet=True)

result = cyl.cut(groove)
