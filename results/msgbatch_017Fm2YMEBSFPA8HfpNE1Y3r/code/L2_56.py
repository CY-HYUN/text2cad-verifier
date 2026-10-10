import cadquery as cq
import math

# Create first cylinder along X-axis
cylinder_x = cq.Workplane("XY").cylinder(100, 20, centered=True)

# Create second cylinder along Y-axis by rotating the workplane
cylinder_y = cq.Workplane("XZ").cylinder(100, 20, centered=True)

# Boolean union of the two cylinders
cross = cylinder_x.union(cylinder_y)

# Get all faces of the cross shape
all_faces = cross.faces().all()

# Identify end faces - these are the circular faces at the ends of the cylinders
# End faces are located at the extremities along X and Y axes
end_faces = []
for face in all_faces:
    center = face.Center()
    # End faces are those far from origin along their respective axes
    # For X-axis cylinder ends: at x=±50, for Y-axis cylinder ends: at y=±50
    if abs(center.x) > 45 or abs(center.y) > 45:
        end_faces.append(face)

# Perform shell operation - remove end faces and create 2mm wall thickness
result = cross.shell(2.0, end_faces)
