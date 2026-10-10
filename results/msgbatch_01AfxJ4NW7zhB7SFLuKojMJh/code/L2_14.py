import cadquery as cq

cube = cq.Workplane("XY").box(60, 60, 60)

hole_x = cq.Workplane("XY").box(60, 40, 40)
hole_y = cq.Workplane("XY").box(40, 60, 40)
hole_z = cq.Workplane("XY").box(40, 40, 60)

# make cutters slightly longer to ensure clean through-cuts
cut_x = cq.Workplane("XY").box(80, 40, 40)
cut_y = cq.Workplane("XY").box(40, 80, 40)
cut_z = cq.Workplane("XY").box(40, 40, 80)

result = cube.cut(cut_x).cut(cut_y).cut(cut_z)
