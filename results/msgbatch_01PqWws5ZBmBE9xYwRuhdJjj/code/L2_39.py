import cadquery as cq
import math

# Create the right trapezoid in the front view plane
# Base 60mm, rear vertical side 40mm, front vertical side 10mm
trapezoid_points = [
    (0, 0),      # origin
    (60, 0),     # base (60mm)
    (60, 10),    # front vertical side (10mm)
    (0, 40)      # rear vertical side (40mm)
]

# Create the 2D trapezoid sketch
trapezoid = cq.Sketch().polygon(trapezoid_points).close()

# Create a workplane and create the trapezoid face
wp = cq.Workplane("front")
trapezoid_face = wp.placeSketch(trapezoid).extrude(40)  # Extrude 40mm to form wedge

# Now we need to find the beveled (slanted) face and work with it
# The beveled face is the face connecting (60,10) to (0,40) and extending through the extrusion
# Let's identify and work with this face

# Get all faces and find the slanted one (the beveled face)
# The beveled face should have a normal that's tilted
solid = trapezoid_face.val()
faces = solid.faces()

# Find the slanted face by checking face normals
beveled_face = None
for face in faces:
    normal = face.normalAt()
    # The beveled face should have a normal with both x and z components (not purely in y direction)
    if abs(normal.x) > 0.1 and abs(normal.z) > 0.1:
        beveled_face = face
        break

# Create a new workplane on the beveled face
if beveled_face is not None:
    wp_beveled = cq.Workplane("front").moveTo(0, 0).workplaneFromFace(beveled_face)
    
    # Draw a 30x15mm rectangle centered on this face
    # We need to position it appropriately on the beveled face
    # The rectangle should be positioned at the center of the face
    rect_sketch = cq.Sketch().rect(30, 15)
    
    # Create the slot by cutting 10mm downward perpendicular to the beveled face
    slot = wp_beveled.placeSketch(rect_sketch).cutBlind(-10)
else:
    slot = trapezoid_face

# Now find the bottom plane and create a circle at its center
# The bottom plane is at z=0 in our original coordinate system
# Get the bottom face (should be one of the rectangular faces at z=0)
solid = slot.val()
faces = solid.faces()

# Find the bottom face (z=0 plane)
bottom_face = None
for face in faces:
    # Check if this is the bottom face by checking the bounding box
    bb = face.BoundingBox()
    if bb.zmin < 1 and bb.zmax < 1:  # Close to z=0
        bottom_face = face
        break

# Create a workplane on the bottom face and add an 8mm diameter circle at center
if bottom_face is not None:
    wp_bottom = cq.Workplane("front").workplaneFromFace(bottom_face)
    # Get the center of the bottom face
    bb = bottom_face.BoundingBox()
    center_x = (bb.xmin + bb.xmax) / 2
    center_y = (bb.ymin + bb.ymax) / 2
    
    circle_sketch = cq.Sketch().circle(4)  # 8mm diameter = 4mm radius
    
    # Cut through the entire solid vertically downward
    result = wp_bottom.moveTo(center_x, center_y).placeSketch(circle_sketch).cutThruAll()
else:
    result = slot

# Ensure result is assigned properly
if result is None:
    result = slot
