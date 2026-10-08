import cadquery as cq

# Disc: diameter 60 mm, thickness 10 mm
disc = cq.Workplane("XY").circle(30.0).extrude(10.0)

# Cutout circle (diameter 60 mm) centered on the outer edge at (30, 0), through all
cutter = (
    cq.Workplane("XY")
    .center(30.0, 0)
    .circle(30.0)
    .extrude(10.0)
)

result = disc.cut(cutter)
