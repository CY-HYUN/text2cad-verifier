import cadquery as cq

# Base plate 100x100x15 with R10 vertical corner fillets
base = (
    cq.Workplane("XY")
    .box(100, 100, 15, centered=(True, True, False))
    .edges("|Z").fillet(10)
)

# Sleeve rising from top of plate
sleeve = (
    cq.Workplane("XY").workplane(offset=15)
    .circle(30).extrude(40)
)

result = base.union(sleeve)

# Central bore through the whole part
bore = cq.Workplane("XY").circle(20).extrude(55)
result = result.cut(bore)

# Four corner mounting holes on 80x80 pattern
holes = (
    cq.Workplane("XY")
    .rect(80, 80, forConstruction=True).vertices()
    .circle(5).extrude(15)
)
result = result.cut(holes)
