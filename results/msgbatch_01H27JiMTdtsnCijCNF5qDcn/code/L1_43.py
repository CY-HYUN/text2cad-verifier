import cadquery as cq

# Outer solid: 100 x 50 x 30, centered in XY, base on Z=0
outer = cq.Workplane("XY").rect(100.0, 50.0).extrude(30.0)

# Slot: 100 (X) x 30 (Y), cut 20 mm deep from the top face (Z=30 down to Z=10)
slot = (
    cq.Workplane("XY")
    .workplane(offset=30.0)
    .rect(100.0, 30.0)
    .extrude(-20.0)
)

result = outer.cut(slot)
