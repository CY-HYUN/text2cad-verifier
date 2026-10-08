import cadquery as cq
import math

# Base flange disk: OD 100, thickness 12, bottom face at Z=0
plate = cq.Workplane("XY").circle(50).extrude(12)

# Four through-holes, dia 10, on a 70 mm bolt circle at 0/90/180/270 deg
pts = [(35, 0), (0, 35), (-35, 0), (0, -35)]
plate = plate.faces(">Z").workplane().pushPoints(pts).hole(10)

# 45 deg x 0.8 mm chamfer on the top edges of the holes
# (circular edges on the top face, excluding the outer rim)
plate = (
    plate.faces(">Z")
    .edges(cq.selectors.RadiusNthSelector(0))
    .chamfer(0.8)
)

result = plate
