import cadquery as cq
import math

# Create the base rectangular prism
base = cq.Workplane("XY").box(100, 3, 50, centered=False)
base = base.translate((0, -3, 0))  # Position so top surface is at Y=0

# Create the sinusoidal fin
# The fin profile follows Y = 5*sin(2*pi*X/20) + 5
# Amplitude = 5mm, wavelength = 20mm, vertical offset = 5mm
# 5 complete cycles over 100mm length

# Create points for the sinusoidal profile
fin_points = []
num_points = 200  # High resolution for smooth curve
x_start = 0
x_end = 100

for i in range(num_points + 1):
    x = x_start + (x_end - x_start) * i / num_points
    y = 5 * math.sin(2 * math.pi * x / 20) + 5
    fin_points.append((x, y))

# Create the fin as a 2D profile, then extrude it
# Start with the baseline (bottom of fin at Y=0)
fin_profile_points = [(0, 0)] + fin_points + [(100, 0)]

# Create a sketch of the fin profile
fin_sketch = cq.Workplane("XY").polyline(fin_profile_points)

# Close the profile to create a closed shape
fin_2d = fin_sketch.close()

# Create a face from the profile
fin_face = cq.Face.makeFromWires(fin_sketch.val())

# Create the fin by extruding the 2D profile in the Z direction (50mm width)
# We need to create a thin-walled fin, so we'll create it as a surface
# First, create two parallel curves offset by the wall thickness (1mm)

# Create the fin by lofting between two curves (inner and outer surfaces)
fin_points_outer = []
fin_points_inner = []

for i in range(num_points + 1):
    x = x_start + (x_end - x_start) * i / num_points
    y = 5 * math.sin(2 * math.pi * x / 20) + 5
    fin_points_outer.append((x, y))

# For the inner surface, offset perpendicular to the curve
# Approximate perpendicular offset for thin wall
for i in range(num_points + 1):
    x = x_start + (x_end - x_start) * i / num_points
    y = 5 * math.sin(2 * math.pi * x / 20) + 5
    # Calculate derivative to find normal direction
    dy_dx = 5 * (2 * math.pi / 20) * math.cos(2 * math.pi * x / 20)
    # Normal vector (pointing inward)
    norm_length = math.sqrt(1 + dy_dx**2)
    normal_x = -dy_dx / norm_length
    normal_y = 1 / norm_length
    # Offset by wall thickness (1mm)
    offset = 1.0
    fin_points_inner.append((x - normal_x * offset, y - normal_y * offset))

# Build the fin as a swept surface
# Create outer edge at Z=0
outer_edge_z0 = cq.Workplane("XY").polyline(fin_points_outer)
# Create outer edge at Z=50
outer_edge_z50 = cq.Workplane("XY").polyline(fin_points_outer).translate((0, 0, 50))

# Create inner edge at Z=0
inner_edge_z0 = cq.Workplane("XY").polyline(fin_points_inner)
# Create inner edge at Z=50
inner_edge_z50 = cq.Workplane("XY").polyline(fin_points_inner).translate((0, 0, 50))

# Create the fin surface by lofting
# Build edges as wires
outer_z0_wire = outer_edge_z0.val()
outer_z50_wire = outer_edge_z50.val()
inner_z0_wire = inner_edge_z0.val()
inner_z50_wire = inner_edge_z50.val()

# Create faces between the wires and loft them
fin_solid = cq.Workplane("XY")

# Create the fin as a swept profile along the length
profile_points_z0 = fin_points_outer
profile_points_z50 = [(p[0], p[1], 50) for p in fin_points_outer]

# Create a shell by building it step by step
# Outer surface
outer_pts_3d = [(p[0], p[1], 0) for p in fin_points_outer]
fin = cq.Workplane("XY").polyline(outer_pts_3d)

# Build the fin as a solid thin shell
# Create the fin by extruding and then making it hollow
fin_workplane = cq.Workplane("XY")

# Create outer curve points in 3D
curve_outer = [(x, 5 * math.sin(2 * math.pi * x / 20) + 5, 0) for x in [x_start + (x_end - x_start) * i / num_points for i in range(num_points + 1)]]
curve_outer_z50 = [(x, y, 50) for x, y, z in curve_outer]

# Create the fin surface as a lofted solid
fin_surface = cq.Workplane("XY").polyline(curve_outer).close().workplane(offset=50).polyline(curve_outer_z50).close().loft(ruled=True)

# Simpler approach: create fin as extruded thin profile
fin_profile = cq.Workplane("XY").polyline(fin_points_outer)
fin = fin_profile.extrude(50)

# Combine base and fin
result = base.union(fin)
