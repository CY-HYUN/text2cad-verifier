import cadquery as cq
import math

# Main shaft
D = 30.0
L = 80.0
R = D / 2.0
cyl = cq.Workplane("XY").circle(R).extrude(L)

# Helical groove parameters
pitch = 20.0
groove_r = 2.5  # semicircular groove radius (circle centered on surface)

# Extend helix beyond both ends for a clean cut
ext = 10.0
h_total = L + 2 * ext
helix = cq.Wire.makeHelix(pitch=pitch, height=h_total, radius=R,
                          center=cq.Vector(0, 0, -ext))

# Profile plane normal to helix tangent at start point
start = cq.Vector(R, 0, -ext)
tangent = cq.Vector(0, 2 * math.pi * R, pitch).normalized()
plane = cq.Plane(origin=start, xDir=cq.Vector(1, 0, 0), normal=tangent)

groove = (
    cq.Workplane(plane)
    .circle(groove_r)
    .sweep(cq.Workplane(obj=helix), isFrenet=True)
)

result = cyl.cut(groove)
