import cadquery as cq
import math

# Ring dimensions
outer_d = 100.0
inner_d = 60.0
thickness = 20.0

# Tooth dimensions
tooth_w = 5.0
tooth_h = 3.0
n_teeth = 12

# Base ring, extruded 20 mm along Z
ring = (
    cq.Workplane("XY")
    .circle(outer_d / 2)
    .circle(inner_d / 2)
    .extrude(thickness)
)

r_in = inner_d / 2
# Small overlap so each tooth fuses cleanly with the ring
overlap = 0.5
tooth_len = tooth_h + overlap
# Radial centre of the tooth: it runs from r_in - 3 up to r_in + overlap
center_r = r_in - tooth_h + tooth_len / 2

result = ring
for i in range(n_teeth):
    ang = 360.0 / n_teeth * i
    tooth = (
        cq.Workplane("XY")
        .center(center_r, 0)
        .rect(tooth_len, tooth_w)
        .extrude(thickness)
        .rotate((0, 0, 0), (0, 0, 1), ang)
    )
    result = result.union(tooth)
