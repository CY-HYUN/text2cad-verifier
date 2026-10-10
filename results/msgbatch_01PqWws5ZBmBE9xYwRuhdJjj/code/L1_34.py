import cadquery as cq

# Create the lower cuboid (100mm x 60mm x 20mm)
lower_cuboid = cq.Workplane("XY").rect(100.0, 60.0).extrude(20.0)

# Create the upper rectangle on top of the lower cuboid
# It should be centered (100mm x 30mm) and extruded 20mm
upper_rect = (
    cq.Workplane("XY")
    .workplane(offset=20.0)  # Move to the top surface of lower cuboid
    .rect(100.0, 30.0)
    .extrude(20.0)
)

# Merge the two parts to form the T-shaped slider
result = lower_cuboid.union(upper_rect)
