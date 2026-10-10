import cadquery as cq
import math

R = 40
profile = (cq.Workplane("XZ")
           .moveTo(-R, 0).lineTo(R, 0)
           .threePointArc((0, -R), (-R, 0))
           .close())
hemi = profile.revolve(360, (0, 0, 0), (1, 0, 0))

box1 = cq.Workplane("XY").box(100, 10, 20).translate((0, 0, -10))
box2 = cq.Workplane("XY").box(10, 100, 20).translate((0, 0, -10))

result = hemi.cut(box1).cut(box2)
