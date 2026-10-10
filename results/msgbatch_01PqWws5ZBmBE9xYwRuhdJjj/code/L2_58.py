import cadquery as cq
import math

# Create the base rectangular prism
result = cq.Workplane("XY").box(80, 40, 40)

# Define circle diameter for the holes
diameter = 20
radius = diameter / 2

# First hole: on the left side (YZ plane), going right (along X axis) for 40mm
# The left side is at X = -40, we want to cut from there going right
result = result.faces("<X").workplane().circle(radius).cutBlind(-40)

# Second hole: on the top surface (XY plane), centered, going down (along -Z axis) for 20mm
# The top surface is at Z = 20, we want to cut from there going down
result = result.faces(">Z").workplane().circle(radius).cutBlind(-20)

# The two holes intersect:
# - First hole goes from X=-40 to X=0 (center), at Y=0, Z=0
# - Second hole goes from Z=20 to Z=0 (center), at X=0, Y=0
# They meet at the center point (0, 0, 0) forming an L-shaped internal channel
