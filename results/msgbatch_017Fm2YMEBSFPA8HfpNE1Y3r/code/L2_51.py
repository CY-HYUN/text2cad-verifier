import cadquery as cq
import math

# Create a T-shaped block by combining two rectangles
# Horizontal bar: 40mm wide x 10mm tall
horizontal = cq.Workplane("XY").rect(40, 10).extrude(20)

# Vertical bar: 10mm wide x 30mm tall, centered on horizontal bar
vertical = cq.Workplane("XY").rect(10, 30).extrude(20)

# Combine the two parts using union
t_shape = horizontal.union(vertical)

# Fillet all edges with radius 8mm
filleted = t_shape.edges().fillet(8)

# Create holes at three flat ends
# Top hole (at y=20, center of top flat surface)
hole_top = cq.Workplane("XY").moveTo(0, 20).circle(2.5).cutThruAll()

# Bottom hole (at y=-20, center of bottom flat surface)
hole_bottom = cq.Workplane("XY").moveTo(0, -20).circle(2.5).cutThruAll()

# Center hole (at y=0, center of the vertical bar)
hole_center = cq.Workplane("XY").moveTo(0, 0).circle(2.5).cutThruAll()

# Cut all three holes through the filleted block
result = filleted.cut(hole_top).cut(hole_bottom).cut(hole_center)
