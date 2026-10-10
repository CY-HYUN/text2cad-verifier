import cadquery as cq
import math

radius = 15.0
length = 80.0
pitch = 20.0
groove_r = 2.0

# base shaft
shaft = cq.Workplane("XY").circle(radius).extrude(length)

# helical path on the cylinder surface (4 turns)
helix = cq.Wire.makeHelix(pitch, length, radius)
path = cq.Workplane("XY").newObject([helix])

# circular profile centred on the surface -> semicircular groove
profile = cq.Workplane("XZ", origin=(radius, 0, 0)).circle(groove_r)
groove = profile.sweep(path, isFrenet=True)

result = shaft.cut(groove)
