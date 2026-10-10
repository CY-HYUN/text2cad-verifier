import cadquery as cq
import math

cube = cq.Workplane("XY").rect(60.0, 60.0).extrude(60.0)
sphere = cq.Workplane("XY").sphere(30.5).translate((0, 0, 30))
result = cube.cut(sphere)
