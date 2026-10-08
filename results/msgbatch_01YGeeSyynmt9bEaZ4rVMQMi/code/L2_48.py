import cadquery as cq

# 50 mm cube extruded from a square sketch, spanning (0,0,0) to (50,50,50)
cube = cq.Workplane("XY").rect(50, 50, centered=False).extrude(50)

# Sphere of radius 30 mm centred on the vertex at the origin
sphere = cq.Workplane("XY").sphere(30)

# Subtract the sphere to cut a concave spherical pocket into the corner
result = cube.cut(sphere)
