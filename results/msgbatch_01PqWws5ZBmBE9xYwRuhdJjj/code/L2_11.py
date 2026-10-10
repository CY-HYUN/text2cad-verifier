import cadquery as cq
import math

# Create a 60x40mm rectangle and extrude it 40mm
result = cq.Workplane("XY").rect(60, 40).extrude(40)

# Add blind holes on top surface
# Two circles with 10mm diameter, spaced 30mm apart
result = result.faces(">Z").workplane().moveTo(-15, 0).circle(5).cutBlind(30)
result = result.faces(">Z").workplane().moveTo(15, 0).circle(5).cutBlind(30)

# Create a horizontal hole through the side
# Select a side face (the one at Y = -20), draw a circle and cut inward
# The hole needs to go deep enough to intersect both vertical blind holes
result = result.faces("<Y").workplane().moveTo(0, 20).circle(5).cutBlind(35)
