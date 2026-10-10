import cadquery as cq
import math

# Create the base disc
base_disc = cq.Workplane("XY").circle(50).extrude(10)

# Parameters for frustums
base_diameter = 20
top_diameter = 10
frustum_height = 15
num_frustums = 3
angle_step = 360 / num_frustums

# Create frustums and add them to the base
part = base_disc

for i in range(num_frustums):
    angle = i * angle_step
    radius_from_center = 30
    
    x = radius_from_center * math.cos(math.radians(angle))
    y = radius_from_center * math.sin(math.radians(angle))
    
    # Create a frustum by creating a cone-like shape
    # Use loft to create a frustum between two circles
    sketch_base = cq.Workplane("XY").moveTo(x, y).circle(base_diameter / 2)
    sketch_top = cq.Workplane("XY").moveTo(x, y).circle(top_diameter / 2).workplane(offset=frustum_height)
    
    frustum = sketch_base.loft(sketch_top)
    part = part.union(frustum)

# Create three through-holes at the center of each frustum
for i in range(num_frustums):
    angle = i * angle_step
    radius_from_center = 30
    
    x = radius_from_center * math.cos(math.radians(angle))
    y = radius_from_center * math.sin(math.radians(angle))
    
    # Create a through-hole
    hole = (cq.Workplane("XY")
            .moveTo(x, y)
            .circle(5 / 2)
            .cutThruAll())
    
    part = part.cut(hole)

result = part
