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
# The curve is tangent to the axis at both ends
# Control points for the Bezier curve in 2D (distance from axis vs axial position)
# P0: inlet (0, inlet_radius) - tangent to axis means the curve should start horizontally
# P1: (tangent_control_arm, inlet_radius) - control point for tangent direction at inlet
# P2: (converging_length - tangent_control_arm, throat_radius) - control point for tangent at throat
# P3: (converging_length, throat_radius) - throat point, tangent to axis

def bezier_point(t, p0, p1, p2, p3):
    """Calculate a point on a cubic Bezier curve"""
    mt = 1 - t
    return (mt**3 * p0 + 3 * mt**2 * t * p1 + 3 * mt * t**2 * p2 + t**3 * p3)

# Create converging section profile (2D curve)
converging_points = []
for i in range(101):
    t = i / 100.0
    # Axial position
    x = bezier_point(t, 0, tangent_control_arm, converging_length - tangent_control_arm, converging_length)
    # Radial position
    r = bezier_point(t, inlet_radius, inlet_radius, throat_radius, throat_radius)
    converging_points.append((x, r))

# Create diverging section using paraboloid
# Vertex at throat center, opening towards exit
# Using parabola equation: r = sqrt(4*p*(x-vertex))
# At x = diverging_length, r = exit_radius
# Vertex at x = 0 (throat), r = throat_radius
# Parabola: (r - throat_radius)^2 = 4*p*x, where p is the focal parameter
# At x = diverging_length: (exit_radius - throat_radius)^2 = 4*p*diverging_length
p_param = (exit_radius - throat_radius)**2 / (4 * diverging_length)

diverging_points = []
for i in range(101):
    t = i / 100.0
    x = converging_length + t * diverging_length
    # Parabola equation
    r_offset = math.sqrt(4 * p_param * (t * diverging_length))
    r = throat_radius + r_offset
    diverging_points.append((x, r))

# Combine profiles
all_profile_points = converging_points + diverging_points[1:]  # Skip first point of diverging to avoid duplicate

# Create inner surface by revolving the profile
inner_profile = cq.Workplane("XY").spline(
    [(pt[0], 0, pt[1]) for pt in all_profile_points],
    includeCurrent=False
)

inner_surface = inner_profile.revolve(360, (0, 0, 1), (0, 0, 0))

# Create outer surface (offset outward by wall thickness)
outer_profile_points = []
for x, r in all_profile_points:
    # Offset radially outward by wall thickness
    outer_profile_points.append((x, 0, r + wall_thickness))

outer_profile = cq.Workplane("XY").spline(
    outer_profile_points,
    includeCurrent=False
)

outer_surface = outer_profile.revolve(360, (0, 0, 1), (0, 0, 0))

# Create the solid model by taking the difference
# We need to close the ends and create a proper solid
inlet_plane = (0, 0, 0)
outlet_plane = (converging_length + diverging_length, 0, 0)

# Build solid by creating two cylinders at ends and the revolved surfaces
# Create inlet end cap
inlet_inner_cylinder = cq.Workplane("XY").circle(inlet_radius).extrude(0.1)
inlet_outer_cylinder = cq.Workplane("XY").circle(inlet_radius + wall_thickness).extrude(0.1)

# Create outlet end cap  
outlet_inner_cylinder = cq.Workplane("XY").workplane(offset=converging_length + diverging_length).circle(exit_radius).extrude(0.1)
outlet_outer_cylinder = cq.Workplane("XY").workplane(offset=converging_length + diverging_length).circle(exit_radius + wall_thickness).extrude(0.1)

# Create the nozzle solid using loft between inner and outer profiles
# Build from scratch with proper solid
inner_pts = [(pt[0], pt[1], 0) for pt in all_profile_points]
outer_pts = [(pt[0], pt[1] + wall_thickness, 0) for pt in all_profile_points]

# Create a solid nozzle by revolving the annular profile
profile_2d = [
    (all_profile_points[0][0], all_profile_points[0][1]),
    *all_profile_points[1:-1],
    (all_profile_points[-1][0], all_profile_points[-1][1]),
    (all_profile_points[-1][0], all_profile_points[-1][1] + wall_thickness),
    *[(pt[0], pt[1] + wall_thickness) for pt in all_profile_points[-2:0:-1]],
    (all_profile_points[0][0], all_profile_points[0][1] + wall_thickness),
]

# Simpler approach: create by revolving an annular profile
base = cq.Workplane("XZ")
for i, (x, r) in enumerate(all_profile_points):
    if i == 0:
        base = base.moveTo(x, r)
    else:
        base = base.lineTo(x, r)

# Add outer profile line back
for i in range(len(all_profile_points)-1, -1, -1):
    x, r = all_profile_points[i]
    base = base.lineTo(x, r + wall_thickness)

# Close the profile
base = base.close()
result = base.revolve(360, (0, 0, 1))
