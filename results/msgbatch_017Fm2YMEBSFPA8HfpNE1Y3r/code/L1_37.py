import cadquery as cq

# Create a new workplane with the XY plane as base
wp = cq.Workplane("XY")

# Draw a circle (diameter 80.0 mm) on the XY plane and extrude it 15.0 mm to form a disk
disk = wp.circle(40.0).extrude(15.0)

# Now we'll work on the top surface to create the cross slots
# Get the top face of the disk and create a workplane on it
top_workplane = disk.faces(">Z").workplane()

# Create a sketch on the top surface with two perpendicular rectangles
slot_sketch = top_workplane.sketch()

# Add first slot (horizontal, along X-axis): width 10mm, length 100mm
# Rectangle centered at origin: 100mm long, 10mm wide
slot_sketch.rect(100.0, 10.0, mode="a")

# Add second slot (vertical, along Y-axis): width 10mm, length 100mm
# Rectangle centered at origin: 10mm wide, 100mm long
slot_sketch.rect(10.0, 100.0, mode="a")

# Finalize the sketch
slot_sketch = slot_sketch.finalize()

# Perform an extruded cut with a depth of 5.0 mm
result = disk.cutBlind(slot_sketch, -5.0)
