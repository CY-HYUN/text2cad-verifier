import cadquery as cq
import math

# Create the base plate
base = cq.Workplane("XY").rect(100, 50).extrude(3.0)

# Create parametric sine curve points
points = []
t_values = [i * 0.5 for i in range(0, 201)]  # t from 0 to 100 with finer resolution
for t in t_values:
    x = t
    y = 5 * math.sin(2 * math.pi * t / 20)
    points.append((x, y))

# Create offset curve (1.0mm offset perpendicular to the sine wave)
# For a parametric curve, perpendicular offset requires calculating the normal
offset_points = []
for t in t_values:
    x = t
    y = 5 * math.sin(2 * math.pi * t / 20)
    # Approximate perpendicular offset using derivative
    dy_dt = 5 * 2 * math.pi / 20 * math.cos(2 * math.pi * t / 20)
    dx_dt = 1.0
    # Normal vector (perpendicular to tangent)
    norm_length = math.sqrt(dx_dt**2 + dy_dt**2)
    normal_x = -dy_dt / norm_length
    normal_y = dx_dt / norm_length
    # Offset point
    offset_x = x + normal_x * 1.0
    offset_y = y + normal_y * 1.0
    offset_points.append((offset_x, offset_y))

# Create closed profile: start curve + offset curve reversed + closing lines
closed_profile_points = points + list(reversed(offset_points))

# Create workplane on top of base plate
wp = cq.Workplane("XY").workplane(offset=3.0)

# Create a face from the closed profile
face = wp.polyline(closed_profile_points).close().extrude(50.0)

# Union the corrugated section with the base
result = base.union(face)
