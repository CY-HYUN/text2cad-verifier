import cadquery as cq
import math

R = 15.0
H = 80.0
pitch = 20.0

cyl = cq.Workplane("XY").circle(R).extrude(H)

helix = cq.Wire.makeHelix(pitch, H, R)
path = cq.Workplane("XY").add(helix)

a = math.atan2(pitch, 2 * math.pi * R)
sa, ca = math.sin(a), math.cos(a)
plane = cq.Plane(origin=(R, 0, 0), xDir=(0, -sa, ca), normal=(0, ca, sa))

profile = (
    cq.Workplane(plane)
    .moveTo(-2, 0)
    .lineTo(2, 0)
    .threePointArc((0, -2), (-2, 0))
    .close()
)

groove = profile.sweep(path, isFrenet=True)

result = cyl.cut(groove)
