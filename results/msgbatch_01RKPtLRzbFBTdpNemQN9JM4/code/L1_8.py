import cadquery as cq
import math

# Main block: 80 x 80 x 40, centered in XY, base at z=0, top at z=40
body = cq.Workplane("XY").box(80, 80, 40, centered=(True, True, False))

# Sphere of radius 20 centered at the top surface center; the lower half cuts a hemispherical pit
sphere = cq.Workplane("XY").sphere(20).translate((0, 0, 40))

result = body.cut(sphere)
