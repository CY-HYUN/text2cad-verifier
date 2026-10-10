import cadquery as cq
import math

disc = cq.Workplane("XY").circle(50).extrude(10)
pts = [(35 * math.cos(math.radians(a)), 35 * math.sin(math.radians(a))) for a in (0, 90, 180, 270)]
result = disc.faces(">Z").workplane().pushPoints(pts).hole(10)
