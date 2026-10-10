import cadquery as cq
import math

# Create a cylinder with diameter 30mm and height 50mm
cylinder = cq.Workplane("XY").circle(15).extrude(50)

# Define the inclined plane
# The plane passes through point (-15, 0, 50) on the top surface
# It's inclined at 30° relative to horizontal, tilted along X direction
angle_rad = math.radians(30)
normal_x = math.sin(angle_rad)
normal_z = math.cos(angle_rad)

# Three points to define the cutting plane:
p1 = (-15, 0, 50)
p2 = (-15, 10, 50)
p3 = (-15 + 10 * math.cos(angle_rad), 0, 50 + 10 * math.sin(angle_rad))

# Create a plane through the three points
cutting_plane = cq.Plane.XY()
cutting_plane = cq.Plane(basePnt=p1, xDir=(0, 1, 0), normal=(normal_x, 0, normal_z))

# Split the cylinder with the plane
result = cylinder.split(cutting_plane)

# Keep only the lower part (the part that remains after cutting above the plane)
# The split returns a compound; we need to keep the piece below the plane
# We'll select the larger piece or the one with lower center of mass
result = result.faces(">Z")

# Alternative: use a box to cut away the upper part
# Create a cutting box that extends from the plane upward
result = cylinder

# Use the plane to cut - create a half-space above the plane and remove it
# Manually perform the cutting operation
bbox = cylinder.val().BoundingBox()

# Create a solid above the inclined plane using a box and transform
cutting_box = cq.Workplane("XY").box(100, 100, 100, centered=True)

# Rotate the cutting box to align with plane normal
# The plane normal is (sin(30°), 0, cos(30°))
# We need to rotate so that (0, 0, 1) aligns with (normal_x, 0, normal_z)

# Rotation axis is perpendicular to both: (0, 0, 1) × (normal_x, 0, normal_z)
# = (0*normal_z - 1*0, 1*normal_x - 0*normal_z, 0*0 - 0*normal_x) = (0, normal_x, 0) = (0, 0.5, 0)
# Rotation angle: arccos(dot product) = arccos(normal_z) = arccos(cos(30°)) = 30°

rotation_angle = 30

# Translate and rotate the cutting box
cutting_box = cutting_box.translate((p1[0], p1[1], p1[2]))
cutting_box = cutting_box.rotate((0, 0, 0), (0, 1, 0), rotation_angle)

# Cut the cylinder
result = cylinder.cut(cutting_box)
