import cadquery as cq

# Horizontal bar: Ø20 x 80 along X, centered at origin
bar = cq.Workplane("YZ").circle(10).extrude(40, both=True)

# Vertical stem: Ø20 x 40 along Z, starting at bar axis and going down
stem = cq.Workplane("XY").workplane(offset=-40).circle(10).extrude(40)

result = bar.union(stem)
