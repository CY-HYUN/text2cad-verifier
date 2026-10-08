import cadquery as cq

# Base plate 60 x 60 x 10
L = 60.0
W = 60.0
T = 10.0
base = cq.Workplane("XY").box(L, W, T, centered=(False, False, False))

# Fin: 2 mm (X) x 60 mm (Y) rectangle, extruded 40 mm upward from top face
fin_t = 2.0
fin_h = 40.0
n = 10
spacing = (L - fin_t) / (n - 1)  # 58/9 so outer fins sit flush with plate edges

result = base
for i in range(n):
    x = i * spacing
    fin = (
        cq.Workplane("XY")
        .workplane(offset=T)
        .center(x + fin_t / 2.0, W / 2.0)
        .rect(fin_t, W)
        .extrude(fin_h)
    )
    result = result.union(fin)

result = result.clean()
