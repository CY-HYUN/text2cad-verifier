import cadquery as cq
import math

# Create the base workplane
wp = cq.Workplane("XY")

# Create Plane 1 at z=0 with a 50x50 rectangle
plane1_rect = wp.sketch().rect(50, 50).finalize().extrude(0.1)

# Create Plane 2 at z=30 with a 50x50 rectangle
plane2_rect = wp.transformed(offset=(0, 0, 30)).sketch().rect(50, 50).finalize().extrude(0.1)

# Create Plane 3 at z=60 with a circle of diameter 30mm (radius 15mm)
plane3_circle = wp.transformed(offset=(0, 0, 60)).sketch().circle(15).finalize().extrude(0.1)

# Create the loft between Plane 2 rectangle and Plane 3 circle
# First, create profiles for lofting
rectangle_profile = cq.Workplane("XY").transformed(offset=(0, 0, 30)).sketch().rect(50, 50).finalize()
circle_profile = cq.Workplane("XY").transformed(offset=(0, 0, 60)).sketch().circle(15).finalize()

# Create rectangles and circle as wires for lofting
rect_wire = (cq.Workplane("XY").sketch().rect(50, 50).finalize().val().wires()[0])
circle_wire = (cq.Workplane("XY").sketch().circle(15).finalize().val().wires()[0])

# Create the loft solid
loft_solid = cq.Workplane("XY").loft([rect_wire, circle_wire])

# Create a 20mm square column at the bottom (Plane 1 level)
square_column = (cq.Workplane("XY")
                 .sketch()
                 .rect(20, 20)
                 .finalize()
                 .extrude(20))

# Create a 20mm cylindrical column at the top (Plane 3 level)
cylinder_column = (cq.Workplane("XY")
                   .transformed(offset=(0, 0, 60))
                   .sketch()
                   .circle(10)
                   .finalize()
                   .extrude(20))

# Combine all parts
result = square_column.union(loft_solid).union(cylinder_column)

# Apply shell operation to remove top and bottom faces with 2mm wall thickness
# Get all faces and identify top/bottom faces to remove
faces = result.val().faces()
# Filter to get top and bottom faces (approximate approach)
faces_to_remove = []
for face in faces:
    center = face.Center()
    # Remove faces at z~0 and z~80 (top and bottom)
    if center.z < 5 or center.z > 75:
        faces_to_remove.append(face)

# Create shell by removing top and bottom faces
result = result.shell(2, faceList=faces_to_remove)
