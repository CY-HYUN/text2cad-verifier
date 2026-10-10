import cadquery as cq
import math

# Create the base cylinder
# Circle with diameter 50 mm (radius 25 mm), extruded 100 mm along Z-axis
base_cylinder = cq.Workplane("XY").circle(25).extrude(100)

# Get the cylindrical face (side surface) for the wrap operation
cylindrical_face = base_cylinder.faces(">Z").objects[0]  # Get top face to reference
# Actually, we need the side face
side_faces = base_cylinder.faces(">>Z").objects if len(base_cylinder.faces(">>Z").objects) > 0 else []
# Better approach: get cylindrical face by normal direction
cylinder_faces = [f for f in base_cylinder.faces() if f.geomType() == "CYLINDER"]

if len(cylinder_faces) > 0:
    target_face = cylinder_faces[0]
else:
    target_face = base_cylinder.faces(">Z").objects[0]

# Create the unwrapped rectangle sketch
# Width = 100 (height of cylinder), Length = π × 50 (circumference)
circumference = math.pi * 50
unwrap_length = circumference
unwrap_height = 100

# Create sketch on XZ plane for the unwrapped pattern
sketch_plane = cq.Workplane("XZ")

# Create a rectangle representing the unwrapped surface
# Then add the sine curve with offset

# Build the sine curve path
points = []
num_points = 200
x_start = 0
x_end = unwrap_length

for i in range(num_points):
    x = x_start + (x_end - x_start) * i / (num_points - 1)
    # Sine curve: Y = 15 * sin(k * X) + 50, where k relates to frequency
    k = 2 * math.pi / unwrap_length  # Complete one sine wave across the circumference
    y = 15 * math.sin(k * x) + 50
    points.append((x, y))

# Create upper and lower offset curves (±4mm offset = 8mm total groove width)
offset_dist = 4.0

upper_points = []
lower_points = []

for i, (x, y) in enumerate(points):
    upper_points.append((x, y + offset_dist))
    lower_points.append((x, y - offset_dist))

# Create the sketch with the sine curve and offsets
sketch = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(unwrap_length, 0)
    .lineTo(unwrap_length, unwrap_height)
    .lineTo(0, unwrap_height)
    .close()
)

# Create a face sketch with the sine wave groove profile
groove_sketch = cq.Workplane("XZ")

# Draw the closed groove profile (sine curve with offsets)
# Start at beginning of upper offset curve
groove_sketch = groove_sketch.moveTo(upper_points[0][0], upper_points[0][1])

# Trace upper curve
for x, y in upper_points[1:]:
    groove_sketch = groove_sketch.lineTo(x, y)

# Trace lower curve in reverse
for x, y in reversed(lower_points):
    groove_sketch = groove_sketch.lineTo(x, y)

# Close the path
groove_sketch = groove_sketch.close()

# Create a 3D shape from the sketch
groove_profile = groove_sketch.extrude(1)  # Thin extrusion for wrapping

# Use wrap operation by creating cut geometry
# For this implementation, we'll create the groove by cutting the sine pattern from the cylinder

# Create a workplane on the cylinder and project the sine curve
# Build the grooved cylinder by cutting the sine wave pattern
result = base_cylinder

# Create the sine wave as a face to cut
wrap_sketch = cq.Workplane("XY").center(0, 0)

# Create multiple vertical planes at angles around the cylinder
# and cut the sine pattern projected onto the surface
for angle_deg in range(0, 360, 5):
    angle_rad = math.radians(angle_deg)
    
    # Local position on unwrapped surface
    local_x = angle_deg * math.pi * 50 / 360  # Maps angle to position on unwrapped surface
    k = 2 * math.pi / (math.pi * 50)
    groove_depth = 15 * math.sin(k * local_x) + 50
    
    # Cut the groove
    cut_profile = (
        cq.Workplane("YZ")
        .moveTo(groove_depth - offset_dist, 0)
        .lineTo(groove_depth + offset_dist, 0)
        .lineTo(groove_depth + offset_dist, 100)
        .lineTo(groove_depth - offset_dist, 100)
        .close()
        .extrude(10)
    )
    result = result.cut(cut_profile)

result = base_cylinder
