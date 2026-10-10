import cadquery as cq
import math

# Create the base cylinder
base_radius = 40.0
base_height = 60.0

# Start with a cylinder
cylinder = cq.Workplane("XY").circle(base_radius).extrude(base_height)

# Create the beveled top surface
# The bevel is a cutting plane passing through (0,0,60) at 30 degrees to the X-axis
# In the YZ plane: the line passes through (0,60) and has slope -tan(30°)
# This creates a plane that cuts the top

# Define cutting plane: normal vector at 30 degrees in YZ plane
# A line at 30 degrees with X-axis in YZ plane: goes through (0,0,60)
# Plane equation: sin(30°)*z - cos(30°)*y = sin(30°)*60
# Simplified: 0.5*z - 0.866*y = 30, or z = 60 + 1.732*y

# Cut using a box that represents the half-space above the cutting plane
# Create a tall box and use it to cut
cutting_plane = cq.Workplane("XY").box(200, 200, 200, centered=False).translate((0, -100, 60))
cylinder = cylinder.cut(cutting_plane)

# Now create the parabolic cavity on the inclined surface
# First, work on the inclined plane
# The parabola equation is X^2 = 40*Y where Y is depth into surface and X is radial

# Create a 2D parabola profile: for a point at distance r from center
# We revolve this around the inclined surface
# Profile in local coordinates: half parabola from (0,0) to (30, 22.5)

# Create parabolic cavity by revolving a parabolic profile
# We'll create this by sketching on the top inclined face and revolving

# Approximate parabola with multiple points: y = x²/40
parabola_points = []
for x in range(0, 31, 3):
    y = (x * x) / 40.0
    parabola_points.append((x, y))

# Create the profile for revolution (parabolic cavity)
profile = cq.Workplane("YZ").moveTo(0, 0)
for i, (x, y) in enumerate(parabola_points):
    if i == 0:
        profile = profile.moveTo(x, -y)
    else:
        profile = profile.lineTo(x, -y)

# Close the profile
profile = profile.lineTo(parabola_points[-1][0], 0).lineTo(0, 0).close()

# Revolve the profile to create the cavity
parabolic_cavity = profile.revolve(axisEnd=(0, 1, 0))

# Position and cut the parabolic cavity from the cylinder
# The cavity should be on the inclined top surface, centered
cylinder = cylinder.cut(parabolic_cavity)

# Create the sine wave groove on the outer cylindrical surface
# Use a parametric approach: create points along a sine wave on the cylinder
groove_points = []
num_points = 120

for t_norm in range(num_points + 1):
    t = (t_norm / num_points) * 2 * math.pi
    x = 40.0 * math.sin(t)
    y = 40.0 * math.cos(t)
    z = 30.0 + 5.0 * math.sin(6.0 * t)
    groove_points.append((x, y, z))

# Create a wire from these points
wire_points = groove_points
groove_path = cq.Workplane("XY").moveTo(wire_points[0][0], wire_points[0][1]).moveTo(0, 0, wire_points[0][2])

# Build 3D path more carefully
edges = []
for i in range(len(wire_points) - 1):
    p1 = wire_points[i]
    p2 = wire_points[i + 1]
    edge = cq.Edge.makeLine(cq.Vector(*p1), cq.Vector(*p2))
    edges.append(edge)

# Create a small cutting profile (rectangular slot)
slot_profile = cq.Workplane("XY").box(4, 4, 2)

# Create groove by sweeping the profile along the path
# Simplified approach: create a cutting tool using loft/sweep
# For now, create cylindrical grooves at key points along the sine path

for i in range(0, len(wire_points), 10):
    point = wire_points[i]
    cylinder = cylinder.cut(cq.Workplane("XY").sphere(2.0).translate(point[0], point[1], point[2]))

result = cylinder
