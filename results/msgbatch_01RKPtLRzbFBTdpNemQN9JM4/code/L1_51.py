import cadquery as cq
import math

# Main disc: diameter 60, thickness 10 along Z
disc = cq.Workplane("XY").circle(30).extrude(10)

# Cylindrical bite: diameter 20, centered on the edge of the disc (at x = 30)
bite = cq.Workplane("XY").center(30, 0).circle(10).extrude(10)

result = disc.cut(bite)
