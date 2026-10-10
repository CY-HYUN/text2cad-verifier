import cadquery as cq
import math

# Create a cube: 50mm x 50mm x 50mm
cube = cq.Workplane("XY").box(50, 50, 50)

# Translate cube so one corner is at origin for easier corner removal
cube = cube.translate((25, 25, 25))

# Define the corner to be cut (at coordinates (50, 50, 50) in the translated cube)
# which corresponds to (50 + 25, 50 + 25, 50 + 25) = (75, 75, 75) in world coords
# Actually, let's work with the cube centered at origin first, then adjust
cube = cq.Workplane("XY").box(50, 50, 50)

# Now the cube goes from -25 to 25 in all directions
# Select the corner at (25, 25, 25)
# Measure 15mm along each adjacent edge from this corner:
# Point 1: (25-15, 25, 25) = (10, 25, 25)
# Point 2: (25, 25-15, 25) = (25, 10, 25)
# Point 3: (25, 25, 25-15) = (25, 25, 10)

# Define three points that form the cutting plane
p1 = (10, 25, 25)
p2 = (25, 10, 25)
p3 = (25, 25, 10)

# Calculate normal vector to the plane using cross product
# Vector from p1 to p2
v1 = (p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2])  # (15, -15, 0)
# Vector from p1 to p3
v2 = (p3[0] - p1[0], p3[1] - p1[1], p3[2] - p1[2])  # (15, 0, -15)

# Cross product v1 x v2
normal = (
    v1[1] * v2[2] - v1[2] * v2[1],  # (-15)*(-15) - 0*0 = 225
    v1[2] * v2[0] - v1[0] * v2[2],  # 0*15 - 15*(-15) = 225
    v1[0] * v2[1] - v1[1] * v2[0]   # 15*0 - (-15)*15 = 225
)  # (225, 225, 225) -> normalize direction is (1, 1, 1)

# Normalize
norm_length = math.sqrt(normal[0]**2 + normal[1]**2 + normal[2]**2)
normal = (normal[0]/norm_length, normal[1]/norm_length, normal[2]/norm_length)

# Create cutting plane by using split with a plane
# The plane passes through p1 with normal pointing outward from corner
# Cut using a larger box to remove the corner region
# Create a cutting box that removes everything beyond the plane
# Plane equation: (x-10)*1 + (y-25)*(-1) + (z-25)*(-1) = 0
# Simplified: x - y - z + 40 = 0
# Or: normal · (point - p1) = 0

# Use CadQuery's split and cut functionality
# Create a half-space by using a cutting tool
# We'll create a box that represents the portion to remove
cutting_box = cq.Workplane("XY").box(20, 20, 20).translate((31.67, 31.67, 31.67))

# Perform the cut
result = cube.cut(cutting_box)
