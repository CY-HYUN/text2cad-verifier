import cadquery as cq

L, W, H = 100.0, 40.0, 30.0
groove_r = 10.0
pocket_len, pocket_h, pocket_d = 60.0, 10.0, 5.0
pocket_zc = 12.0

# Main body
body = cq.Workplane("XY").box(L, W, H, centered=(True, True, False))

# Semicircular groove along the length on the top face
groove = (
    cq.Workplane("YZ")
    .workplane(offset=-L / 2 - 1)
    .center(0, H)
    .circle(groove_r)
    .extrude(L + 2)
)
body = body.cut(groove)

# Rectangular weight-reduction pockets on both long sides
for s in (1, -1):
    pocket = (
        cq.Workplane("XY")
        .box(pocket_len, pocket_d * 2, pocket_h)
        .translate((0, s * W / 2, pocket_zc))
    )
    body = body.cut(pocket)

result = body
