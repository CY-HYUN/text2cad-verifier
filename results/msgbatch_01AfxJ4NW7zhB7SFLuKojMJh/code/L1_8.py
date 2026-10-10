import cadquery as cq
import math

# Rectangular block 80 x 80 x 40, centered in XY, base at z=0, top at z=40
body = cq.Workplane("XY").box(80, 80, 40, centered=(True, True, False))

# Sphere of radius 20 centered on the top surface; its lower half is the hemispherical pit
sphere = cq.Workplane("XY").workplane(offset=40).sphere(20)

result = body.cut(sphere)
