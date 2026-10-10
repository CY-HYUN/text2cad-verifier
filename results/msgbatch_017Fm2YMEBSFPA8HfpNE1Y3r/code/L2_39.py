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

# Create the 2D trapezoid sketch and extrude to form wedge
wp = cq.Workplane("front")
wedge = wp.sketch().polygon(trapezoid_points).close().extrude(40)

# Find the beveled face (the slanted face)
# Iterate through faces to find one with a tilted normal
beveled_face = None
for face in wedge.faces().objects:
    normal = face.normalAt()
    # The beveled face should have significant x and z components
    if abs(normal.x) > 0.3 and abs(normal.z) > 0.3:
        beveled_face = face
        break

# Create workplane on the beveled face and cut a rectangular slot
if beveled_face is not None:
    wp_beveled = cq.Workplane().workplaneFromFace(beveled_face)
    # Draw 30x15mm rectangle and cut 10mm perpendicular to face
    wedge_with_slot = wp_beveled.sketch().rect(30, 15).close().cutBlind(-10)
else:
    wedge_with_slot = wedge

# Find the bottom face (at z=0) to locate the circle center
bottom_face = None
for face in wedge_with_slot.faces().objects:
    bb = face.BoundingBox()
    # Bottom face should have minimal z extent
    if bb.zmin < 1 and bb.zmax < 1:
        bottom_face = face
        break

# Create the final result with circle hole
if bottom_face is not None:
    wp_bottom = cq.Workplane().workplaneFromFace(bottom_face)
    bb = bottom_face.BoundingBox()
    center_x = (bb.xmin + bb.xmax) / 2
    center_y = (bb.ymin + bb.ymax) / 2
    
    result = wp_bottom.moveTo(center_x, center_y).sketch().circle(4).close().cutThruAll()
else:
    result = wedge_with_slot
