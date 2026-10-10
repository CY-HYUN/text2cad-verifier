import cadquery as cq
import math

# Create the base plate
base_plate = cq.Workplane("XY").box(100, 100, 5)

# Define slot parameters
slot_length = 80
slot_width = 10
slot_height = 5  # Through the entire thickness
num_slots = 5
slot_spacing = 5
deflector_length = 80
deflector_width = 12
deflector_thickness = 2
deflector_angle = 15  # degrees, sloping outward

# Calculate total height occupied by slots and spacing
total_slot_height = (num_slots * slot_width) + ((num_slots - 1) * slot_spacing)
start_y = -total_slot_height / 2

# Start with the base plate
result = base_plate

# Create and subtract each slot with its deflector
for i in range(num_slots):
    # Calculate Y position of this slot
    slot_y = start_y + i * (slot_width + slot_spacing) + slot_width / 2
    
    # Create the rectangular slot (through hole)
    slot_box = cq.Workplane("XY").box(slot_length, slot_width, slot_height + 1)
    slot_box = slot_box.translate((0, slot_y, 0))
    
    # Subtract the slot from the result
    result = result.cut(slot_box)
    
    # Create the deflector plate (angled outward from the top of the slot)
    # Position the deflector at the top surface of the base plate
    deflector = cq.Workplane("XY").box(deflector_length, deflector_width, deflector_thickness)
    
    # Translate to position above the slot
    deflector = deflector.translate((0, slot_y, 2.5 + deflector_thickness / 2))
    
    # Rotate the deflector to create the sloping angle (tilting outward in Y direction)
    deflector = deflector.rotate((1, 0, 0), (0, 0, 0), deflector_angle)
    
    # Add the deflector to the result
    result = result.union(deflector)

result = result
