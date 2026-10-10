import cadquery as cq
import math

# Create base workplane
wp = cq.Workplane("XY")

# Create a 50x50 rectangle on Plane 1 (z=0)
rect1 = cq.Workplane("XY").rect(50, 50).wire()

# Create a 50x50 rectangle on Plane 2 (z=30)
rect2 = cq.Workplane("XY").transformed(offset=(0, 0, 30)).rect(50, 50).wire()

# Create a circle with diameter 30mm on Plane 3 (z=60)
circle = cq.Workplane("XY").transformed(offset=(0, 0, 60)).circle(15).wire()

# Create loft between rect2 and circle (from z=30 to z=60)
loft_solid = cq.Workplane("XY").loft([rect2, circle])

# Create a 20mm square column at the bottom
square_column = cq.Workplane("XY").box(20, 20, 20, centered=True)

# Create a 20mm cylindrical column at the top (at z=60)
cylinder_column = (cq.Workplane("XY")
                   .transformed(offset=(0, 0, 70))
                   .cylinder(20, 10, centered=True))

# Combine all parts
combined = square_column.union(loft_solid).union(cylinder_column)

# Apply shell operation to remove top and bottom faces with 2mm wall thickness
# Get faces to remove (top and bottom faces)
all_faces = combined.val().faces()
faces_to_remove = []

for face in all_faces:
    center = face.Center()
    # Remove bottom face (z < 0) and top face (z > 75)
    if center.z < -5 or center.z > 75:
        faces_to_remove.append(face)

# Create shell with 2mm thickness
result = combined.shell(2, faceList=faces_to_remove)
