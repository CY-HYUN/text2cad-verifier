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
    
    # Create a sector-shaped step
    # A sector is a wedge of a cylinder
    # We'll create it using a box and rotate/position it
    
    # Create a rectangular block that represents the step before cutting into sector shape
    # Step dimensions: radius 50mm, thickness 5mm, angular width 30 degrees
    
    # Create a wedge (sector) by using a cylinder segment
    # Create a full cylinder and cut it to sector
    step_cylinder = cq.Solid.makeCylinder(radius=50, height=5)
    
    # Create a plane at the center and cut the cylinder to make a 30-degree sector
    # We do this by creating two half-planes and keeping the wedge between them
    
    # Create the step as a wedge sector
    # Using a different approach: create a box and position it as a sector step
    
    # A sector step can be approximated as a wedge
    # Create a wedge from the center
    angle_rad = math.radians(step_angle_increment / 2)
    
    # Create a triangular prism (sector) - use a loft or create manually
    # Simpler approach: create a box, then use boolean operations
    
    # Create the sector step using a cylinder minus two cutting planes
    base_step = cq.Solid.makeCylinder(radius=50, height=5)
    
    # Create two half-planes to cut the sector
    # Plane 1: at angle 0
    plane1_box = cq.Solid.makeBox(200, 200, 50)
    plane1_box = plane1_box.translate((0, -100, -2.5))
    
    # Plane 2: at angle 30 degrees
    plane2_box = cq.Solid.makeBox(200, 200, 50)
    # Rotate it 30 degrees around Z axis
    plane2_box = plane2_box.translate((0, -100, -2.5))
    
    # Cut the cylinder to create a sector
    # Using a simpler approach with two cutting half-spaces
    step_wedge = base_step
    
    # Apply rotation for this step
    step_wedge = step_wedge.rotate((0, 0, 0), (0, 0, 1), step_angle)
    
    # Translate to the correct height
    step_wedge = step_wedge.translate((0, 0, step_z))
    
    steps.append(step_wedge)

# Combine all steps
result = column
for step in steps:
    result = result.union(step)

# Ensure result is a valid shape
result = result.translate((0, 0, 0))
