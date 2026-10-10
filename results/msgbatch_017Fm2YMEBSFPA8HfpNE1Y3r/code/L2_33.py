import cadquery as cq
import math

# Create the base plate
base_plate = cq.Workplane("XY").box(100, 100, 5)

# Create the slot box centered at origin
slot_box = cq.Workplane("XY").box(80, 10, 10)

# Create the baffle profile: 2mm thick, 12mm wide, extruded along one direction
baffle_profile = cq.Workplane("XZ").rect(2, 12).extrude(10)

# Rotate the baffle to 45 degrees around Y axis
baffle_rotated = baffle_profile.rotate((0, 0, 0), (0, 1, 0), 45)

# Start with the base plate
result = base_plate

# Create an array by replicating the slot-baffle feature 5 times along Y-axis with 15mm spacing
for i in range(5):
    y_offset = i * 15 - 30  # Center the array around y=0
    
    # Cut the slot at this Y position
    slot_positioned = slot_box.translate((0, y_offset, 0))
    result = result.cut(slot_positioned)
    
    # Add the baffle at this Y position
    baffle_positioned = baffle_rotated.translate((0, y_offset, 0))
    result = result.union(baffle_positioned)
