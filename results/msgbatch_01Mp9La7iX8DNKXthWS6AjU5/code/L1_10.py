import cadquery as cq

# Base block: 100 (X) x 50 (Y) x 30 (Z), centered on XY, sitting on Z=0..30
base = cq.Workplane("XY").rect(100.0, 50.0).extrude(30.0)

# Through-length slot on top: 100 long (X) x 20 wide (Y), depth 15
slot = (
    cq.Workplane("XY")
    .workplane(offset=30.0)
    .rect(100.0, 20.0)
    .extrude(-15.0)
)

result = base.cut(slot)
