import cadquery as cq

cube = cq.Workplane("XY").box(60, 60, 60)

hole_x = cq.Workplane("XY").box(60, 40, 40)
hole_y = cq.Workplane("XY").box(40, 60, 40)
hole_z = cq.Workplane("XY").box(40, 40, 60)

result = cube.cut(hole_x).cut(hole_y).cut(hole_z)
