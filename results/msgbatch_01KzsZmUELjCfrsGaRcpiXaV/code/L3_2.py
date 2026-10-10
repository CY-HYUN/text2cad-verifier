import cadquery as cq
import math

# Create the base rectangular prism
base = cq.Workplane("XY").box(100, 3, 50, centered=False)
base = base.translate((0, -3, 0))  # Position so top surface is at Y=0

# Create the sinusoidal fin as a swept surface
# The fin profile follows Y = 5*sin(2*pi*X/20) + 5
# Amplitude = 5mm, wavelength = 20mm, vertical offset = 5mm
# 5 complete cycles over 100mm length

# Create high-resolution points for the sinusoidal curve
num_points = 200
x_coords = [i * 100 / num_points for i in range(num_points + 1)]

# Create the centerline of the fin (the sinusoidal curve in XY plane)
centerline_points = []
for x in x_coords:
    y = 5 * math.sin(2 * math.pi * x / 20) + 5
    centerline_points.append((x, y))

# Create the fin by using a wire and then creating a thin shell
# Build outer surface points (at centerline)
outer_points_z0 = [(x, y, 0) for x, y in centerline_points]
outer_points_z50 = [(x, y, 50) for x, y in centerline_points]

# Build inner surface points (offset perpendicular to curve by 0.5mm on each side = 1mm thickness)
inner_points_z0 = []
inner_points_z50 = []

for i, (x, y) in enumerate(centerline_points):
    # Calculate derivative to find normal direction
    dy_dx = 5 * (2 * math.pi / 20) * math.cos(2 * math.pi * x / 20)
    # Normal vector components (perpendicular in XY plane)
    norm_length = math.sqrt(1 + dy_dx**2)
    normal_x = -dy_dx / norm_length
    normal_y = 1 / norm_length
    # Offset by 0.5mm inward
    offset = 0.5
    inner_x = x - normal_x * offset
    inner_y = y - normal_y * offset
    inner_points_z0.append((inner_x, inner_y, 0))
    inner_points_z50.append((inner_x, inner_y, 50))

# Create the fin surface by building it from individual faces
edges = []

# Create outer surface (loft between z=0 and z=50)
outer_z0 = cq.Workplane("XY").polyline(outer_points_z0)
outer_z50 = cq.Workplane("XY").polyline(outer_points_z50)

# Create the four boundary edges
start_edge_outer = [(outer_points_z0[0], outer_points_z50[0])]
end_edge_outer = [(outer_points_z0[-1], outer_points_z50[-1])]

# Build fin as swept surface
fin_edges = []
fin_pts_sweep = []

for x in x_coords:
    y = 5 * math.sin(2 * math.pi * x / 20) + 5
    fin_pts_sweep.append((x, y))

# Create a lofted fin by sweeping the rectangular profile along the path
# Use a different approach: create rectangular cross-sections and loft them

fin_sections = []
for x in x_coords:
    y = 5 * math.sin(2 * math.pi * x / 20) + 5
    # Create a small rectangular cross-section at this X position
    section = [
        (x, y, 0),
        (x, y, 50),
        (x, y - 0.5, 50),
        (x, y - 0.5, 0)
    ]
    fin_sections.append(section)

# Build fin by creating triangular faces between consecutive sections
fin_faces = []
for i in range(len(fin_sections) - 1):
    sec1 = fin_sections[i]
    sec2 = fin_sections[i + 1]
    
    # Create faces connecting the sections
    # Outer surface
    pts_outer = [sec1[0], sec2[0], sec2[1], sec1[1]]
    # Inner surface
    pts_inner = [sec1[3], sec1[2], sec2[2], sec2[3]]
    # Front cap
    pts_front = [sec1[0], sec1[3], sec2[3], sec2[0]]
    # Back cap
    pts_back = [sec1[1], sec2[1], sec2[2], sec1[2]]

# Simpler approach: create the fin as a solid using shell construction
fin = cq.Workplane("XY")

# Create profiles at different X positions and loft them
profiles = []
for i in range(0, len(x_coords), max(1, len(x_coords) // 20)):  # Sample profiles
    x = x_coords[i]
    y = 5 * math.sin(2 * math.pi * x / 20) + 5
    # Create a vertical rectangular profile
    profile_pts = [(y, 0), (y, 50), (y - 1, 50), (y - 1, 0)]
    profiles.append(profile_pts)

# Build fin as a thick solid by creating box sections and unioning them
fin_solid = None
step = 2
for i in range(0, len(x_coords) - step, step):
    x1 = x_coords[i]
    x2 = x_coords[i + step]
    y1 = 5 * math.sin(2 * math.pi * x1 / 20) + 5
    y2 = 5 * math.sin(2 * math.pi * x2 / 20) + 5
    y_mid = (y1 + y2) / 2
    
    # Create a thin box approximating the fin section
    section = cq.Workplane("XY").box(x2 - x1, 1, 50, centered=False)
    section = section.translate((x1, y_mid - 0.5, 0))
    
    if fin_solid is None:
        fin_solid = section
    else:
        fin_solid = fin_solid.union(section)

# Combine base and fin
result = base.union(fin_solid)
