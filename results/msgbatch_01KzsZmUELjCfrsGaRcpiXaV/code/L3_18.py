import cadquery as cq
import math

# Create the base ellipsoid
a = 40  # semi-minor axis (horizontal radius)
b = 60  # semi-major axis (vertical radius)

# Create a simple ellipsoid by revolving an ellipse
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
solid = cq.Workplane("XZ").spline(profile_points).revolve(360, (0, 0, 1))

# Inner ellipsoid with wall thickness of 3mm
inner_a = a - 3
inner_b = b - 3

inner_profile_points = []
for i in range(101):
    t = i / 100 * math.pi
    x = inner_a * math.cos(t)
    z = inner_b * math.sin(t)
    inner_profile_points.append((x, z))

inner_solid = cq.Workplane("XZ").spline(inner_profile_points).revolve(360, (0, 0, 1))

# Create hollow ellipsoid
hollow_ellipsoid = solid.cut(inner_solid)

# Create 12 longitudinal ribs
num_ribs = 12
rib_width = 4
rib_height = 120

ribs_union = None
for i in range(num_ribs):
    angle = (i / num_ribs) * 360
    # Create a rib as a rectangular box
    rib_box = cq.Workplane("XY").box(rib_width, rib_height, 3, centered=True)
    rib_box = rib_box.rotate((0, 0, 0), (0, 0, 1), angle)
    if ribs_union is None:
        ribs_union = rib_box
    else:
        ribs_union = ribs_union.union(rib_box)

# Create 3 latitudinal rings at z = -30, 0, +30
ring_width = 4
ring_radius = a + 10
ring_positions = [-30, 0, 30]

rings_union = None
for z_pos in ring_positions:
    # Create ring using a cylinder that we'll intersect
    ring = cq.Workplane("XY").cylinder(ring_width, ring_radius, centered=True)
    ring = ring.translate((0, 0, z_pos))
    if rings_union is None:
        rings_union = ring
    else:
        rings_union = rings_union.union(ring)

# Combine ribs and rings
lattice_structure = ribs_union.union(rings_union)

# Intersect lattice structure with hollow ellipsoid to create the latticed pattern
lattice = hollow_ellipsoid.intersect(lattice_structure)

# Cut off the bottom (below z = -50)
cutting_plane = cq.Workplane("XY").box(300, 300, 20, centered=True).translate((0, 0, -60))
result = lattice.cut(cutting_plane)

# Create the 10mm diameter hole at the top for wiring
hole = cq.Workplane("XY").circle(5).extrude(30, both=True)
result = result.cut(hole)
