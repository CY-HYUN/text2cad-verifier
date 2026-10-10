import cadquery as cq
import math

# Create a regular dodecahedron with circumscribed sphere radius of 30mm
# For a regular dodecahedron, the relationship between circumscribed radius R and edge length a is:
# R = a * sqrt(3) * (1 + sqrt(5)) / 4
# So: a = 4 * R / (sqrt(3) * (1 + sqrt(5)))

R = 30  # circumscribed radius
phi = (1 + math.sqrt(5)) / 2  # golden ratio
a = 4 * R / (math.sqrt(3) * (1 + math.sqrt(5)))

# Golden ratio based coordinates for dodecahedron vertices
# Scaled to have circumscribed radius of 30mm
scale = R / math.sqrt(3 * (phi + 2))

# Generate the 20 vertices of a regular dodecahedron
vertices = [
    (-1, -1, -1),
    (-1, -1, 1),
    (-1, 1, -1),
    (-1, 1, 1),
    (1, -1, -1),
    (1, -1, 1),
    (1, 1, -1),
    (1, 1, 1),
    (0, -1/phi, -phi),
    (0, -1/phi, phi),
    (0, 1/phi, -phi),
    (0, 1/phi, phi),
    (-1/phi, -phi, 0),
    (-1/phi, phi, 0),
    (1/phi, -phi, 0),
    (1/phi, phi, 0),
    (-phi, 0, -1/phi),
    (-phi, 0, 1/phi),
    (phi, 0, -1/phi),
    (phi, 0, 1/phi),
]

# Scale vertices
vertices = [(v[0] * scale, v[1] * scale, v[2] * scale) for v in vertices]

# Define the 12 pentagonal faces of the dodecahedron
faces = [
    [0, 12, 16, 2, 10],
    [0, 10, 6, 4, 14],
    [0, 14, 5, 1, 12],
    [1, 5, 9, 11, 3],
    [1, 3, 13, 17, 12],
    [2, 16, 17, 13, 15],
    [2, 15, 7, 6, 10],
    [3, 11, 7, 15, 13],
    [4, 6, 7, 11, 19],
    [4, 19, 9, 5, 14],
    [8, 10, 2, 16, 18],
    [8, 18, 19, 11, 9],
]

# Calculate face centers (for drilling holes)
face_centers = []
for face in faces:
    cx = sum(vertices[i][0] for i in face) / 5
    cy = sum(vertices[i][1] for i in face) / 5
    cz = sum(vertices[i][2] for i in face) / 5
    face_centers.append((cx, cy, cz))

# Start with a sphere as the base solid
result = cq.Workplane().sphere(R)

# Create edges by building the dodecahedron frame
# Build all edges as cylinders
edges = [
    (0, 12), (0, 10), (0, 14), (1, 5), (1, 12), (1, 3), (1, 9),
    (2, 16), (2, 10), (2, 15), (3, 13), (3, 11), (4, 6), (4, 14),
    (4, 19), (5, 9), (5, 14), (6, 7), (6, 10), (7, 11), (7, 15),
    (8, 10), (8, 18), (8, 9), (9, 11), (9, 19), (11, 19), (11, 7),
    (12, 16), (12, 17), (13, 15), (13, 17), (15, 7), (16, 17), (16, 18),
    (18, 19),
]

# Remove duplicates and create edge cylinders
edge_radius = a * 0.12  # Make edges thinner relative to edge length
edge_union = None

for edge in edges:
    v1 = vertices[edge[0]]
    v2 = vertices[edge[1]]
    
    # Create cylinder between vertices
    midpoint = ((v1[0] + v2[0])/2, (v1[1] + v2[1])/2, (v1[2] + v2[2])/2)
    direction = (v2[0] - v1[0], v2[1] - v1[1], v2[2] - v1[2])
    length = math.sqrt(direction[0]**2 + direction[1]**2 + direction[2]**2)
    
    edge_cyl = cq.Workplane().moveTo(0, 0).circle(edge_radius).extrude(length)
    edge_cyl = edge_cyl.translate(midpoint)
    
    if edge_union is None:
        edge_union = edge_cyl
    else:
        edge_union = edge_union.union(edge_union.union(edge_cyl))

# Create the skeletal structure by drilling holes at face centers
hole_radius = a * 0.35  # Radius for connecting holes

for center in face_centers:
    # Calculate hole direction (radial from origin)
    dist = math.sqrt(center[0]**2 + center[1]**2 + center[2]**2)
    direction = (center[0]/dist, center[1]/dist, center[2]/dist)
    
    # Create through-hole cylinder
    hole = cq.Workplane().moveTo(0, 0).circle(hole_radius).extrude(R * 2.5)
    hole = hole.translate((center[0] - direction[0]*R*1.25, 
                           center[1] - direction[1]*R*1.25, 
                           center[2] - direction[2]*R*1.25))
    result = result.cut(hole)

# Combine with edges to create skeletal frame
if edge_union is not None:
    result = edge_union.union(result)
