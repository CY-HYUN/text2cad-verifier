import cadquery as cq
import math

outer_d = 100.0
inner_d = 60.0
thickness = 20.0
tooth_w = 5.0
tooth_h = 3.0
n_teeth = 12

ri = inner_d / 2.0

# Base ring
result = (
    cq.Workplane("XY")
    .circle(outer_d / 2.0)
    .circle(ri)
    .extrude(thickness)
)

# Single tooth: rectangle 5 wide, extending 3 mm inward from the inner edge
# (small overlap into the ring to guarantee a solid union)
overlap = 0.5
tooth_len = tooth_h + overlap
tooth_center_x = ri - tooth_h + tooth_len / 2.0

for i in range(n_teeth):
    ang = 360.0 / n_teeth * i
    tooth = (
        cq.Workplane("XY")
        .center(tooth_center_x, 0)
        .rect(tooth_len, tooth_w)
        .extrude(thickness)
        .rotate((0, 0, 0), (0, 0, 1), ang)
    )
    result = result.union(tooth)
