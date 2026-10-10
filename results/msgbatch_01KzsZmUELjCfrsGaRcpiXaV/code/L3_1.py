import cadquery as cq
import math

# Create a paraboloid of revolution for a car headlight reflector
# Vertex at (100, 75, 0), focus at (150, 75, 0), focal length = 50mm
# Paraboloid equation: Y^2 + Z^2 = 200(X - 100)
# Extends from X=100 to X=200

def create_paraboloid_surface():
    # Parameters
    vertex_x = 100
    vertex_y = 75
    vertex_z = 0
    focal_length = 50
    p = 100  # 2 * focal_length
    depth = 100
    
    num_sections = 40
    
    # Create profile curve (parabola in XY plane at Z=0)
    profile_points = []
    
    for i in range(num_sections + 1):
        x_local = (i / num_sections) * depth
        y_offset = math.sqrt(p * x_local)
        profile_points.append((x_local, y_offset))
    
    # Create the 2D profile as a polyline
    # Start from vertex, go along parabola, then close back
    profile_2d = profile_points.copy()
    profile_2d.append((depth, 0))
    profile_2d.append((0, 0))
    
    # Create workplane in YZ plane (looking along X-axis)
    # Build profile in XY coordinates which become YZ in the workplane
    wp = cq.Workplane("XY")
    
    # Build the profile starting from origin
    wp = wp.moveTo(profile_2d[0][0], profile_2d[0][1])
    for point in profile_2d[1:]:
        wp = wp.lineTo(point[0], point[1])
    wp = wp.close()
    
    # Revolve around X-axis (the first axis, which is X in the local XY plane)
    # We need to revolve around the X-axis through the origin
    face = wp.faces().val()
    solid = cq.Workplane("XY").revolve(360, axis=(1, 0, 0), origin=(0, 0, 0))
    
    # Alternative approach: use the wire and revolve
    wp_profile = cq.Workplane("XY")
    wp_profile = wp_profile.moveTo(profile_2d[0][0], profile_2d[0][1])
    for point in profile_2d[1:]:
        wp_profile = wp_profile.lineTo(point[0], point[1])
    wp_profile = wp_profile.close()
    
    solid = wp_profile.revolve(360, axis=(1, 0, 0))
    
    # Translate to correct position
    solid = solid.translate((vertex_x, vertex_y, vertex_z))
    
    return solid

result = create_paraboloid_surface()
