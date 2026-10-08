import cadquery as cq

# Base plate 60 x 60 x 10
base = cq.Workplane("XY").box(60, 60, 10, centered=False)

# Fin parameters
fin_t = 2.0
fin_len = 60.0
fin_h = 40.0
n = 10
spacing = (60.0 - fin_t) / (n - 1)  # 58/9 so the fins span the full base

result = base
for i in range(n):
    x = i * spacing
    fin = (
        cq.Workplane("XY")
        .workplane(offset=10)
        .center(x + fin_t / 2, fin_len / 2)
        .rect(fin_t, fin_len)
        .extrude(fin_h)
    )
    result = result.union(fin)

result = result.clean()
