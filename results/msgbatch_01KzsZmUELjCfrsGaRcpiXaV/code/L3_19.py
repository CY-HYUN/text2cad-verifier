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

# Create 3D spiral wall by building it layer by layer
# Create the spiral wall as a lofted solid between bottom and top profiles

# Bottom profile (at z=10)
bottom_inner = [(20 + 3.5*theta) * math.cos(theta), (20 + 3.5*theta) * math.sin(theta), 10) for theta in theta_values]
bottom_outer = [(20 + 3.5*theta + 4) * math.cos(theta), (20 + 3.5*theta + 4) * math.sin(theta), 10) for theta in theta_values]

# Top profile (at z=35)
top_inner = [(20 + 3.5*theta) * math.cos(theta), (20 + 3.5*theta) * math.sin(theta), 35) for theta in theta_values]
top_outer = [(20 + 3.5*theta + 4) * math.cos(theta), (20 + 3.5*theta + 4) * math.sin(theta), 35) for theta in theta_values]

# Create a polygon for the spiral cross-section at each point
# Build the spiral wall using wire extrusion

# Create bottom inner wire
bottom_inner_wire_pts = [((20 + 3.5*theta) * math.cos(theta), (20 + 3.5*theta) * math.sin(theta)) for theta in theta_values]
bottom_outer_wire_pts = [((20 + 3.5*theta + 4) * math.cos(theta), (20 + 3.5*theta + 4) * math.sin(theta)) for theta in theta_values]

# Create the spiral wall as a swept surface
# Use a different approach: create rectangular sections and loft them

sections = []
num_sections = 40

for i in range(num_sections + 1):
    t = i / num_sections
    theta = t * 3 * math.pi
    r_inner = 20 + 3.5 * theta
    r_outer = r_inner + 4
    
    x_inner = r_inner * math.cos(theta)
    y_inner = r_inner * math.sin(theta)
    x_outer = r_outer * math.cos(theta)
    y_outer = r_outer * math.sin(theta)
    
    # Create a rectangular profile at this theta position
    pts = [
        (x_inner, y_inner, 10),
        (x_outer, y_outer, 10),
        (x_outer, y_outer, 35),
        (x_inner, y_inner, 35),
    ]
    sections.append(pts)

# Build faces connecting consecutive sections
spiral_wall = cq.Workplane("XY")
edges = []

for i in range(len(sections) - 1):
    pts1 = sections[i]
    pts2 = sections[i + 1]
    
    # Inner surface
    inner_pts = [pts1[0], pts2[0], pts2[3], pts1[3]]
    # Outer surface
    outer_pts = [pts1[1], pts2[1], pts2[2], pts1[2]]
    
    # Add to edges list for creating faces
    for p in inner_pts:
        edges.append(p)
    for p in outer_pts:
        edges.append(p)

# Create spiral wall shell - build it as a solid extrusion
wp = cq.Workplane("XY")

# Create bottom profile as a closed wire
bottom_profile_pts = []
for theta in theta_values:
    r_inner = 20 + 3.5 * theta
    r_outer = r_inner + 4
    bottom_profile_pts.append(((r_inner * math.cos(theta), r_inner * math.sin(theta))))

bottom_profile_outer_pts = []
for theta in theta_values:
    r_inner = 20 + 3.5 * theta
    r_outer = r_inner + 4
    bottom_profile_outer_pts.append(((r_outer * math.cos(theta), r_outer * math.sin(theta))))

# Create annular region and extrude upward
spiral_wall = cq.Workplane("XY").polyline(bottom_profile_outer_pts).close().polyline(bottom_profile_pts[::-1]).close().extrude(25)

# Create exhaust hole at center
hole = cq.Workplane("XY").circle(4).extrude(-10)

# Combine base and spiral wall
result = base.union(spiral_wall).cut(hole)

# Add fillet at edges
result = result.edges("|Z").fillet(2)
