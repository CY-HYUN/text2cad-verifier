import cadquery as cq

# Create a new workplane on the XY plane at origin
wp = cq.Workplane("XY")

# Draw a circle with diameter 60.0 mm on the XY plane and extrude it 40.0 mm
cylinder = wp.circle(60.0 / 2).extrude(40.0)

# Create a sketch on the top surface of the cylinder
top_surface = cylinder.faces(">Z").workplane()

# Offset 15.0 mm in the +X direction and draw a hole with diameter 10.0 mm
hole_sketch = top_surface.moveTo(15.0, 0).circle(10.0 / 2)

# Perform an extruded cut through the entire part
result = cylinder.cutThruAll(hole_sketch)
