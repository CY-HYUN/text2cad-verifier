import cadquery as cq
import math

# Cylinder
R = 15.0
H = 80.0
cyl = cq.Workplane("XY").circle(R).extrude(H)

# Helix along cylinder surface
pitch = 20.0
turns = 4
helix = cq.Wire.makeHelix(pitch=pitch, height=pitch * turns, radius=R)

# Profile plane perpendicular to helix at its start point (R, 0, 0)
tangent = cq.Vector(0, R, pitch / (2 * math.pi)).normalized()
plane = cq.Plane(origin=(R, 0, 0), xDir=(1, 0, 0), normal=tangent)

# Semicircle r=2, straight edge on cylinder surface, arc inward (-local x).
# Small outward extension (outside the cylinder) for robust boolean.
r = 2.0
ext = 0.5
profile = (
    cq.Workplane(plane)
    .moveTo(ext, -r)
    .lineTo(0, -r)
    .threePointArc((-r, 0), (0, r))
    .lineTo(ext, r)
    .close()
)

groove = profile.sweep(cq.Workplane().add(helix), isFrenet=True)

result = cyl.cut(groove)
