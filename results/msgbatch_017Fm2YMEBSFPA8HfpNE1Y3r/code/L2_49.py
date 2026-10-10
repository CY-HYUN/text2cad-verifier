import cadquery as cq
import math

# Entity 1: Horizontal ring (revolved around Y-axis)
# Create a circle in the XY plane (front view) offset from origin, then revolve around Y-axis
wp1 = cq.Workplane("XY")
wp1 = wp1.movePolar(1.5, 0).circle(0.5)  # Circle centered at distance 1.5 from origin
entity1 = wp1.revolve(360, axisStartPoint=(0, 0, 0), axisEndPoint=(0, 1, 0))

# Entity 2: Vertical ring (revolved around X-axis)
# Create a circle in the YZ plane (right view) offset from origin, then revolve around X-axis
wp2 = cq.Workplane("YZ")
wp2 = wp2.movePolar(1.5, 0).circle(0.5)  # Circle centered at distance 1.5 from origin
entity2 = wp2.revolve(360, axisStartPoint=(0, 0, 0), axisEndPoint=(1, 0, 0))

# Combine both entities
result = entity1.union(entity2)
