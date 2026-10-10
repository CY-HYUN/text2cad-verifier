import cadquery as cq
import math

# Hollow spherical shell: outer diameter 50, inner diameter 40
outer = cq.Workplane("XY").sphere(25)
inner = cq.Workplane("XY").sphere(20)
shell = outer.cut(inner)

# 20x20 square through-hole along the X axis, cutting both sides of the shell
cutter = (
    cq.Workplane("YZ")
    .rect(20, 20)
    .extrude(30, both=True)
)

result = shell.cut(cutter)
