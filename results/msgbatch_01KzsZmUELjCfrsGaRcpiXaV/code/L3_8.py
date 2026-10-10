import cadquery as cq
import math

# Parameters
inlet_diameter = 50
throat_diameter = 20
exit_diameter = 60
converging_length = 30
diverging_length = 50
wall_thickness = 3
tangent_control_arm = 15

inlet_radius = inlet_diameter / 2
throat_radius = throat_diameter / 2
exit_radius = exit_diameter / 2

# Create converging section using cubic Bezier curve
def bezier_point(t, p0, p1, p2, p3):
    """Calculate a point on a cubic Bezier curve"""
    mt = 1 - t
    return (mt**3 * p0 + 3 * mt**2 * t * p1 + 3 * mt * t**2 * p2 + t**3 * p3)

# Create converging section profile (2D curve)
converging_points = []
for i in range(101):
    t = i / 100.0
    x = bezier_point(t, 0, tangent_control_arm, converging_length - tangent_control_arm, converging_length)
    r = bezier_point(t, inlet_radius, inlet_radius, throat_radius, throat_radius)
    converging_points.append((x, r))

# Create diverging section using parabola of revolution
p_param = (exit_radius - throat_radius)**2 / (4 * diverging_length)

diverging_points = []
for i in range(101):
    t = i / 100.0
    x = converging_length + t * diverging_length
    r_offset = math.sqrt(4 * p_param * (t * diverging_length))
    r = throat_radius + r_offset
    diverging_points.append((x, r))

# Combine profiles
all_profile_points = converging_points + diverging_points[1:]

# Create the nozzle by revolving the annular profile around the axis
# Build profile in XZ plane: inner surface, then outer surface back
profile_points_xz = []

# Inner surface (inlet to outlet)
for x, r in all_profile_points:
    profile_points_xz.append((x, r))

# Outer surface (outlet back to inlet)
for x, r in reversed(all_profile_points):
    profile_points_xz.append((x, r + wall_thickness))

# Create a face by sketching the profile and revolving
base = cq.Workplane("XZ")
base = base.moveTo(profile_points_xz[0][0], profile_points_xz[0][1])

for point in profile_points_xz[1:]:
    base = base.lineTo(point[0], point[1])

# Close the profile
base = base.close()

# Revolve around the Z-axis to create the 3D solid
result = base.revolve(360, (0, 0, 1))
