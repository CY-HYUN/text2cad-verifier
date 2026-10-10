import cadquery as cq
import math

# Create the base disc
base_disc = cq.Workplane("XY").circle(50).extrude(10)

# Create the three frustums on top of the disc
frustums = cq.Workplane("XY")

# Parameters for frustums
base_diameter = 20
top_diameter = 10
frustum_height = 15
num_frustums = 3
angle_step = 360 / num_frustums

# Position the frustums around the center
for i in range(num_frustums):
    angle = i * angle_step
    # Distance from center to place frustums (positioned near edge for good support)
    radius_from_center = 30
    
    x = radius_from_center * math.cos(math.radians(angle))
    y = radius_from_center * math.sin(math.radians(angle))
    
    # Create a frustum as a tapered solid
    # Start with a circle at the base, extrude and taper to smaller circle at top
    frustum = (cq.Workplane("XY")
               .moveTo(x, y)
               .circle(base_diameter / 2)
               .extrude(frustum_height)
               .faces(">Z")
               .circle(top_diameter / 2)
               .cutThruAll())
    
    # Union the frustum to the main shape
    frustums = frustums.union(frustum)

# Combine base disc with frustums
part = base_disc.union(frustums)

# Create three through-holes at the center of each frustum
for i in range(num_frustums):
    angle = i * angle_step
    radius_from_center = 30
    
    x = radius_from_center * math.cos(math.radians(angle))
    y = radius_from_center * math.sin(math.radians(angle))
    
    # Create a through-hole (cylinder passing through entire part)
    hole = (cq.Workplane("XY")
            .moveTo(x, y)
            .circle(5 / 2)
            .cutThruAll())
    
    part = part.cut(hole)

result = part
