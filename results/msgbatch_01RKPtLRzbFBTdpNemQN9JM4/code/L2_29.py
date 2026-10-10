import cadquery as cq
import math

thickness = 20.0
outer_d = 100.0
hole_d = 60.0
n_teeth = 12
tooth_w = 5.0
tooth_h = 5.0

ring = (
    cq.Workplane("XY")
    .circle(outer_d / 2)
    .circle(hole_d / 2)
    .extrude(thickness)
)

r_hole = hole_d / 2
# Tooth extends from slightly inside the wall (for a solid union) toward the center
overlap = 2.0
length = tooth_h + overlap
# center of tooth radially: outer end at r_hole + overlap, inner end at r_hole - tooth_h
r_center = (r_hole + overlap + (r_hole - tooth_h)) / 2

result = ring
for i in range(n_teeth):
    ang = i * 360.0 / n_teeth
    tooth = (
        cq.Workplane("XY")
        .box(length, tooth_w, thickness, centered=(True, True, False))
        .translate((r_center, 0, 0))
        .rotate((0, 0, 0), (0, 0, 1), ang)
    )
    result = result.union(tooth)
