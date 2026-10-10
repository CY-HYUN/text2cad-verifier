import cadquery as cq
import math

# Create the main vertical tube
main_diameter = 20
main_radius = main_diameter / 2
main_height = 60

# Create the vertical main tube
main_tube = cq.Workplane("XY").circle(main_radius).extrude(main_height)

# Create the two branch tubes
branch_diameter = 20
branch_radius = branch_diameter / 2
branch_length = 50
branch_angle = 60  # angle between the two branches

# Convert angle to radians for calculations
angle_rad = math.radians(branch_angle / 2)

# Create first branch - angled at +30 degrees from vertical
branch1 = (cq.Workplane("XY")
           .circle(branch_radius)
           .extrude(branch_length)
           .rotate((0, 0, 0), (0, 1, 0), 30)
           .translate((branch_radius * math.sin(angle_rad), 0, main_height)))

# Create second branch - angled at -30 degrees from vertical
branch2 = (cq.Workplane("XY")
           .circle(branch_radius)
           .extrude(branch_length)
           .rotate((0, 0, 0), (0, 1, 0), -30)
           .translate((-branch_radius * math.sin(angle_rad), 0, main_height)))

# Combine all parts
result = main_tube.union(branch1).union(branch2)

# Create a smooth bifurcation transition using a sphere at the junction
transition_radius = main_radius * 1.2
transition_sphere = cq.Workplane("XY").sphere(transition_radius).translate((0, 0, main_height))

# Union the transition to smooth the junction
result = result.union(transition_sphere)

# Create the internal cavity by subtracting cylinders
# Internal cavity for main tube
main_cavity = cq.Workplane("XY").circle(main_radius * 0.95).extrude(main_height + 5)

# Internal cavity for branch 1
branch1_cavity = (cq.Workplane("XY")
                  .circle(branch_radius * 0.95)
                  .extrude(branch_length + 5)
                  .rotate((0, 0, 0), (0, 1, 0), 30)
                  .translate((branch_radius * math.sin(angle_rad), 0, main_height - 5)))

# Internal cavity for branch 2
branch2_cavity = (cq.Workplane("XY")
                  .circle(branch_radius * 0.95)
                  .extrude(branch_length + 5)
                  .rotate((0, 0, 0), (0, 1, 0), -30)
                  .translate((-branch_radius * math.sin(angle_rad), 0, main_height - 5)))

# Combine cavities
cavity = main_cavity.union(branch1_cavity).union(branch2_cavity)

# Create the final Y-shaped T-fitting by subtracting cavities from the solid
result = result.cut(cavity)
