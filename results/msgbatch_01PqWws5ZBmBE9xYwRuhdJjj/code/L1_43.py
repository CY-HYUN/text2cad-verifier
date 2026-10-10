import cadquery as cq

# Create the base rectangular solid
# Outer rectangle: 100mm long, 50mm wide, extruded 30mm high
base = cq.Workplane("XY").rect(100.0, 50.0).extrude(30.0)

# Create the slot on the top surface
# Slot dimensions: 100mm long, 30mm wide
# The slot should be centered and cut down 20mm from the top
# This leaves 10mm at the bottom and creates 10mm side walls

# Select the top face and create the slot
result = base.faces(">Z").workplane().rect(100.0, 30.0).cutBlind(-20.0)

