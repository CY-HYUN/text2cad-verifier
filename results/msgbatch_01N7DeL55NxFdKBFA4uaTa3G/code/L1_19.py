import cadquery as cq

# Both rings described have OD 80 mm and ID 60 mm, so they coincide;
# they are modelled here as a single ring.
outer_d = 80.0
inner_d = 60.0
height = 20.0

ring = (
    cq.Workplane("XY")
    .circle(outer_d / 2.0)
    .circle(inner_d / 2.0)
    .extrude(height)
)

result = ring
