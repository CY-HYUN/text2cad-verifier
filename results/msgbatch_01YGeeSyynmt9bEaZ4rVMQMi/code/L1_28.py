import cadquery as cq

side = 60.0
sphere_d = 61.0

cube = cq.Workplane("XY").rect(side, side).extrude(side)
sphere = cq.Workplane("XY").sphere(sphere_d / 2.0).translate((0, 0, side / 2.0))

result = cube.cut(sphere)
