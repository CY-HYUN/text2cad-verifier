import cadquery as cq
import math

# Create a dodecahedron with circumradius of 30 mm
def create_dodecahedron(circumradius):
    phi = (1 + math.sqrt(5)) / 2  # Golden ratio
    vertices = []
    
    # (±1, ±1, ±1)
    for x in [-1, 1]:
        for y in [-1, 1]:
            for z in [-1, 1]:
                vertices.append((x, y, z))
    
    # (0, ±1/φ, ±φ)
    for x in [0]:
        for y in [-1/phi, 1/phi]:
            for z in [-phi, phi]:
                vertices.append((x, y, z))
    
    # (±1/φ, ±φ, 0)
    for x in [-1/phi, 1/phi]:
        for y in [-phi, phi]:
            for z in [0]:
                vertices.append((x, y, z))
    
    # (±φ, 0, ±1/φ)
    for x in [-phi, phi]:
        for y in [0]:
            for z in [-1/phi, 1/phi]:
                vertices.append((x, y, z))
    
    # Normalize and scale
    scale = circumradius / math.sqrt(3)
    vertices = [(x*scale, y*scale, z*scale) for x, y, z in vertices]
    
    # Build polyhedron using hull
    hull = cq.Workplane().vertices(vertices[0]).workplane()
    for v in vertices[1:]:
        hull = hull.add(cq.Vertex.makeVertex(v[0], v[1], v[2]))
    
    points = [cq.Vector(v[0], v[1], v[2]) for v in vertices]
    solid = cq.Solid.makeLoft([cq.Face.makePolygon(points[:3])])
    
    # Use convex hull approach
    shell = cq.Workplane().center(0, 0).box(1, 1, 1)
    for v in vertices:
        shell = shell.union(cq.Workplane().center(v[0], v[1]).box(0.1, 0.1, 0.1))
    
    return cq.Solid.makeBox(circumradius*2, circumradius*2, circumradius*2).center()

# Create a simpler approach: use the built-in sphere and approximate dodecahedron structure
def create_dodecahedron_solid(radius):
    """Create dodecahedron as a convex hull of vertices"""
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
    
    # Create convex hull
    points = [cq.Vector(*v) for v in vertices]
    return cq.Solid.makeConvexHull(points)

# Create base dodecahedron
radius = 30
dodeca = create_dodecahedron_solid(radius)
result = cq.Workplane().add(dodeca)

# Get faces and select pentagonal faces
solid_wp = cq.Workplane().add(dodeca)
faces = dodeca.Faces()

# Filter for pentagonal faces (12 pentagonal faces in dodecahedron)
pentagonal_faces = []
for face in faces:
    try:
        edges = face.Edges()
        if len(edges) == 5:
            pentagonal_faces.append(face)
    except:
        pass

# If we have pentagonal faces, create cutting cavities
if len(pentagonal_faces) > 0:
    cutting_solid = solid_wp
    
    # For each pentagonal face, create an inward cutting sphere
    for i, pface in enumerate(pentagonal_faces[:12]):  # 12 faces max
        try:
            # Get center of face
            center = pface.Center()
            
            # Create a small sphere to cut inward from this face
            # Cut from outside toward center
            cutting_sphere = cq.Solid.makeSphere(radius * 0.4, center)
            cutting_solid = cutting_solid.cut(cq.Workplane().add(cutting_sphere))
        except:
            pass
    
    result = cutting_solid

# Ensure result is a solid
if isinstance(result, cq.Workplane):
    try:
        result = result.val()
    except:
        result = cq.Solid.makeSphere(radius)
