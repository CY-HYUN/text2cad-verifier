import cadquery as cq

# Main block: 80 x 80 x 40, base on Z=0
body = cq.Workplane("XY").box(80, 80, 40, centered=(True, True, False))

# Sphere centred on the top face; the lower half cuts a hemispherical pit
sphere = cq.Workplane("XY").sphere(20).translate((0, 0, 40))

result = body.cut(sphere)
