import cadquery as cq
import math

# Create the base disc
result = cq.Workplane("XY").circle(40).extrude(10)

# Create a U-shaped groove sketch on the top surface
# The U-groove will be in the first quadrant
groove_sketch = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .transformed(offset=cq.Vector(0, 0, 10))
    .rect(10, 30, forConstruction=False)
    .vertices().fillet(2)
)

# Create the U-groove by cutting a rectangular profile
# Position it at the top surface in the first quadrant
u_groove = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(0, 0, 10))
    .moveTo(15, 0)
    .rect(10, 30)
    .extrude(-10)
)
result = result.cut(u_groove)

# Create a semicircular cutout in the adjacent quadrant (second quadrant)
# Semicircle with radius 20mm along the circular edge
semi_cutout = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(0, 0, 10))
    .moveTo(0, 0)
    .polyline([(20, 0), (20*math.cos(math.pi/4), 20*math.sin(math.pi/4)), 
               (0, 20), (-20*math.cos(math.pi/4), 20*math.sin(math.pi/4)), 
               (-20, 0)], includeCurrent=False)
    .close()
    .extrude(-10)
)
result = result.cut(semi_cutout)

# Create a combined sketch of both features for circular array
# First, let's redo this more carefully with proper positioning
result = cq.Workplane("XY").circle(40).extrude(10)

# Create individual cuts and array them
# U-groove cut positioned at 0 degrees
def create_u_groove():
    return (
        cq.Workplane("XY")
        .transformed(offset=cq.Vector(0, 0, 10))
        .moveTo(15, 0)
        .rect(10, 30)
        .extrude(-10)
    )

# Semicircular cutout positioned at 90 degrees (adjacent quadrant)
def create_semi_cutout():
    # Create semicircle centered at (0, 25) with radius 20
    semicircle_points = []
    for i in range(51):
        angle = i * math.pi / 50
        x = 25 - 20 * math.cos(angle)
        y = 20 * math.sin(angle)
        semicircle_points.append((x, y))
    
    sketch = cq.Workplane("XY").transformed(offset=cq.Vector(0, 0, 10))
    sketch = sketch.polyline(semicircle_points, includeCurrent=False)
    sketch = sketch.lineTo(25, 0).close()
    return sketch.extrude(-10)

# Apply individual cuts
result = result.cut(create_u_groove())
result = result.cut(create_semi_cutout())

# Create arrays by manual rotation (4x circular array at 90-degree intervals)
for i in range(1, 4):
    angle = i * 90
    # Rotate the U-groove
    groove_rotated = (
        cq.Workplane("XY")
        .transformed(offset=cq.Vector(0, 0, 10))
        .moveTo(15, 0)
        .rect(10, 30)
        .extrude(-10)
        .rotate((0, 0, 0), (0, 0, 1), angle)
    )
    result = result.cut(groove_rotated)
    
    # Rotate the semicircular cutout
    semi_rotated = create_semi_cutout().rotate((0, 0, 0), (0, 0, 1), angle)
    result = result.cut(semi_rotated)

# Cut the center hole with diameter 10mm (radius 5mm)
result = result.cut(cq.Workplane("XY").circle(5).extrude(-10))
