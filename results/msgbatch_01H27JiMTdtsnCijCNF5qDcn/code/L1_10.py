import cadquery as cq

# Base block: 100 (X) x 50 (Y) x 30 (Z), centered on XY, base at z=0
block = cq.Workplane("XY").rect(100.0, 50.0).extrude(30.0)

# Slot: 100 long along X (through), 20 wide along Y, 15 deep from top face
slot = (
    cq.Workplane("XY")
    .workplane(offset=30.0)
    .rect(100.0, 20.0)
    .extrude(-15.0)
)

result = block.cut(slot)
