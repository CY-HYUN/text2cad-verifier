import cadquery as cq
import math

outer = cq.Workplane("XY").sphere(50.0)
inner = cq.Workplane("XY").sphere(40.0)

# Half-space box covering z >= 0
cutter = cq.Workplane("XY").box(200, 200, 100, centered=(True, True, False))

outer_h = outer.intersect(cutter)
inner_h = inner.intersect(cutter)

result = outer_h.cut(inner_h)
