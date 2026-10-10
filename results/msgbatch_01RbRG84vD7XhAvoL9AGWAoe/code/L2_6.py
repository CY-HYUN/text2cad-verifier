import cadquery as cq
import math

# Parameters
D = 30.0          # shaft diameter
L = 80.0          # shaft length
R = D / 2.0
pitch = 20.0
turns = 4
groove_r = 2.5    # semicircular groove radius (circle centered on surface)

# Base cylinder
shaft = cq.Workplane("XY").circle(R).extrude(L)

# Helical path on the cylinder surface
helix = cq.Wire.makeHelix(pitch, pitch * turns, R)

# Profile circle perpendicular to helix tangent at start point (R,0,0)
tangent = cq.Vector(0, 2 * math.pi * R, pitch)
plane = cq.Plane(origin=(R, 0, 0), xDir=(1, 0, 0), normal=tangent)
profile = cq.Workplane(plane).circle(groove_r)

# Sweep the circle along the helix (half of it lies inside the shaft -> semicircular groove)
groove = profile.sweep(cq.Workplane(obj=helix), isFrenet=True)

result = shaft.cut(groove)
