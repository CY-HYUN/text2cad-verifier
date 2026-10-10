import cadquery as cq
import math

R = 30.0
offset = 15.0  # each center displaced +/- in y, total misalignment 30 mm

left_sphere = cq.Workplane("XY").sphere(R).translate((0, -offset, 0))
right_sphere = cq.Workplane("XY").sphere(R).translate((0, offset, 0))

# half-space boxes
box_left = cq.Workplane("XY").box(2*R+10, 4*R, 2*R+10, centered=(False, True, True)).translate((-(2*R+10), 0, 0))
box_right = cq.Workplane("XY").box(2*R+10, 4*R, 2*R+10, centered=(False, True, True))

left_h = left_sphere.intersect(box_left)
right_h = right_sphere.intersect(box_right)

result = left_h.union(right_h)
