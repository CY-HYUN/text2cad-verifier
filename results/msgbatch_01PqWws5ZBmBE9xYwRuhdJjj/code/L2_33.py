import cadquery as cq
import math

# Create the base plate
base_plate = cq.Workplane("XY").box(100, 100, 5)

# Create a single slot and baffle unit
def create_slot_baffle_unit():
    # Start with a workplane at the top of the base plate
    wp = cq.Workplane("XY").moveTo(0, 0).transformed(offset=(0, 0, 2.5))
    
    # Cut the slot: 80x10mm
    slot_box = cq.Workplane("XY").box(80, 10, 10)
    
    # Create the baffle profile
    # Baffle: 12mm width, 2mm thickness, at 45 degrees
    baffle_wp = cq.Workplane("XZ").moveTo(0, 0)
    
    # Create a rectangular baffle profile (2mm thick, 12mm tall)
    baffle_profile = baffle_wp.rect(2, 12).extrude(10)
    
    # Rotate the baffle to 45 degrees
    baffle_rotated = baffle_profile.rotate((0, 0, 0), (0, 1, 0), 45)
    
    return slot_box, baffle_rotated

# Get the slot and baffle for the first unit
slot_box, baffle_rotated = create_slot_baffle_unit()

# Create an array by replicating the slot-baffle feature 5 times along Y-axis with 15mm spacing
result = base_plate.copy()

for i in range(5):
    y_offset = i * 15 - 30  # Center the array around y=0
    
    # Cut the slot at this Y position
    slot_positioned = slot_box.translate((0, y_offset, 0))
    result = result.cut(slot_positioned)
    
    # Add the baffle at this Y position
    baffle_positioned = baffle_rotated.translate((0, y_offset, 0))
    result = result.union(baffle_positioned)

