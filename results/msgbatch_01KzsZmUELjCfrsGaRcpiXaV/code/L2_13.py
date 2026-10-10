import cadquery as cq
import math

# Create a regular dodecahedron with circumscribed sphere radius of 30mm
R = 30  # circumscribed radius
phi = (1 + math.sqrt(5)) / 2  # golden ratio

# Golden ratio based coordinates for dodecahedron vertices
# Standard dodecahedron vertex set
scale = R / math.sqrt(3 * (phi + 2))

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

# Calculate face centers and normals
face_centers = []
for face in faces:
    cx = sum(vertices[i][0] for i in face) / 5
    cy = sum(vertices[i][1] for i in face) / 5
    cz = sum(vertices[i][2] for i in face) / 5
    face_centers.append((cx, cy, cz))

# Define edges of dodecahedron
edges = [
    (0, 12), (0, 10), (0, 14), (1, 5), (1, 12), (1, 3), (1, 9),
    (2, 16), (2, 10), (2, 15), (3, 13), (3, 11), (4, 6), (4, 14),
    (4, 19), (5, 9), (5, 14), (6, 7), (6, 10), (7, 11), (7, 15),
    (8, 10), (8, 18), (8, 9), (9, 11), (9, 19), (11, 19), (11, 7),
    (12, 16), (12, 17), (13, 15), (13, 17), (15, 7), (16, 17), (16, 18),
    (18, 19),
]

# Create edge cylinders with proper geometry
edge_radius = 1.2
edge_parts = []

for edge in edges:
    v1 = vertices[edge[0]]
    v2 = vertices[edge[1]]
    
    midpoint = ((v1[0] + v2[0])/2, (v1[1] + v2[1])/2, (v1[2] + v2[2])/2)
    direction = (v2[0] - v1[0], v2[1] - v1[1], v2[2] - v1[2])
    length = math.sqrt(direction[0]**2 + direction[1]**2 + direction[2]**2)
    
    # Create a small cylinder for the edge
    edge_cyl = cq.Workplane().moveTo(0, 0).circle(edge_radius).extrude(length)
    
    # Normalize direction and rotate to align with edge
    dir_norm = (direction[0]/length, direction[1]/length, direction[2]/length)
    
    # Translate to midpoint
    edge_cyl = edge_cyl.translate((midpoint[0], midpoint[1], midpoint[2]))
    edge_parts.append(edge_cyl)

# Start with union of all edges
if edge_parts:
    result = edge_parts[0]
    for part in edge_parts[1:]:
        result = result.union(part)
else:
    result = cq.Workplane().box(0.1, 0.1, 0.1)

# Create holes at face centers
hole_radius = 3.8
for center in face_centers:
    # Create through-hole cylinder
    hole_length = R * 2.8
    hole = cq.Workplane().moveTo(0, 0).circle(hole_radius).extrude(hole_length)
    
    # Position hole through face center
    dist = math.sqrt(center[0]**2 + center[1]**2 + center[2]**2)
    if dist > 0:
        direction = (center[0]/dist, center[1]/dist, center[2]/dist)
        offset = (direction[0] * hole_length / 2, direction[1] * hole_length / 2, direction[2] * hole_length / 2)
        hole = hole.translate((center[0] - offset[0], center[1] - offset[1], center[2] - offset[2]))
    
    result = result.cut(hole)

