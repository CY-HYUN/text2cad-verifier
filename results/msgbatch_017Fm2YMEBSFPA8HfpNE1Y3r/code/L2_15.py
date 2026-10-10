import cadquery as cq
import math

# Create the base disc
result = cq.Workplane("XY").circle(40).extrude(10)

# Create U-groove cut positioned at 0 degrees
def create_u_groove():
    return (
        cq.Workplane("XY")
        .moveTo(15, 0)
        .rect(10, 30)
        .extrude(-10)
    )

# Create semicircular cutout positioned at 90 degrees
def create_semi_cutout():
    # Create semicircle as a half-circle cutout at the edge
    sketch = cq.Workplane("XY")
    
    # Create a semicircle profile centered at distance 25 from origin
    semicircle_points = []
    for i in range(51):
        angle = i * math.pi / 50
        x = 25 + 20 * math.cos(angle)
        y = 20 * math.sin(angle)
        semicircle_points.append((x, y))
    
    sketch = sketch.polyline(semicircle_points, includeCurrent=False)
    sketch = sketch.lineTo(25, 0).close()
    return sketch.extrude(-10)

# Apply the base cuts
result = result.cut(create_u_groove())

# Rotate and cut the semicircle
semi_cutout = create_semi_cutout()
result = result.cut(semi_cutout)

# Create 4x circular array (90-degree intervals) for the remaining 3 positions
for i in range(1, 4):
    angle = i * 90
    
    # Rotate U-groove cut
    groove_tool = cq.Workplane("XY").moveTo(15, 0).rect(10, 30).extrude(-10)
    groove_rotated = groove_tool.rotate((0, 0, 0), (0, 0, 1), angle)
    result = result.cut(groove_rotated)
    
    # Rotate semicircular cutout
    semi_tool = cq.Workplane("XY")
    semicircle_points = []
    for j in range(51):
        angle_semi = j * math.pi / 50
        x = 25 + 20 * math.cos(angle_semi)
        y = 20 * math.sin(angle_semi)
        semicircle_points.append((x, y))
    
    semi_tool = semi_tool.polyline(semicircle_points, includeCurrent=False)
    semi_tool = semi_tool.lineTo(25, 0).close().extrude(-10)
    semi_rotated = semi_tool.rotate((0, 0, 0), (0, 0, 1), angle)
    result = result.cut(semi_rotated)

# Cut the center hole with diameter 10mm (radius 5mm)
center_hole = cq.Workplane("XY").circle(5).extrude(-10)
result = result.cut(center_hole)
