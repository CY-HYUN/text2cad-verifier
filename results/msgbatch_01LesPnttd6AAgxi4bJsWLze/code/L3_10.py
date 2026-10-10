import cadquery as cq
import math

# Create the parabolic reflector concentrator
def create_parabolic_reflector():
    # Parameters
    focal_length = 20  # mm
    total_height = 80  # mm
    max_outer_diameter = 170  # mm
    max_outer_radius = max_outer_diameter / 2  # 85 mm
    wall_thickness = 5  # mm
    flange_width = 10  # mm
    flange_thickness = 5  # mm
    mounting_hole_diameter = 5  # mm
    bottom_hole_diameter = 10  # mm
    
    # Calculate parabola parameters: Z = R^2 / (4*f) where f is focal length
    # Given Z = R^2 / 80, we have 4*f = 80, so f = 20
    # At height H=80, R_max should be: 80 = R_max^2 / 80, so R_max = sqrt(6400) = 80
    # But we need max_outer_diameter = 170, so outer_radius = 85
    # We need to scale: at height 80, R = 80 for the paraboloid
    # So the outer surface extends from height 0 to 80 with radius growing as sqrt(80*Z)
    
    # Inner paraboloid surface: Z = R^2 / 80
    # For Z = 80: R = sqrt(80 * 80) = 80
    inner_max_radius = 80  # mm at Z = 80
    outer_max_radius = inner_max_radius + wall_thickness  # 85 mm
    
    # Create the inner paraboloid surface by revolving a parabola
    # Parabola equation: z = r^2 / 80
    inner_profile = cq.Workplane("XZ").moveTo(0, 0)
    
    # Create inner paraboloid profile (r, z coordinates)
    inner_points = [(0, 0)]
    for r in [i * 2 for i in range(1, int(inner_max_radius) + 1)]:
        z = (r ** 2) / 80
        if z <= total_height:
            inner_points.append((r, z))
    inner_points.append((inner_max_radius, 80))
    
    # Create outer surface profile
    outer_points = [(r + wall_thickness, z) for r, z in inner_points]
    # Add flange at top
    top_radius = outer_points[-1][0]
    flange_outer_radius = top_radius + flange_width
    outer_points.append((flange_outer_radius, total_height))
    outer_points.append((flange_outer_radius, total_height - flange_thickness))
    
    # Create solid by lofting or revolving
    # Create inner surface by revolution
    inner_wire = cq.Workplane("XZ").spline(inner_points)
    inner_face = inner_wire.revolve(360)
    
    # Create outer surface profile
    outer_wire = cq.Workplane("XZ").spline(outer_points)
    outer_solid = outer_wire.revolve(360)
    
    # Combine to create shell (outer - inner)
    shell = outer_solid.cut(inner_face)
    
    # Add flange
    flange = cq.Workplane("XY").circle(flange_outer_radius).circle(top_radius).extrude(flange_thickness)
    flange = flange.translate((0, 0, total_height - flange_thickness))
    
    # Create the complete body
    body = shell.union(flange)
    
    # Add mounting holes on the flange
    # Four holes at 90-degree intervals, one at positive Y
    hole_radius = mounting_hole_diameter / 2
    hole_distance = top_radius + flange_width / 2  # At middle of flange width
    
    mounting_hole_positions = [
        (0, hole_distance),  # Positive Y
        (hole_distance, 0),  # Positive X
        (0, -hole_distance),  # Negative Y
        (-hole_distance, 0)  # Negative X
    ]
    
    for x, y in mounting_hole_positions:
        hole = cq.Workplane("XY").circle(hole_radius).extrude(-flange_thickness * 2)
        hole = hole.translate((x, y, total_height))
        body = body.cut(hole)
    
    # Add center through-hole at bottom
    bottom_hole_radius = bottom_hole_diameter / 2
    bottom_hole = cq.Workplane("XY").circle(bottom_hole_radius).extrude(total_height + 10)
    bottom_hole = bottom_hole.translate((0, 0, -5))
    body = body.cut(bottom_hole)
    
    return body

result = create_parabolic_reflector()
