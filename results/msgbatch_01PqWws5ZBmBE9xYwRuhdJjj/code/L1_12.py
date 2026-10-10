import cadquery as cq

# Create a new part with a disk (cylinder)
# Step 1: Create a circle on the XY plane with diameter 90 mm and extrude by 15 mm
disk = cq.Workplane("XY").circle(90.0 / 2).extrude(15.0)

# Step 2: Create a sketch on the top surface and draw a central square hole
# The top surface is at Z = 15 mm
# Create a square hole with side length 30 mm, centered at origin
disk_with_hole = disk.faces(">Z").workplane().rect(30.0, 30.0).cutThruAll()

result = disk_with_hole
