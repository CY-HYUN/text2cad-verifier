import cadquery as cq
import math

# Create the base ring
outer_diameter = 120
inner_diameter = 80
thickness = 20

# Create the ring by making a cylinder and subtracting a smaller cylinder
ring = cq.Workplane("XY").cylinder(thickness, outer_diameter/2).faces(">Z").workplane().hole(inner_diameter/2 * 2)

# Add construction circle on top surface (for reference)
construction_circle_diameter = 100
pcd = construction_circle_diameter  # PCD is 100mm

# Define the hole parameters
countersink_diameter = 10
countersink_depth = 10
through_hole_diameter = 6
num_holes = 6

# Create a single countersunk hole at a point on the construction circle
# Position the first hole on the PCD
angle_step = 360 / num_holes

# Start with the base ring
result = ring

# Create holes using a loop for circular array
for i in range(num_holes):
    angle = i * angle_step
    # Calculate position on the PCD
    x = (pcd / 2) * math.cos(math.radians(angle))
    y = (pcd / 2) * math.sin(math.radians(angle))
    
    # Create a workplane at the top surface
    hole_plane = result.faces(">Z").workplane().moveTo(x, y)
    
    # Create countersunk hole: first the countersink, then the through hole
    # Countersink is a cone-like cut
    result = hole_plane.hole(through_hole_diameter, depth=thickness)
    
    # For the countersink, we need to use a different approach
    # Create a countersink by using a conical cut
    # We'll use cboreHole which creates a counterbore, but we need to adapt for countersink
    # Instead, manually create the countersink geometry
    
result = ring

# Apply circular array of holes more explicitly
for i in range(num_holes):
    angle = i * angle_step
    x = (pcd / 2) * math.cos(math.radians(angle))
    y = (pcd / 2) * math.sin(math.radians(angle))
    
    # Create countersink hole using cboreHole
    # cboreHole(diameter, depth, cboreDiameter, cboreDepth)
    result = result.faces(">Z").workplane().moveTo(x, y).cboreHole(
        through_hole_diameter, 
        depth=thickness,
        cboreDiameter=countersink_diameter,
        cboreDepth=countersink_depth
    )

result = result
