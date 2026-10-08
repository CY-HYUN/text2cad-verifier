import cadquery as cq

# Cylinder: diameter 30 mm, height 100 mm, base on XY plane at origin
cylinder = cq.Workplane("XY").circle(15.0).extrude(100.0)

# Sphere: diameter 40 mm, center at Z = 115 mm (as specified)
sphere = cq.Workplane("XY").sphere(20.0).translate((0, 0, 115.0))

# Boolean union
result = cylinder.union(sphere)
