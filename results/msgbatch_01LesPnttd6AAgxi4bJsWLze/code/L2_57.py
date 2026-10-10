import cadquery as cq
import math

# Create the main cylinder body
main_cylinder = cq.Solid.makeCylinder(50, 30)

# Create the central hole
hole = cq.Solid.makeCylinder(15, 30)

# Subtract the hole from the main cylinder
body = main_cylinder.cut(hole)

# Create the eight semicircular grooves
groove_radius = 10
cylinder_radius = 50
num_grooves = 8

for i in range(num_grooves):
    # Calculate angle for each groove
    angle = (360 / num_grooves) * i
    angle_rad = math.radians(angle)
    
    # Position of groove center on the circumference
    groove_x = cylinder_radius * math.cos(angle_rad)
    groove_y = cylinder_radius * math.sin(angle_rad)
    
    # Create a sphere for the semicircular groove
    # The sphere will be positioned at the edge and cut into the body
    sphere = cq.Solid.makeSphere(groove_radius)
    
    # Translate sphere to the edge of the cylinder
    sphere = sphere.translate((groove_x, groove_y, 0))
    
    # Create a cutting box to keep only the semicircle that intersects with the cylinder edge
    # Cut the groove from the body
    body = body.cut(sphere)

# Create the keyway on the hole
# The keyway is a rectangular cut: width 8mm, depth 4mm
keyway_width = 8
keyway_depth = 4
keyway_height = 30

# Create a box for the keyway positioned at the edge of the hole
keyway_box = cq.Solid.makeBox(keyway_width, keyway_depth, keyway_height)

# Position keyway at the edge of the hole (15mm radius - 4mm depth)
keyway_box = keyway_box.translate((-keyway_width/2, 15 - keyway_depth, -keyway_height/2))

# Cut the keyway from the body
body = body.cut(keyway_box)

result = body
