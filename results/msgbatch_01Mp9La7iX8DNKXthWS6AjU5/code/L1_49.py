import cadquery as cq
import math

L = 40.0
d = 10.0

cube = cq.Workplane("XY").box(L, L, L, centered=(True, True, False))
cz = L / 2.0

# Z-axis hole
hole_z = cq.Workplane("XY").circle(d / 2).extrude(L * 2).translate((0, 0, -L / 2))

# X-axis hole (through center at z = 20)
hole_x = cq.Workplane("YZ").workplane(offset=-L).center(0, cz).circle(d / 2).extrude(L * 2)

# Y-axis hole
hole_y = cq.Workplane("XZ").workplane(offset=-L).center(0, cz).circle(d / 2).extrude(L * 2)

result = cube.cut(hole_z).cut(hole_x).cut(hole_y)
