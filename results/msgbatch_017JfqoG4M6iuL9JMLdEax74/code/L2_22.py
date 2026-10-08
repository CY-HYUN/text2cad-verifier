import cadquery as cq

# Base cube 40mm
cube = cq.Workplane("XY").box(40, 40, 40)

# 10x10 chamfer on the four vertical edges
cube = cube.edges("|Z").chamfer(10)

# Central through-hole, diameter 30mm, along Z
hole = cq.Workplane("XY").circle(15).extrude(50).translate((0, 0, -25))

result = cube.cut(hole)
