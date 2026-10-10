import cadquery as cq
import math

# Create first cylinder along X-axis
cylinder_x = cq.Workplane("XY").cylinder(100, 20, centered=True)

# Create second cylinder along Y-axis
cylinder_y = cq.Workplane("XY").cylinder(100, 20, centered=True).rotated(0, 90, 0)

# Boolean union of the two cylinders
cross = cylinder_x.union(cylinder_y)

# Get all faces and identify the four end faces (the smallest circular faces)
# We'll use the shell command to create a hollow structure with 2mm wall thickness
# The shell command removes selected faces and creates a hollow interior

# Get faces of the cross shape
faces = cross.faces()

# Identify end faces - these are the circular faces at the ends of the cylinders
# We need to find and remove the 4 end faces (2 on X-axis cylinder, 2 on Y-axis cylinder)
# End faces are at z=±50 and y=±50 for the respective cylinders

end_faces = []
all_faces = faces.all()

# Filter faces based on their position - end faces are the flat circular faces
# at the extremities of each cylinder
for face in all_faces:
    # Get the center point of the face
    center = face.Center()
    # End faces are those far from origin along their respective axes
    if abs(center.z) > 45 or abs(center.y) > 45:  # Circular ends
        end_faces.append(face)

# Perform shell operation - remove end faces and create 2mm wall thickness
result = cross.shell(2.0, end_faces)
