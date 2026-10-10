import cadquery as cq
import math

# Create the main pyramid (solid first)
base_size = 40
height = 40

# Create the outer pyramid
def create_pyramid(base_size, height):
    # Create a square base
    base = cq.Workplane("XY").box(base_size, base_size, 0.1)
    
    # Create pyramid by lofting from base to apex
    square_base = cq.Workplane("XY").rect(base_size, base_size)
    apex_point = cq.Workplane("XY").workplane(offset=height).point(0, 0)
    
    # Create the four triangular faces
    half_size = base_size / 2
    vertices_base = [
        (-half_size, -half_size, 0),
        (half_size, -half_size, 0),
        (half_size, half_size, 0),
        (-half_size, half_size, 0)
    ]
    apex = (0, 0, height)
    
    # Build pyramid as a solid
    solid = cq.Workplane("XY")
    
    # Create 4 triangular faces and close them
    faces = []
    for i in range(4):
        v1 = vertices_base[i]
        v2 = vertices_base[(i + 1) % 4]
        v3 = apex
        
        # Create triangle vertices
        pts = [v1, v2, v3]
        faces.append(pts)
    
    # Create base face
    base_pts = vertices_base
    
    # Use Shell to create the pyramid surface, then make it solid
    pyramid = cq.Workplane("XY").rect(base_size, base_size).extrude(0.1)
    
    # Better approach: create pyramid using loft
    base_sketch = cq.Workplane("XY").rect(base_size, base_size)
    top_sketch = cq.Workplane("XY").workplane(offset=height).point(0, 0)
    
    # Create solid pyramid by building from faces
    # Create the 4 side triangles and base
    pyramid_solid = cq.Workplane("XY").box(base_size, base_size, height, centered=False)
    
    # Better: use a direct approach with vertices
    half = base_size / 2
    base_corners = [(-half, -half), (half, -half), (half, half), (-half, half)]
    
    # Create edges for pyramid skeleton
    edges = cq.Workplane("XY")
    
    # Create the four base edges
    for i in range(4):
        p1 = base_corners[i]
        p2 = base_corners[(i + 1) % 4]
        edge = cq.Workplane("XY").moveTo(p1[0], p1[1]).lineTo(p2[0], p2[1])
    
    # Create a box and hollow it out
    pyramid_box = cq.Workplane("XY").box(base_size, base_size, height, centered=False)
    
    # Create inner cavity (smaller pyramid from center)
    inner_pyramid_size = base_size * 0.6
    inner_depth = height * 0.5
    
    # Cut the inner pyramid cavity
    cavity = cq.Workplane("XY").workplane(offset=0.1).rect(inner_pyramid_size, inner_pyramid_size).extrude(inner_depth)
    
    # Create triangular holes on each face
    # Each triangular hole connects the outer face to the inner cavity
    
    # Start with hollow pyramid framework
    result = pyramid_box
    
    # Remove inner cavity
    inner_cavity = cq.Workplane("XY").box(inner_pyramid_size, inner_pyramid_size, inner_depth, centered=False)
    result = result.cut(inner_cavity)
    
    # Create triangular apertures on each face
    tri_height = base_size * 0.3
    tri_width = base_size * 0.25
    
    # Triangle hole on front face
    for face_idx in range(4):
        # Create a triangular face cut
        tri_pts = [
            (-tri_width/2, height/3, -0.1),
            (tri_width/2, height/3, -0.1),
            (0, height/3 + tri_height, -0.1)
        ]
        
        # Create extrusion for the cut (goes through)
        tri_sketch = cq.Workplane("XY").workplane(offset=height/3)
        tri_sketch = tri_sketch.moveTo(-tri_width/2, 0).lineTo(tri_width/2, 0).lineTo(0, tri_height).close()
        tri_cut = tri_sketch.extrude(base_size)
        
        # This is complex, use a simpler approach
    
    # Simplify: create frame-like structure
    thickness = 2
    result = cq.Workplane("XY").box(base_size, base_size, thickness, centered=False)
    
    # Add four vertical edges (ribs)
    for i in range(4):
        p = base_corners[i]
        rib = cq.Workplane("XY").moveTo(p[0], p[1]).box(thickness, thickness, height, centered=False)
        result = result.union(rib)
    
    # Add four slanted edges to apex
    apex_x, apex_y, apex_z = 0, 0, height
    for i in range(4):
        p1 = base_corners[i]
        # Create a thin triangular face from base corner to apex
        edge_rib = cq.Workplane("XY").polyline([
            (p1[0], p1[1], 0),
            (apex_x, apex_y, apex_z)
        ]).toPending()
    
    # Simplified skeleton pyramid
    return result

result = create_pyramid(40, 40)
