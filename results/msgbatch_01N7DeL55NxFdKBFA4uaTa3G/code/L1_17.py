import cadquery as cq

# Block: 60 (X) x 20 (Y, thickness) x 30 (Z, height)
block = cq.Workplane("XY").box(60.0, 20.0, 30.0, centered=(True, True, False))

# Semicircular arch profile on the front face (XZ), centered at bottom edge midpoint
arch = (
    cq.Workplane("XZ", origin=(0, 15.0, 0))
    .moveTo(-20.0, 0)
    .threePointArc((0, 20.0), (20.0, 0))
    .close()
    .extrude(30.0)  # through the full thickness
)

result = block.cut(arch)
