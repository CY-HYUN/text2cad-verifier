import cadquery as cq

# Base plate with R10 corner fillets
base = (
    cq.Workplane("XY")
    .box(100, 100, 15, centered=(True, True, False))
    .edges("|Z").fillet(10)
)

# Four corner through-holes on 80x80 pattern
base = (
    base.faces(">Z").workplane()
    .rect(80, 80, forConstruction=True)
    .vertices()
    .hole(10)
)

# Central sleeve
sleeve = (
    cq.Workplane("XY").workplane(offset=15)
    .circle(30)
    .extrude(40)
)

result = base.union(sleeve)

# Bore through sleeve and base
bore = cq.Workplane("XY").circle(20).extrude(55)
result = result.cut(bore)
