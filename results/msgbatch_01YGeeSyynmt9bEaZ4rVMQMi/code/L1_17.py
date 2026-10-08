import cadquery as cq

# Base block: 60 (X) x 20 (Y) x 30 (Z), sketched on XY and extruded up
block = cq.Workplane("XY").rect(60.0, 20.0).extrude(30.0)

# Semicircular profile on the front face (XZ plane), centered at bottom edge midpoint
arch = (
    cq.Workplane("XZ", origin=(0, 10.0, 0))
    .moveTo(-20.0, 0)
    .threePointArc((0, 20.0), (20.0, 0))
    .close()
    .extrude(20.0)  # XZ normal is -Y, so this goes from y=10 to y=-10
)

result = block.cut(arch)
