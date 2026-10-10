import cadquery as cq

# Create a new workplane with the XY plane as base
wp = cq.Workplane("XY")

# Draw a circle (diameter 80.0 mm) on the XY plane and extrude it 15.0 mm to form a disk
disk = wp.circle(40.0).extrude(15.0)

# Now we'll work on the top surface to create the cross slots
# Get the top face of the disk
top_face = disk.faces(">Z").workplane()

# Create two perpendicular rectangular slots
# Slot 1: horizontal slot (along X-axis)
# Slot 2: vertical slot (along Y-axis)
# Both slots have width 10.0 mm and length > 80.0 mm (use 100 mm to ensure they pass through)

# Create a sketch on the top surface with two perpendicular rectangles
slot_sketch = top_face.sketch()

# Add first slot (horizontal, along X-axis): width 10mm, length 100mm
# Rectangle centered at origin: from (-50, -5) to (50, 5)
slot_sketch.rect(100.0, 10.0, mode="a")

# Add second slot (vertical, along Y-axis): width 10mm, length 100mm
# Rectangle centered at origin: from (-5, -50) to (5, 50)
slot_sketch.rect(10.0, 100.0, mode="a")

# Finalize the sketch
slot_sketch = slot_sketch.finalize()

# Perform an extruded cut with a depth of 5.0 mm
result = disk.cutBlind(slot_sketch, -5.0)
