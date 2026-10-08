import cadquery as cq
import math

# Cylinder: diameter 30, height 80
R = 15.0
H = 80.0
cylinder = cq.Workplane("XY").circle(R).extrude(H)

# Helix: pitch 20, 4 turns, on the cylinder surface (starts at end-face edge)
pitch = 20.0
turns = 4
helix = cq.Wire.makeHelix(pitch=pitch, height=pitch * turns, radius=R)

# Profile plane perpendicular to the helix at its start point (R, 0, 0)
r = 2.0
start = cq.Vector(R, 0, 0)
tangent = cq.Vector(0, 2 * math.pi * R, pitch).normalized()
plane = cq.Plane(origin=start, xDir=cq.Vector(1, 0, 0), normal=tangent)

# Circle centered on the cylinder surface: the half outside the cylinder removes
# nothing, so the cut equals a semicircular groove (flat on the surface, arc inward).
profile_wire = cq.Workplane(plane).circle(r).val()

groove = cq.Solid.sweep(profile_wire, [], helix, makeSolid=True, isFrenet=True)

result = cylinder.cut(cq.Workplane(obj=groove))
