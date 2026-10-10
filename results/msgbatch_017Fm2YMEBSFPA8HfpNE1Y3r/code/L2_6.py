import cadquery as cq
import math

# Create a cylinder with diameter 30 mm and height 80 mm
cylinder = cq.Workplane("XY").circle(15).extrude(80)

# Create the helix path
# Helix parameters: radius = 15 mm, pitch = 20 mm, 4 turns
radius = 15
pitch = 20
turns = 4
total_height = pitch * turns  # 80 mm

# Generate helix points
helix_points = []
num_points = 200
for i in range(num_points + 1):
    t = i / num_points
    angle = t * turns * 2 * math.pi
    x = radius * math.cos(angle)
    y = radius * math.sin(angle)
    z = t * total_height
    helix_points.append((x, y, z))

# Create the helix as a wire
helix_edges = []
for i in range(len(helix_points) - 1):
    pt1 = cq.Vector(*helix_points[i])
    pt2 = cq.Vector(*helix_points[i + 1])
    helix_edges.append(cq.Edge.makeLine(pt1, pt2))

helix_wire = cq.Wire.assembleEdges(helix_edges)

# Get the starting point of the helix
start_point = cq.Vector(*helix_points[0])

# Create a reference plane perpendicular to the helix at the starting point
# The helix tangent at start point
tangent_angle = turns * 2 * math.pi / num_points
tangent_x = -radius * math.sin(0) * tangent_angle
tangent_y = radius * math.cos(0) * tangent_angle
tangent_z = total_height / num_points

tangent = cq.Vector(tangent_x, tangent_y, tangent_z).normalized()

# Normal to the cylinder surface at start point (radial direction)
normal_radial = cq.Vector(math.cos(0), math.sin(0), 0)

# Create semicircle profile in the perpendicular plane
# Semicircle with radius 2 mm, straight edge against cylinder surface
semicircle_radius = 2

# Draw semicircle: straight edge is tangent to cylinder, arc points inward
# Create local coordinate system where x is inward, y is along tangent
arc_points = []
for i in range(101):
    angle = i * math.pi / 100
    # Local x is along the inward direction, local y is along tangent direction
    local_x = semicircle_radius * math.cos(angle)
    local_y = semicircle_radius * math.sin(angle)
    arc_points.append((local_x, local_y))

# Convert to 3D points in world coordinates
# At start point, inward is toward center, tangent is along helix direction
profile_3d = []
inward = normal_radial.multiply(-1)
for local_x, local_y in arc_points:
    pt = start_point.add(inward.multiply(local_x)).add(tangent.multiply(local_y))
    profile_3d.append(pt)

# Create semicircle as a wire
profile_edges = []
for i in range(len(profile_3d) - 1):
    profile_edges.append(cq.Edge.makeLine(profile_3d[i], profile_3d[i + 1]))

# Close the semicircle with a straight line
profile_edges.append(cq.Edge.makeLine(profile_3d[-1], profile_3d[0]))
profile_wire = cq.Wire.assembleEdges(profile_edges)

# Create a face from the semicircle wire for sweep
profile_face = cq.Face.makeFromWires(profile_wire)

# Perform sweep cut using the semicircle profile and helix path
result = cylinder.sweep(profile_face, helix_wire, isFrenet=True)
