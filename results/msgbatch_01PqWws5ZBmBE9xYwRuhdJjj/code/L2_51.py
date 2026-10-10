import cadquery as cq
import math

# Create a T-shaped sketch
sketch = cq.Sketch().rect(40, 10, mode="a").rect(10, 30, mode="a").vertices().circle(2.5)

# Extrude the sketch by 20mm
extruded = cq.Workplane("XY").planeData().sketch(sketch).val()
base = cq.Workplane("XY").sketch(sketch).extrude(20)

# Create the T-shape more explicitly
# Horizontal bar: 40mm wide x 10mm tall
# Vertical bar: 10mm wide x 30mm tall, centered on horizontal bar
horizontal = cq.Workplane("XY").rect(40, 10).extrude(20)
vertical = cq.Workplane("XY").rect(10, 30).extrude(20)

# Combine the two parts
t_shape = horizontal.union(vertical)

# Fillet all edges with radius 8mm
filleted = t_shape.edges().fillet(8)

# Now add holes for the three sides
# Top side hole
hole_top = cq.Workplane("XY").moveTo(0, 20).circle(2.5).extrude(-20)

# Bottom side hole  
hole_bottom = cq.Workplane("XY").moveTo(0, -20).circle(2.5).extrude(-20)

# Front side hole (vertical bar extending down)
hole_front = cq.Workplane("XY").moveTo(0, 0).circle(2.5).extrude(-20)

# Cut all three holes
result = filleted.cut(hole_top).cut(hole_bottom).cut(hole_front)
