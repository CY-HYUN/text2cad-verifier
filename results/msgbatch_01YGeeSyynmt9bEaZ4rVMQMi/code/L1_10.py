import cadquery as cq

# Base block: 100 x 50 footprint centred on XY, extruded 30 mm up
block = cq.Workplane("XY").rect(100.0, 50.0).extrude(30.0)

# Slot on top face: 100 long (full length) x 20 wide, 15 deep, cut downward
slot = (
    cq.Workplane("XY")
    .workplane(offset=30.0 - 15.0)
    .rect(100.0, 20.0)
    .extrude(15.0)
)

result = block.cut(slot)
