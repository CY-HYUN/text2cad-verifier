import cadquery as cq
import math

# Parameters
square_side = 50
square_height = 20
transition_height = 20
cylinder_diameter = 30
cylinder_height = 20
wall_thickness = 2

# Calculate inner dimensions
square_inner = square_side - 2 * wall_thickness
cylinder_radius = cylinder_diameter / 2
cylinder_inner_radius = cylinder_radius - wall_thickness

# Create the outer square base
outer_square_base = cq.Workplane("XY").box(square_side, square_side, square_height, centered=True)

# Create the outer transition section (tapered from square to circle)
# We'll create this by lofting between square and circle profiles
square_points = [
    (square_side/2, square_side/2),
    (-square_side/2, square_side/2),
    (-square_side/2, -square_side/2),
    (square_side/2, -square_side/2),
    (square_side/2, square_side/2)
]

circle_radius = cylinder_radius
circle_points = []
num_circle_points = 32
for i in range(num_circle_points):
    angle = 2 * math.pi * i / (num_circle_points - 1)
    x = circle_radius * math.cos(angle)
    y = circle_radius * math.sin(angle)
    circle_points.append((x, y))

# Create outer loft from square to circle
square_sketch = cq.Workplane("XY").moveTo(0, 0).workplane(offset=square_height/2)
for pt in square_points:
    square_sketch = square_sketch.lineTo(pt[0], pt[1])

circle_sketch = cq.Workplane("XY").moveTo(0, 0).workplane(offset=square_height/2 + transition_height)
for pt in circle_points:
    circle_sketch = circle_sketch.lineTo(pt[0], pt[1])

# Create the outer cylinder (top part)
outer_cylinder = cq.Workplane("XY").cylinder(cylinder_height, cylinder_radius, centered=False)
outer_cylinder = outer_cylinder.translate((0, 0, square_height + transition_height))

# Create the complete outer shape by combining base and cylinder
result = outer_square_base.union(outer_cylinder)

# Now create the inner hollow part
# Inner square base
inner_square_base = cq.Workplane("XY").box(square_inner, square_inner, square_height + 0.1, centered=True)
inner_square_base = inner_square_base.translate((0, 0, -0.05))

# Inner cylinder
inner_cylinder = cq.Workplane("XY").cylinder(cylinder_height + 0.1, cylinder_inner_radius, centered=False)
inner_cylinder = inner_cylinder.translate((0, 0, square_height + transition_height - 0.05))

# Create inner transition (tapered hollow from inner square to inner circle)
inner_square_pts = [
    (square_inner/2, square_inner/2),
    (-square_inner/2, square_inner/2),
    (-square_inner/2, -square_inner/2),
    (square_inner/2, -square_inner/2),
    (square_inner/2, square_inner/2)
]

inner_circle_pts = []
for i in range(num_circle_points):
    angle = 2 * math.pi * i / (num_circle_points - 1)
    x = cylinder_inner_radius * math.cos(angle)
    y = cylinder_inner_radius * math.sin(angle)
    inner_circle_pts.append((x, y))

# Create inner transition loft by creating a tapered shape
# Using multiple intermediate circles to approximate the funnel
inner_hollow = None
for h_offset in range(0, transition_height + 1, 5):
    t = h_offset / transition_height
    # Interpolate between square and circle
    current_radius = cylinder_inner_radius + t * (square_inner/2/math.sqrt(2) - cylinder_inner_radius)
    
    temp_circle = cq.Workplane("XY").circle(current_radius)
    temp_circle = temp_circle.workplane(offset=square_height + h_offset)
    
    if inner_hollow is None:
        inner_hollow = temp_circle.extrude(5)
    else:
        inner_hollow = inner_hollow.union(temp_circle.extrude(5))

# Combine all inner holes
inner_hollow = inner_square_base.union(inner_cylinder)

# Cut the hollow from the outer shape
result = result.cut(inner_hollow)

# Also cut transition section hollow more precisely
transition_section = cq.Workplane("XY")
for h in range(square_height, square_height + transition_height):
    t = (h - square_height) / transition_height
    r = cylinder_inner_radius + t * (square_inner / (2 * math.sqrt(2)) - cylinder_inner_radius)
    temp = cq.Workplane("XY").circle(r).workplane(offset=h).extrude(1)
    transition_section = transition_section.union(temp)

result = result.cut(transition_section)
