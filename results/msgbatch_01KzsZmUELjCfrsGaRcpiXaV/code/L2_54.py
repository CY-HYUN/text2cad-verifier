import cadquery as cq
import math

# Create a frame-like pyramid with triangular openings
base_size = 40
height = 40
thickness = 2

# Create base frame
result = cq.Workplane("XY").box(base_size, base_size, thickness)

# Define the four corners of the base
half = base_size / 2
base_corners = [(-half, -half), (half, -half), (half, half), (-half, half)]

# Create four vertical edge ribs
for i in range(4):
    x, y = base_corners[i]
    rib = cq.Workplane("XY").moveTo(x, y).box(thickness, thickness, height)
    result = result.union(rib)

# Create four slanted ribs from base corners to apex
apex = (0, 0, height)
for i in range(4):
    x1, y1 = base_corners[i]
    x2, y2 = base_corners[(i + 1) % 4]
    
    # Create slanted edge from corner to apex using a thin extrusion
    edge_profile = cq.Workplane("XY").polyline([(x1, y1, 0), (apex[0], apex[1], apex[2])]).extrude(thickness)
    result = result.union(edge_profile)

# Create triangular through-holes on each of the four sides
# These holes connect outer surface to inner cavity
tri_width = base_size * 0.2
tri_height = height * 0.3

# Front face (y = -half)
tri_verts_front = [
    (-tri_width/2, -half, height/2),
    (tri_width/2, -half, height/2),
    (0, -half, height/2 + tri_height)
]

# Create cutting planes for triangular holes
for face_idx in range(4):
    if face_idx == 0:  # Front
        hole = cq.Workplane("XY").moveTo(0, -half).box(tri_width, thickness*2, tri_height, centered=True)
    elif face_idx == 1:  # Right
        hole = cq.Workplane("XY").moveTo(half, 0).box(thickness*2, tri_width, tri_height, centered=True)
    elif face_idx == 2:  # Back
        hole = cq.Workplane("XY").moveTo(0, half).box(tri_width, thickness*2, tri_height, centered=True)
    else:  # Left
        hole = cq.Workplane("XY").moveTo(-half, 0).box(thickness*2, tri_width, tri_height, centered=True)
    
    # Shift hole to middle of height
    hole = hole.translate((0, 0, height/3))
    result = result.cut(hole)

# Create internal cavity - smaller pyramid shape to add skeletal appearance
inner_size = base_size * 0.5
inner_cavity = cq.Workplane("XY").box(inner_size, inner_size, height * 0.6)
inner_cavity = inner_cavity.translate((0, 0, thickness))
result = result.cut(inner_cavity)

