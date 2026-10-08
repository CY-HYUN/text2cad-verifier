import cadquery as cq

# Cube 80 x 80 x 40, base on XY plane, centered in X/Y
cube = cq.Workplane("XY").rect(80.0, 80.0).extrude(40.0)

# Sphere of radius 20 centered at the center of the top face (0,0,40)
sphere = cq.Workplane("XY").sphere(20.0).translate((0, 0, 40.0))

# Difference -> hemispherical recess in the top surface
result = cube.cut(sphere)
