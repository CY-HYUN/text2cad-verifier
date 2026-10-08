import cadquery as cq

# Base plate: 100x100 centered, 15 mm thick
base = cq.Workplane("XY").rect(100, 100).extrude(15)

# Round the four vertical corner edges of the plate
base = base.edges("|Z").fillet(10)

# Bearing seat ring on top of the plate (OD 60, ID 40, height 40)
ring = (
    cq.Workplane("XY").workplane(offset=15)
    .circle(30).circle(20)
    .extrude(40)
)
body = base.union(ring)

# Through hole of 40 mm diameter through plate and ring
body = body.cut(
    cq.Workplane("XY").workplane(offset=-1).circle(20).extrude(60)
)

# Four 10 mm mounting holes on an 80 mm square
holes = (
    cq.Workplane("XY").workplane(offset=-1)
    .rect(80, 80, forConstruction=True)
    .vertices()
    .circle(5)
    .extrude(20)
)
result = body.cut(holes)
