import cadquery as cq
import math

# Create the outer tube
outer_tube = cq.Workplane("XY").cylinder(height=50, radius=40, centered=True).cut(
    cq.Workplane("XY").cylinder(height=50, radius=35, centered=True)
)

# Create the inner tube
inner_tube = cq.Workplane("XY").cylinder(height=50, radius=20, centered=True).cut(
    cq.Workplane("XY").cylinder(height=50, radius=15, centered=True)
)

# Create the four ribs
# Each rib is a rectangular solid connecting the two tubes
# Ribs are 5mm thick, positioned radially at 0°, 90°, 180°, 270°

ribs = cq.Workplane("XY")

for i in range(4):
    # Angle for each rib (0°, 90°, 180°, 270°)
    angle = i * 90
    angle_rad = math.radians(angle)
    
    # Create a rib as a box that extends from inner radius to outer radius
    # Inner radius: 20mm, Outer radius: 40mm
    # Rib thickness: 5mm, Length: 50mm (same as tube length)
    
    # Position the rib at the correct angle
    # The rib extends radially from radius 20 to radius 40
    rib_center_x = (20 + 40) / 2 * math.cos(angle_rad)
    rib_center_y = (20 + 40) / 2 * math.sin(angle_rad)
    
    # Create individual rib
    single_rib = (
        cq.Workplane("XY")
        .box(20, 5, 50, centered=True)  # width=20 (from r=20 to r=40), thickness=5, height=50
        .rotate((0, 0, 0), (0, 0, 1), angle)  # Rotate to the correct angular position
    )
    
    ribs = ribs.union(single_rib)

# Combine all components
result = outer_tube.union(inner_tube).union(ribs)
