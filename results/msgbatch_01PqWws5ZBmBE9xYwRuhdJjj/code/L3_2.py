import cadquery as cq
import math

# Create the base plate
base = cq.Workplane("XY").rect(100, 50).extrude(3.0)

# Get the top surface of the base plate for the next sketch
top_face = base.faces(">Z").first()

# Create a workplane on the top surface
sketch_plane = cq.Workplane("XY").workplane(offset=3.0)

# Create parametric sine curve using edge construction
# We'll create points along the parametric equation and connect them
points = []
t_values = [i for i in range(0, 101)]  # t from 0 to 100
for t in t_values:
    x = t
    y = 5 * math.sin(2 * math.pi * t / 20)
    points.append((x, y))

# Create the main sine curve
sine_curve = sketch_plane.polyline(points)

# Create offset curve (1.0mm offset in Y direction - perpendicular to local curve)
# For simplicity, we'll offset by moving points perpendicular to the sine wave
offset_points = []
for t in t_values:
    x = t
    y = 5 * math.sin(2 * math.pi * t / 20) + 1.0  # Simple offset
    offset_points.append((x, y))

# Reverse the offset points to create the closing path
offset_points_reversed = list(reversed(offset_points))

# Create closed profile by combining original curve, offset curve, and closing lines
closed_profile_points = points + offset_points_reversed + [points[0]]

# Create the sketch on the top surface
sketch = (sketch_plane
    .polyline(closed_profile_points)
    .close())

# Extrude the closed sine wave profile 50mm in Z direction (width direction)
corrugated_profile = sketch.extrude(50.0, combine=True)

# Merge with base plate
result = base.union(corrugated_profile)
