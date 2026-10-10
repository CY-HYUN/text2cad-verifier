import cadquery as cq
import math

# Create a paraboloid of revolution for a car headlight reflector
# Vertex at (100, 75, 0), focus at (150, 75, 0), focal length = 50mm
# Paraboloid equation: Y^2 + Z^2 = 200(X - 100)
# Extends from X=100 to X=200

# Create the paraboloid surface using a parametric approach
# We'll generate points on the surface and create a 3D shape

def create_paraboloid_surface():
    # Parameters
    vertex_x = 100
    vertex_y = 75
    vertex_z = 0
    focal_length = 50
    p = 100  # 2 * focal_length
    depth = 100
    
    # Create a series of circular cross-sections along the X-axis
    # and loft them to form the paraboloid surface
    
    sketches = []
    num_sections = 50
    
    for i in range(num_sections + 1):
        x_local = (i / num_sections) * depth
        x_global = vertex_x + x_local
        
        # For paraboloid: Y^2 + Z^2 = 200(X - 100)
        # At position x_global: radius^2 = 200 * (x_global - vertex_x)
        radius_sq = p * x_local
        
        if radius_sq < 0:
            continue
            
        radius = math.sqrt(radius_sq)
        
        # Create a circle at this X position
        # Circle centered at (vertex_y, vertex_z) with given radius
        circle = (
            cq.Workplane("XY")
            .center(vertex_y, vertex_z)
            .circle(radius)
            .workplane(offset=x_global - vertex_x)
        )
        sketches.append((x_global, radius))
    
    # Build the paraboloid by creating circular cross-sections and lofting
    # We'll use a different approach: create a solid of revolution
    
    # Create a 2D profile (parabola in XY plane, then rotate around X-axis)
    # Profile: in the X-Y plane where Z=0
    # Y = sqrt(200 * (X - 100)) for the positive side
    
    points_profile = []
    
    # Start from vertex
    points_profile.append((vertex_x, vertex_y))
    
    # Generate points along the parabola
    for i in range(1, num_sections + 1):
        x_local = (i / num_sections) * depth
        x = vertex_x + x_local
        y_offset = math.sqrt(p * x_local)
        y = vertex_y + y_offset
        points_profile.append((x, y))
    
    # Create the profile curve
    profile_points = [(p[0], 0, p[1]) for p in points_profile]
    
    # Create initial workplane and build the paraboloid
    wp = cq.Workplane("XZ")
    
    # Create a 2D sketch of the parabola profile in XY plane
    sketch_points = []
    for i in range(num_sections + 1):
        x_local = (i / num_sections) * depth
        x = x_local
        y_offset = math.sqrt(p * x_local)
        sketch_points.append((x, y_offset))
    
    # Add the return path to close the profile (vertical lines at ends)
    sketch_points.append((depth, 0))
    sketch_points.append((0, 0))
    
    # Create workplane and sketch the profile
    wp = cq.Workplane("XY").center(vertex_y, vertex_z)
    
    # Create by revolving the parabola around the X-axis
    # Build the profile as a wire
    profile_wire_points = []
    for i in range(num_sections + 1):
        x_local = (i / num_sections) * depth
        y_offset = math.sqrt(p * x_local)
        profile_wire_points.append((x_local, y_offset, 0))
    
    # Add closing points
    profile_wire_points.append((depth, 0, 0))
    profile_wire_points.append((0, 0, 0))
    
    # Create a face by revolving around X-axis
    # Use a 2D profile and revolve
    profile_2d = [(p[0], p[1]) for p in profile_wire_points]
    
    wp = cq.Workplane("YZ").polyline(profile_2d).close()
    solid = wp.revolve(360, (1, 0, 0))
    
    # Translate to correct position
    solid = solid.translate((vertex_x, vertex_y, vertex_z))
    
    return solid

result = create_paraboloid_surface()
