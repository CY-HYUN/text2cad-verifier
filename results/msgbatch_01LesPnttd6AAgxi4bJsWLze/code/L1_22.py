import cadquery as cq
import math

# Create the base frustum (truncated square pyramid)
# Base: 60x60 mm square at z=0
# Top: 40x40 mm square at z=30 mm
# Height: 30 mm

# Create the outer frustum shape
result = cq.Workplane("XY").box(60, 60, 30)

# Create a frustum by cutting away the corners
# We'll use a more precise approach: create the bottom square, then the top square,
# and loft between them

# Start with bottom face (60x60)
bottom = cq.Workplane("XY").moveTo(0, 0).rect(60, 60)

# Create top face (40x40) at height 30
top = cq.Workplane("XY").moveTo(0, 0).rect(40, 40).moveTo(0, 0, 30)

# Create a frustum by creating a box and cutting it to shape
# Actually, let's build this properly using vertices and lofting

# Define vertices for the frustum
# Bottom square: 60x60 centered at origin, z=0
bottom_verts = [
    (-30, -30, 0),
    (30, -30, 0),
    (30, 30, 0),
    (-30, 30, 0)
]

# Top square: 40x40 centered at origin, z=30
top_verts = [
    (-20, -20, 30),
    (20, -20, 30),
    (20, 20, 30),
    (-20, 20, 30)
]

# Create the frustum by lofting between bottom and top
result = (
    cq.Workplane("XY")
    .polyline(bottom_verts)
    .close()
    .workplane(offset=30)
    .polyline(top_verts)
    .close()
    .loft(ruled=True)
)

# Create a cylindrical hole through the center
hole = cq.Workplane("XY").circle(10).extrude(30, both=True)

# Cut the hole from the frustum
result = result.cut(hole)
