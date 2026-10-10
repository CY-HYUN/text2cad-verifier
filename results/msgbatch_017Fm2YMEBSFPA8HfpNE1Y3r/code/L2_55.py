import cadquery as cq
import math

# Create the arc path in the front view plane (XY plane)
# 90-degree arc with radius 50 mm, from (50, 0, 0) to (0, 50, 0)
arc_path = cq.Workplane("front").moveTo(50, 0).radiusArc((0, 50), 50)

# Create the start plane at the beginning of the arc (50, 0, 0)
# This is the XZ plane translated to x=50, y=0
wp_start = cq.Workplane("XZ").transformed(offset=cq.Vector(50, 0, 0))
profile_start = wp_start.circle(15)  # radius = 30/2 = 15

# Create the end plane at the end of the arc (0, 50, 0)
# This is the YZ plane translated to x=0, y=50
wp_end = cq.Workplane("YZ").transformed(offset=cq.Vector(0, 50, 0))
profile_end = wp_end.circle(7.5)  # radius = 15/2 = 7.5

# Get the wire profiles for lofting
wire_start = profile_start.val()
wire_end = profile_end.val()

# Use loft to create the elbow using the profiles
result = cq.Workplane("XY").loft([wire_start, wire_end])
