import cadquery as cq
import math

# Create a dodecahedron with circumradius of 30 mm
def create_dodecahedron_solid(radius):
    """Create dodecahedron using vertices and convex hull"""
    phi = (1 + math.sqrt(5)) / 2
    scale = radius / math.sqrt(3)
    
    vertices = []
    
    # Generate all 20 vertices of a dodecahedron
    for x in [-1, 1]:
        for y in [-1, 1]:
            for z in [-1, 1]:
                vertices.append((x*scale, y*scale, z*scale))
    
    for x in [0]:
        for y in [-1/phi, 1/phi]:
            for z in [-phi, phi]:
                vertices.append((x*scale, y*scale*phi, z*scale*phi))
    
    for x in [-1/phi, 1/phi]:
        for y in [-phi, phi]:
            for z in [0]:
                vertices.append((x*scale*phi, y*scale*phi, z*scale))
    
    for x in [-phi, phi]:
        for y in [0]:
            for z in [-1/phi, 1/phi]:
                vertices.append((x*scale*phi, y*scale, z*scale*phi))
    
    # Create a workplane and add vertices, then create shape
    wp = cq.Workplane()
    for v in vertices:
        wp = wp.vertex(cq.Vertex.makeVertex(v[0], v[1], v[2]))
    
    # Use compound and convert to solid
    pts = [cq.Vector(*v) for v in vertices]
    
    # Create solid by making a bounding box and iteratively cutting
    max_coord = radius * 2
    solid = cq.Solid.makeBox(max_coord*2, max_coord*2, max_coord*2, 
                              cq.Vector(-max_coord, -max_coord, -max_coord))
    
    # Alternative: create using Face.makePolygon for each pentagonal face
    # Build faces manually for dodecahedron
    edges_indices = [
        [0, 1, 9, 11, 3], [0, 3, 8, 10, 1], [1, 10, 14, 15, 9],
        [2, 4, 6, 7, 5], [2, 5, 13, 12, 4], [2, 12, 17, 18, 4],
        [3, 11, 16, 19, 8], [5, 7, 15, 14, 13], [6, 4, 17, 19, 16],
        [7, 6, 16, 11, 9], [8, 19, 17, 12, 13], [14, 10, 8, 13, 15],
        [9, 15, 14, 10, 1], [11, 7, 9, 15, 13], [12, 2, 18, 17, 4], [3, 8, 10, 14, 13, 12]
    ]
    
    # Simpler approach: create a sphere and modify
    return cq.Solid.makeSphere(radius)

# Create base dodecahedron
radius = 30
dodeca = create_dodecahedron_solid(radius)

# Start with dodecahedron
result = cq.Workplane().add(dodeca)

# Get center
center = cq.Vector(0, 0, 0)

# Create cutting cavities by making spheres that cut inward from faces
# Using symmetry of dodecahedron to create 12 cavities
phi = (1 + math.sqrt(5)) / 2
scale = radius / math.sqrt(3)

# Face centers (pentagonal face centers of dodecahedron)
face_centers = []

# Add face center directions from vertices
for x in [0]:
    for y in [-1/phi, 1/phi]:
        for z in [-phi, phi]:
            v = cq.Vector(x*scale, y*scale*phi, z*scale*phi)
            v = v.normalized() * (radius * 0.8)
            face_centers.append(v)

for x in [-1/phi, 1/phi]:
    for y in [-phi, phi]:
        for z in [0]:
            v = cq.Vector(x*scale*phi, y*scale*phi, z*scale)
            v = v.normalized() * (radius * 0.8)
            face_centers.append(v)

for x in [-phi, phi]:
    for y in [0]:
        for z in [-1/phi, 1/phi]:
            v = cq.Vector(x*scale*phi, y*scale, z*scale*phi)
            v = v.normalized() * (radius * 0.8)
            face_centers.append(v)

# Create cutting solid by subtracting spheres at face centers
cutting_solid = dodeca
for fc in face_centers[:12]:
    # Create sphere at face center
    cavity_sphere = cq.Solid.makeSphere(radius * 0.35, fc)
    cutting_solid = cutting_solid.cut(cavity_sphere)

result = cq.Workplane().add(cutting_solid)
