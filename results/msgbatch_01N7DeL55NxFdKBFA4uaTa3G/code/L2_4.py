import cadquery as cq

# Base plate 100x100x15 with filleted vertical edges
base = (
    cq.Workplane("XY")
    .rect(100, 100)
    .extrude(15)
    .edges("|Z")
    .fillet(10)
)

# Bearing seat main body: ring OD60 / ID40, 40mm tall on top of base
boss = (
    cq.Workplane("XY")
    .workplane(offset=15)
    .circle(30)
    .circle(20)
    .extrude(40)
)

result = base.union(boss)

# Through hole in center (through the base as well)
center_hole = cq.Workplane("XY").workplane(offset=-1).circle(20).extrude(60)
result = result.cut(center_hole)

# Four mounting holes D10 at corners of 80mm square
holes = (
    cq.Workplane("XY")
    .workplane(offset=-1)
    .rect(80, 80, forConstruction=True)
    .vertices()
    .circle(5)
    .extrude(20)
)
result = result.cut(holes)
