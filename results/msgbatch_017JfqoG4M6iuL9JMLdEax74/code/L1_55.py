import cadquery as cq

H = 60.0
R_bot = 35.0
R_top = 20.0
r_hole = 10.0
c = 2.0

# chamfer intersection with cone side: r = R_bot - (R_bot-R_top)/H * z, chamfer: r = (R_bot - c) + z
k = (R_bot - R_top) / H
z_c = c / (1 + k)
r_c = R_bot - c + z_c

pts = [
    (r_hole, 0),
    (R_bot - c, 0),
    (r_c, z_c),
    (R_top, H),
    (r_hole, H),
]

result = (
    cq.Workplane("XZ")
    .polyline(pts)
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)
