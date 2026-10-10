import cadquery as cq
import math

# Create the base ring
base_ring = cq.Workplane("XY").cylinder(height=20, radius=60, centered=True)
base_ring = base_ring.cut(cq.Workplane("XY").cylinder(height=20, radius=40, centered=True))

# Create the counterbore holes
# 6 holes evenly distributed on a pitch circle of diameter 100mm (radius 50mm)
# Each hole: 10mm diameter counterbore to 10mm depth, then 6mm diameter through-hole

holes = cq.Workplane("XY")

for i in range(6):
    angle = i * (360 / 6)
    angle_rad = math.radians(angle)
    
    # Calculate position on pitch circle
    x = 50 * math.cos(angle_rad)
    y = 50 * math.sin(angle_rad)
    
    # Create counterbore hole at this position
    # Counterbore: 10mm diameter, 10mm deep
    counterbore = cq.Workplane("XY").workplane(offset=10).cylinder(
        height=10, radius=5, centered=True
    ).translate((x, y, 0))
    
    # Through-hole: 6mm diameter, full depth (20mm)
    through_hole = cq.Workplane("XY").cylinder(
        height=20, radius=3, centered=True
    ).translate((x, y, 0))
    
    # Combine holes
    holes = holes.union(counterbore)
    holes = holes.union(through_hole)

# Cut the holes from the base ring
result = base_ring.cut(holes)
