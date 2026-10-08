import cadquery as cq

cube_edge = 60.0
sphere_diameter = 61.0

# Sphere is slightly larger than the cube, so subtracting it breaks through
# the centre of each of the six faces.
body = cq.Workplane("XY").box(cube_edge, cube_edge, cube_edge)
cavity = cq.Workplane("XY").sphere(sphere_diameter / 2.0)

result = body.cut(cavity)
