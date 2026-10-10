import cadquery as cq
import math

# Create the central column
column = cq.Solid.makeCylinder(radius=10, height=100)

# Create the steps
steps = []
num_steps = 10
step_height_increment = 100 / num_steps  # 10mm between steps
step_angle_increment = 30  # degrees

for i in range(num_steps):
    # Calculate height and rotation for this step
    step_z = i * step_height_increment
    step_angle = i * step_angle_increment
    
    # Create a sector-shaped step using a wedge
    # Create a cylindrical step
    step_radius = 50
    step_thickness = 5
    
    # Create a box to represent the step sector
    # Width is based on sector angle (30 degrees)
    sector_width = step_radius * math.sin(math.radians(step_angle_increment / 2)) * 2
    
    # Create wedge using three points at base and three at top
    pts_base = [
        (0, 0, 0),
        (step_radius * math.cos(math.radians(-step_angle_increment / 2)), 
         step_radius * math.sin(math.radians(-step_angle_increment / 2)), 0),
        (step_radius * math.cos(math.radians(step_angle_increment / 2)), 
         step_radius * math.sin(math.radians(step_angle_increment / 2)), 0),
    ]
    
    pts_top = [
        (0, 0, step_thickness),
        (step_radius * math.cos(math.radians(-step_angle_increment / 2)), 
         step_radius * math.sin(math.radians(-step_angle_increment / 2)), step_thickness),
        (step_radius * math.cos(math.radians(step_angle_increment / 2)), 
         step_radius * math.sin(math.radians(step_angle_increment / 2)), step_thickness),
    ]
    
    # Create a wedge solid
    step_wedge = cq.Solid.makeLoft([
        cq.Face.makeFromWires(cq.Wire.makePolygon(pts_base)),
        cq.Face.makeFromWires(cq.Wire.makePolygon(pts_top))
    ])
    
    # Apply rotation for this step
    step_wedge = step_wedge.rotate((0, 0, 0), (0, 0, 1), step_angle)
    
    # Translate to the correct height
    step_wedge = step_wedge.translate((0, 0, step_z))
    
    steps.append(step_wedge)

# Combine all steps with column using CadQuery Workplane
result = cq.Workplane("XY").add(column)
for step in steps:
    result = result.add(step)

# Convert to solid
result = result.val()
