import cadquery as cq
import math

# Hollow spherical shell: outer diameter 50, inner diameter 40
outer = cq.Workplane("XY").sphere(25)
inner = cq.Workplane("XY").sphere(20)
shell = outer.cut(inner)

# 20x20 square prism along the X axis; cutting the shell on the +X side only
# (through the wall on one side) creating a square window with curved edges.
# Square profile on YZ plane, extruded from x=0 outward past the shell.
cutter = (
    cq.Workplane("YZ")
    .rect(20, 20)
    .extrude(30)
)

result = shell.cut(cutter)
