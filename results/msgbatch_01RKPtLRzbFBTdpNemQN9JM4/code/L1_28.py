import cadquery as cq
import math

cube = cq.Workplane("XY").box(60, 60, 60)
sphere = cq.Workplane("XY").sphere(30.5)
result = cube.cut(sphere)
