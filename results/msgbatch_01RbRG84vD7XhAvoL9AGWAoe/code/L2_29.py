import cadquery as cq
import math

outer_d = 100.0
inner_d = 60.0
thickness = 20.0
n_teeth = 12
tooth_w = 5.0
tooth_h = 5.0

# Main ring
ring = (
    cq.Workplane("XY")
    .circle(outer_d / 2)
    .circle(inner_d / 2)
    .extrude(thickness)
)

# Teeth: extend from inner wall (r=30) toward center (r=25); overlap into wall for solid union
r_in = inner_d / 2 - tooth_h
r_out = inner_d / 2 + 1.0
radial_len = r_out - r_in
r_mid = (r_in + r_out) / 2

teeth = None
for i in range(n_teeth):
    ang = 360.0 / n_teeth * i
    t = (
        cq.Workplane("XY")
        .box(radial_len, tooth_w, thickness, centered=(True, True, False))
        .translate((r_mid, 0, 0))
        .rotate((0, 0, 0), (0, 0, 1), ang)
    )
    teeth = t if teeth is None else teeth.union(t)

result = ring.union(teeth)
