import cadquery as cq
import math

cube = cq.Workplane("XY").rect(50.0, 50.0).extrude(50.0)
result = cube.faces(">Z").workplane().circle(10.0).cutThruAll()
