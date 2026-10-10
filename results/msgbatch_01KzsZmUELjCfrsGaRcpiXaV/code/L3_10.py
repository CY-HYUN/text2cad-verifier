import cadquery as cq
import math

# Create the parabolic reflector concentrator
def create_parabolic_reflector():
    # Parameters
    total_height = 80  # mm
    max_outer_diameter = 170  # mm
    max_outer_radius = max_outer_diameter / 2  # 85 mm
    wall_thickness = 5  # mm
    flange_width = 10  # mm
    flange_thickness = 5  # mm
    mounting_hole_diameter = 5  # mm
    bottom_hole_diameter = 10  # mm
    
    # Inner paraboloid: Z = R^2 / 80
    # At Z = 80: R = 80
    inner_max_radius = 80  # mm at Z = 80
    outer_max_radius = inner_max_radius + wall_thickness  # 85 mm
    
    # Create inner paraboloid profile (r, z coordinates)
    inner_points = [(0, 0)]
    for i in range(1, int(inner_max_radius) + 1):
        r = float(i)
        z = (r ** 2) / 80.0
        if z <= total_height:
            inner_points.append((r, z))
    
    # Ensure we reach the top
    if inner_points[-1][1] < total_height:
        inner_points.append((inner_max_radius, total_height))
    
    # Create outer surface profile (inner + wall thickness)
    outer_points = [(r + wall_thickness, z) for r, z in inner_points]
    
    # Add flange at top
    flange_outer_radius = outer_points[-1][0] + flange_width
    outer_points.append((flange_outer_radius, total_height))
    outer_points.append((flange_outer_radius, total_height - flange_thickness))
    
    # Close the profile by going back to bottom on outer wall
    outer_points.append((outer_max_radius + wall_thickness, 0))
    
    # Create the outer solid by revolving the profile
    outer_profile = cq.Workplane("XZ").polyline(outer_points)
    outer_solid = outer_profile.revolve(360, (0, 0, 0), (0, 0, 1))
    
    # Create the inner cavity profile
    inner_cavity_points = [(0, -1)] + inner_points + [(0, total_height + 1)]
    inner_cavity = cq.Workplane("XZ").polyline(inner_cavity_points)
    inner_cavity_solid = inner_cavity.revolve(360, (0, 0, 0), (0, 0, 1))
    
    # Create body by cutting inner cavity from outer solid
    body = outer_solid.cut(inner_cavity_solid)
    
    # Add mounting holes on the flange (4 holes)
    hole_radius = mounting_hole_diameter / 2
    hole_distance = outer_max_radius + flange_width / 2
    
    mounting_hole_positions = [
        (0, hole_distance),  # Positive Y
        (hole_distance, 0),  # Positive X
        (0, -hole_distance),  # Negative Y
        (-hole_distance, 0)  # Negative X
    ]
    
    for x, y in mounting_hole_positions:
        hole = cq.Workplane("XY").circle(hole_radius).extrude(-(flange_thickness + 2))
        hole = hole.translate((x, y, total_height))
        body = body.cut(hole)
    
    # Add center through-hole at bottom
    bottom_hole_radius = bottom_hole_diameter / 2
    bottom_hole = cq.Workplane("XY").circle(bottom_hole_radius).extrude(total_height + 10)
    bottom_hole = bottom_hole.translate((0, 0, -5))
    body = body.cut(bottom_hole)
    
    return body

result = create_parabolic_reflector()
