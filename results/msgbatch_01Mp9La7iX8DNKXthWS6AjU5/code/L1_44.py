import cadquery as cq
import math

# Cube 40x40x40, base on XY plane at origin (centered in XY)
cube = cq.Workplane("XY").rect(40.0, 40.0).extrude(40.0)

# Through hole diameter 20 from top face
cube = cube.faces(">Z").workplane().circle(10.0).cutThruAll()

# Counterbore diameter 30, depth 10 from top face
cube = cube.faces(">Z").workplane().circle(15.0).cutBlind(-10.0)

result = cube
