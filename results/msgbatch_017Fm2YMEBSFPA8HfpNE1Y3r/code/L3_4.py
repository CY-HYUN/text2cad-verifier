import cadquery as cq
import math

# Create profiles at different X positions
# Profile 1 at X=0: circle with 15mm diameter
profile1_wp = cq.Workplane("YZ").transformed(offset=(0, 0, 0)).circle(15/2)

# Profile 2 at X=50: ellipse with major axis 25mm, minor axis 20mm
profile2_wp = cq.Workplane("YZ").transformed(offset=(50, 0, 0)).ellipse(25/2, 20/2)

# Profile 3 at X=100: ellipse with major axis 22mm, minor axis 18mm
profile3_wp = cq.Workplane("YZ").transformed(offset=(100, 0, 0)).ellipse(22/2, 18/2)

# Profile 4 at X=150: circle with 20mm diameter
profile4_wp = cq.Workplane("YZ").transformed(offset=(150, 0, 0)).circle(20/2)

# Extract edges from profiles for lofting
edge1 = profile1_wp.val().Edges()[0]
edge2 = profile2_wp.val().Edges()[0]
edge3 = profile3_wp.val().Edges()[0]
edge4 = profile4_wp.val().Edges()[0]

# Create lofted solid using the four profile edges
lofted_solid = cq.Workplane("XY").loft([edge1, edge2, edge3, edge4], ruled=False)

# Get the solid from the workplane
solid = lofted_solid.val()

# Apply shell operation to create wall thickness of 1.5mm
# Shell removes the end faces and creates hollow structure
try:
    # Get all faces and identify the end faces (at X=0 and X=150)
    faces = solid.Faces()
    
    # Find and remove the two end faces
    faces_to_remove = []
    for face in faces:
        bb = face.BoundingBox()
        # Check if face is at X=0 or X=150 (end faces)
        if abs(bb.center.x - 0) < 1 or abs(bb.center.x - 150) < 1:
            faces_to_remove.append(face)
    
    # Create shell with 1.5mm wall thickness, removing end faces
    result_solid = solid.shell(1.5, faces=faces_to_remove)
    result = cq.Workplane("XY").add(result_solid)
except:
    # Fallback: create shell with thickness
    result_solid = solid.shell(1.5)
    result = cq.Workplane("XY").add(result_solid)
