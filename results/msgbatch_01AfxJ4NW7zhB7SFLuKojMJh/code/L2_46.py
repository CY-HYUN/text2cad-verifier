import cadquery as cq

R = 30.0
offset = 15.0  # each center is shifted by 15 mm in Y, so 30 mm between centers

def hemisphere(center_y, direction):
    s = cq.Workplane("XY").sphere(R).translate((0, center_y, 0))
    # keep half with x <= 0 (direction=-1) or x >= 0 (direction=+1)
    box = (cq.Workplane("XY")
           .box(R * 2, R * 4, R * 2, centered=(False, True, True)))
    if direction < 0:
        box = box.translate((-R * 2, 0, 0))
    return s.intersect(box)

left = hemisphere(-offset, -1)
right = hemisphere(offset, +1)

result = left.union(right)
