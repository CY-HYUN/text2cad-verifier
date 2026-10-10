import cadquery as cq
import math

# Create the base ellipsoid
a = 40  # semi-minor axis (horizontal radius)
b = 60  # semi-major axis (vertical radius)

# Create a simple ellipsoid by revolving an ellipse
# First, create half ellipse profile in XZ plane
def create_ellipse_profile(num_points=100):
    points = []
    for i in range(num_points + 1):
        t = i / num_points * math.pi
        x = a * math.cos(t)
        z = b * math.sin(t)
        points.append((x, z))
    return points

profile_points = create_ellipse_profile(100)

# Create the solid ellipsoid by revolution
solid = cq.Workplane("XZ").spline(profile_points, forceD=True).revolve(360, (0, 0, 1))

# Create the hollow ellipsoid by creating outer and inner surfaces
# Inner ellipsoid with wall thickness of 3mm
inner_a = a - 3
inner_b = b - 3

inner_profile_points = []
for i in range(101):
    t = i / 100 * math.pi
    x = inner_a * math.cos(t)
    z = inner_b * math.sin(t)
    inner_profile_points.append((x, z))

inner_solid = cq.Workplane("XZ").spline(inner_profile_points, forceD=True).revolve(360, (0, 0, 1))

# Create hollow ellipsoid
hollow_ellipsoid = solid.cut(inner_solid)

# Create 12 longitudinal ribs
num_ribs = 12
rib_width = 4
rib_thickness = 3

ribs = cq.Workplane("XY")
for i in range(num_ribs):
    angle = (i / num_ribs) * 360
    # Create a rib as a rectangular box that follows the ellipse
    rib_box = cq.Workplane("XY").box(rib_width, 200, rib_thickness, centered=True)
    rib_box = rib_box.rotate((0, 0, 0), (0, 0, 1), angle)
    if i == 0:
        ribs = rib_box
    else:
        ribs = ribs.union(rib_box)

# Create 3 latitudinal rings at z = -30, 0, +30
ring_width = 4
ring_positions = [-30, 0, 30]
rings = cq.Workplane("XY")

for z_pos in ring_positions:
    # Create ring as a torus-like structure
    # Using a rectangular profile revolved around z-axis
    ring_box = cq.Workplane("XY").box(2*a + 10, 2*a + 10, ring_width, centered=True)
    ring_box = ring_box.translate((0, 0, z_pos))
    if z_pos == ring_positions[0]:
        rings = ring_box
    else:
        rings = rings.union(ring_box)

# Intersect ribs and rings with the hollow ellipsoid to get lattice structure
# Create lattice by intersecting the union of ribs and rings with the ellipsoid
lattice_structure = ribs.union(rings)
lattice = hollow_ellipsoid.intersect(lattice_structure)

# Cut off the bottom (below z = -50)
cutting_box = cq.Workplane("XY").box(200, 200, 20, centered=True).translate((0, 0, -60))
result_with_opening = lattice.cut(cutting_box)

# Create the 10mm diameter hole at the top
hole = cq.Workplane("XY").circle(5).extrude(20, both=True).translate((0, 0, 65))
result = result_with_opening.cut(hole)

# Final result
result = result_with_opening.cut(cq.Workplane("XY").circle(5).extrude(30, both=True).translate((0, 0, 0)))
