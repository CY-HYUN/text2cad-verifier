import cadquery as cq

# Hollow spherical shell: OD 50 mm, ID 40 mm
outer = cq.Workplane("XY").sphere(25)
inner = cq.Workplane("XY").sphere(20)
shell = outer.cut(inner)

# 20x20 mm square prism along the X axis, cut through the shell
square_prism = cq.Workplane("XY").box(60, 20, 20)

result = shell.cut(square_prism)
