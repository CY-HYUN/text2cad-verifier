import cadquery as cq

# Main body: solid cylinder, D = 30 mm, H = 60 mm, axis along Z (base at Z = 0)
body = cq.Workplane("XY").circle(15).extrude(60)

# Transverse through-hole: D = 10 mm along Y, at mid-height (Z = 30)
hole = (
    cq.Workplane("XZ", origin=(0, 0, 30))
    .circle(5)
    .extrude(20, both=True)
)

result = body.cut(hole)
