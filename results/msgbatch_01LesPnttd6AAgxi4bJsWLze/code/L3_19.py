import cadquery as cq
import math

# Create the circular base
base = cq.Workplane("XY").circle(60).extrude(10)

# Create the Archimedean spiral wall
# Spiral equation: r = 20 + 3.5*theta
# theta from 0 to 3*pi
# Wall height: 25mm, thickness: 4mm

# Generate spiral points
num_points = 300
theta_values = [i * 3 * math.pi / (num_points - 1) for i in range(num_points)]

# Create spiral profile (2D points for the inner and outer edges of the wall)
spiral_points_inner = []
spiral_points_outer = []

for theta in theta_values:
    r_inner = 20 + 3.5 * theta
    r_outer = r_inner + 4  # wall thickness
    
    x_inner = r_inner * math.cos(theta)
    y_inner = r_inner * math.sin(theta)
    x_outer = r_outer * math.cos(theta)
    y_outer = r_outer * math.sin(theta)
    
    spiral_points_inner.append((x_inner, y_inner))
    spiral_points_outer.append((x_outer, y_outer))

# Create the spiral wall by lofting
# First, create a 2D profile at the base
base_profile_inner = cq.Workplane("XY").polyline(spiral_points_inner).close()
base_profile_outer = cq.Workplane("XY").polyline(spiral_points_outer).close()

# Create spiral as a 3D shape by creating multiple cross-sections
# We'll use a different approach: create the spiral as a swept surface

# Create the center line of the spiral
center_line_points = []
for theta in theta_values:
    r = 20 + 3.5 * theta + 2  # middle of wall
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    z = 10  # starting from top of base
    center_line_points.append((x, y, z))

# Create spiral wall using extrusion along a path
# Start with a rectangular profile (wall cross-section: 4mm wide, 25mm tall)
wall_height = 25
wall_thickness = 4

# Create the spiral using loft approach with multiple sections
sections = []
num_sections = 30

for i in range(num_sections + 1):
    t = i / num_sections
    theta = t * 3 * math.pi
    r_mid = 20 + 3.5 * theta
    r_inner = r_mid - wall_thickness / 2
    r_outer = r_mid + wall_thickness / 2
    
    # Create a vertical profile at this theta
    x_inner_base = r_inner * math.cos(theta)
    y_inner_base = r_inner * math.sin(theta)
    x_outer_base = r_outer * math.cos(theta)
    y_outer * math.sin(theta)
    x_inner_top = r_inner * math.cos(theta)
    y_inner_top = r_inner * math.sin(theta)
    x_outer_top = r_outer * math.cos(theta)
    y_outer_top = r_outer * math.sin(theta)
    
    # Create section profile
    section_points = [
        (x_inner_base, y_inner_base, 10),
        (x_outer_base, y_outer_base, 10),
        (x_outer_top, y_outer_top, 35),
        (x_inner_top, y_inner_top, 35),
    ]
    
    section = cq.Workplane("XY").polyline(section_points).close().extrude(0.1)
    sections.append(section)

# Build the spiral wall using sweep with profiles
spiral_wall = cq.Workplane("XY")
wall_faces = []

for i in range(len(theta_values) - 1):
    theta1 = theta_values[i]
    theta2 = theta_values[i + 1]
    
    r1_inner = 20 + 3.5 * theta1
    r1_outer = r1_inner + 4
    r2_inner = 20 + 3.5 * theta2
    r2_outer = r2_inner + 4
    
    # Create quad faces for inner and outer surfaces
    p1_in = (r1_inner * math.cos(theta1), r1_inner * math.sin(theta1), 10)
    p2_in = (r1_inner * math.cos(theta1), r1_inner * math.sin(theta1), 35)
    p3_in = (r2_inner * math.cos(theta2), r2_inner * math.sin(theta2), 35)
    p4_in = (r2_inner * math.cos(theta2), r2_inner * math.sin(theta2), 10)
    
    p1_out = (r1_outer * math.cos(theta1), r1_outer * math.sin(theta1), 10)
    p2_out = (r1_outer * math.cos(theta1), r1_outer * math.sin(theta1), 35)
    p3_out = (r2_outer * math.cos(theta2), r2_outer * math.sin(theta2), 35)
    p4_out = (r2_outer * math.cos(theta2), r2_outer * math.sin(theta2), 10)

# Simplified approach: create solid spiral using loft
spiral_inner = []
spiral_outer = []
spiral_heights = [10, 35]  # bottom and top

for z in spiral_heights:
    inner_pts = [(20 + 3.5*theta)*math.cos(theta), (20 + 3.5*theta)*math.sin(theta)) for theta in theta_values]
    outer_pts = [(20 + 3.5*theta + 4)*math.cos(theta), (20 + 3.5*theta + 4)*math.sin(theta)) for theta in theta_values]

# Create spiral wall as a solid of revolution combined with proper geometry
wp = cq.Workplane("XY")
spiral_wall = wp.workplane(offset=10).polyline(spiral_points_inner).polyline(spiral_points_outer[::-1]).close().extrude(25)

# Create exhaust hole at center
hole = cq.Workplane("XY").circle(4).extrude(-10)

# Combine base and spiral wall
result = base.union(spiral_wall).cut(hole)

# Add fillet at the end of the spiral (R2 fillet)
result = result.edges("|Z").fillet(2)
