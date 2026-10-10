import cadquery as cq
import math

# Create the arc path in the front view plane (XY plane)
# 90-degree arc with radius 50 mm, from (50, 0, 0) to (0, 50, 0)
arc_path = cq.Workplane("front").moveTo(50, 0).radiusArc((0, 50), 50)

# Extract the arc edge for use as the loft path
arc_edge = arc_path.val().Edges()[0]

# Create the start plane at the beginning of the arc (50, 0, 0)
# This is the XZ plane translated to x=50, y=0
start_plane = cq.Workplane("XZ").moveTo(0, 0).transformed(offset=cq.Vector(50, 0, 0))

# Create a circle with diameter 30 mm on the start plane
circle_start = start_plane.circle(15)  # radius = 30/2 = 15

# Create the end plane at the end of the arc (0, 50, 0)
# This is the YZ plane translated to x=0, y=50
end_plane = cq.Workplane("YZ").moveTo(0, 0).transformed(offset=cq.Vector(0, 50, 0))

# Create a circle with diameter 15 mm on the end plane
circle_end = end_plane.circle(7.5)  # radius = 15/2 = 7.5

# Get the wire profiles for lofting
profile_start = circle_start.val()
profile_end = circle_end.val()

# Create the loft between the two circular profiles using the arc as the centerline
# We need to create a loft that follows the arc path
result = cq.Workplane("XY").loft([profile_start, profile_end], ruled=False, combine=True)

# Alternative approach: manually construct using the arc path as spine
# Create workplane at start of arc
wp_start = cq.Workplane("XZ").transformed(offset=cq.Vector(50, 0, 0))
profile1 = wp_start.circle(15).val()

# Create workplane at end of arc  
wp_end = cq.Workplane("YZ").transformed(offset=cq.Vector(0, 50, 0))
profile2 = wp_end.circle(7.5).val()

# Use loft to create the elbow
result = cq.Workplane("XY").loft([profile1, profile2])
