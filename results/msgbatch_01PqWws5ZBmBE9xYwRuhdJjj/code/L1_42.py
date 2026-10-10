import cadquery as cq
import math

# Create a cylinder with diameter 30mm and height 50mm
cylinder = cq.Workplane("XY").circle(15).extrude(50)

# Define the inclined plane
# The plane passes through point (-15, 0, 50) on the top surface
# It's inclined at 30° relative to horizontal, tilted along X direction
# The plane equation: for a plane tilted 30° along X-axis through point (-15, 0, 50)
# The normal vector to the plane (tilted 30° from horizontal along X):
# - Horizontal plane has normal (0, 0, 1)
# - Tilted 30° along X means rotating around Y-axis by 30°
# - Normal becomes: (sin(30°), 0, cos(30°)) = (0.5, 0, √3/2)

angle_rad = math.radians(30)
normal_x = math.sin(angle_rad)
normal_z = math.cos(angle_rad)

# Point on plane: (-15, 0, 50)
point_x, point_y, point_z = -15, 0, 50

# Plane equation: normal_x * (x - point_x) + normal_z * (z - point_z) = 0
# 0.5 * (x + 15) + (√3/2) * (z - 50) = 0
# To cut above the plane, we need to find which direction is "above"
# We'll create a bounding box and cut with a plane

# Create a large box to represent the half-space above the inclined plane
# We need to cut the material above the plane
# Create the cutting plane by defining it through three points

# Three points to define the cutting plane:
# Point 1: (-15, 0, 50) - the pivot point
# Point 2: A point along the Y-axis at the same height: (0, 10, 50) translated appropriately
# Point 3: A point higher in Z direction along the tilted plane

# For a plane tilted 30° along X through (-15, 0, 50):
# Point along Y direction (perpendicular to tilt): (-15, 10, 50)
# Point along the tilt direction: we go in +X direction and adjust Z by tan(30°)
p1 = (-15, 0, 50)
p2 = (-15, 10, 50)  # Along Y-axis
p3 = (-15 + 10 * math.cos(angle_rad), 0, 50 + 10 * math.sin(angle_rad))  # Along the incline

# Create a large box that extends well beyond the cylinder
large_box = cq.Workplane("XY").box(100, 100, 100, centered=False).translate((-50, -50, 0))

# Use the plane defined by three points to split
# We'll create a plane and use it to cut the cylinder
# The material to remove is above the plane (higher Z values relative to plane)

# Create a cutting tool - a half-space defined by the plane
# Using CadQuery's split operation with a plane
result = cylinder.split(cq.Plane.XY().rotated((0, 1, 0), 30).offset(p1))

# Alternative approach: use transformed operations
# Create a wedge/cutting object aligned with the plane
# Rotate the cylinder so the plane becomes horizontal, cut, then rotate back

# Simpler approach: manually create the cut
# Translate so the plane passes through origin, tilt it, cut with XY plane, rotate back

result = cylinder.transformed(rotate=(0, 0, 0))

# Perform the cut using a plane definition
# Create working plane at the incline
result = cylinder.split(cq.Plane(basePnt=p1, xDir=(0, 1, 0), normal=(normal_x, 0, normal_z)))
