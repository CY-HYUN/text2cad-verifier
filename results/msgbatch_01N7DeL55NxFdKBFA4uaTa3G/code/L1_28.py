import cadquery as cq

# Cube: 60 mm square on XY, extruded 60 mm in +Z
cube = cq.Workplane("XY").rect(60.0, 60.0).extrude(60.0)

# Sphere diameter 61 mm at the cube's geometric center
sphere = cq.Workplane("XY").sphere(30.5).translate((0, 0, 30.0))

result = cube.cut(sphere)
