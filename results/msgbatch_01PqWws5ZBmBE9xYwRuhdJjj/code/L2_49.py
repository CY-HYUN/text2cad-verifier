import cadquery as cq
import math

# Entity 1: Horizontal ring (revolved around Y-axis)
# Create a circle in the XY plane (front view) and revolve around Y-axis
sketch1 = cq.Workplane("XY").circle(1).circle(0.3)  # Outer circle and inner hole
entity1 = sketch1.revolve(360, (0, 1, 0))

# Entity 2: Vertical ring (revolved around X-axis)
# Create a circle in the YZ plane (right view) with center offset so it passes through Entity 1's inner hole
# The inner radius of Entity 1 is 0.3mm, so we position Entity 2's circle appropriately
# Circle center offset: we want the ring to pass through the hole at radius ~1mm from X-axis
sketch2 = cq.Workplane("YZ").workplane(offset=0).circle(1).circle(0.3)
# Move the sketch so the center is at the right height to intersect with Entity 1's inner hole
sketch2 = cq.Workplane("YZ").transformed(offset=(0, 0, 0)).circle(1).circle(0.3)
entity2 = sketch2.revolve(360, (1, 0, 0))

# Combine both entities
result = entity1.union(entity2)
