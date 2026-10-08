import cadquery as cq

# Cube: 80 x 80 base on XY plane, extruded 40 mm upward (Z from 0 to 40)
cube = cq.Workplane("XY").rect(80.0, 80.0).extrude(40.0)

# Sphere cutter centered at the center of the top face (0, 0, 40)
sphere = cq.Workplane("XY").sphere(20.0).translate((0, 0, 40.0))

# Boolean difference -> hemispherical recess in the top face
result = cube.cut(sphere)
