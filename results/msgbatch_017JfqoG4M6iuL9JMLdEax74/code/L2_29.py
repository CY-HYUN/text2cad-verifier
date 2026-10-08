import cadquery as cq
import math

outer_d = 100.0
thickness = 20.0
bore_d = 60.0
n_teeth = 12
tooth_w = 5.0
tooth_h = 5.0

# Main ring
ring = (
    cq.Workplane("XY")
    .circle(outer_d / 2)
    .circle(bore_d / 2)
    .extrude(thickness)
)

# Internal teeth (slight overlap into wall for clean union)
r_in = bore_d / 2 - tooth_h
overlap = 1.0
radial_len = tooth_h + overlap
r_center = r_in + radial_len / 2

result = ring
for i in range(n_teeth):
    ang = 360.0 / n_teeth * i
    tooth = (
        cq.Workplane("XY")
        .box(radial_len, tooth_w, thickness, centered=(True, True, False))
        .translate((r_center, 0, 0))
        .rotate((0, 0, 0), (0, 0, 1), ang)
    )
    result = result.union(tooth)
