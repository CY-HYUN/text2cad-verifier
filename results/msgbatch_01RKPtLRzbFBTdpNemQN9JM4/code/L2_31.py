import cadquery as cq
import math

outer = cq.Workplane("XY").sphere(25)
inner = cq.Workplane("XY").sphere(20)
shell = outer.cut(inner)

# square prism along +X, 20x20 cross-section in YZ plane
cutter = cq.Workplane("YZ").rect(20, 20).extrude(30)

result = shell.cut(cutter)
