import cadquery as cq

# Main body: 80 x 80 x 40, base on Z=0
body = cq.Workplane("XY").box(80, 80, 40, centered=(True, True, False))

# Hemispherical pit: sphere centred on the top face, so the rim is flush with it
sphere = cq.Workplane("XY").sphere(20).translate((0, 0, 40))

result = body.cut(sphere)
