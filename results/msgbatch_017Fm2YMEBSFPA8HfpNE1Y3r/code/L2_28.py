import cadquery as cq
import math

# Create the outer cube shell
outer_cube = cq.Workplane("XY").box(60, 60, 60)
outer_shell = outer_cube.shell(5.0)  # 5mm wall thickness

# Create the inner small cube at the center
inner_cube = cq.Workplane("XY").box(20, 20, 20)

# Define the six face centers of the small cube (20mm edge)
# Faces are at distance 10mm from center
face_centers = [
    (10, 0, 0),    # +X face
    (-10, 0, 0),   # -X face
    (0, 10, 0),    # +Y face
    (0, -10, 0),   # -Y face
    (0, 0, 10),    # +Z face
    (0, 0, -10),   # -Z face
]

# Create cylinders from each face center to touch the inner wall
# Inner cavity radius is 30mm - 5mm = 25mm from center
# Distance from center to face of inner cube: 10mm
# Distance from face of inner cube to inner wall: 25mm - 10mm = 15mm
cylinder_length = 15.0
cylinder_radius = 1.0  # 2mm diameter = 1mm radius

# Create all six cylinders
cylinders = []
directions = [
    (1, 0, 0),   # +X
    (-1, 0, 0),  # -X
    (0, 1, 0),   # +Y
    (0, -1, 0),  # -Y
    (0, 0, 1),   # +Z
    (0, 0, -1),  # -Z
]

for i, (center, direction) in enumerate(zip(face_centers, directions)):
    # Create a cylinder along the direction
    cyl = cq.Workplane("XY").cylinder(cylinder_length, cylinder_radius)
    # Rotate and position the cylinder
    if i < 2:  # X direction cylinders
        cyl = cyl.rotateAboutCenter((0, 1, 0), 90)
    elif i < 4:  # Y direction cylinders
        cyl = cyl.rotateAboutCenter((1, 0, 0), 90)
    # Position at the face center
    cyl = cyl.translate(center)
    cylinders.append(cyl)

# Combine all cylinders
all_cylinders = cylinders[0]
for cyl in cylinders[1:]:
    all_cylinders = all_cylinders.union(cyl)

# Create the internal solid as a combination of inner cube and cylinders
internal_solid = inner_cube.union(all_cylinders)

# Merge the internal and external solids
result = outer_shell.union(internal_solid)
