import cadquery as cq

R_out = 50.0
R_in = 40.0

# Outer sphere, trimmed to the upper hemisphere (z >= 0)
outer = cq.Workplane("XY").sphere(R_out)
box_o = cq.Workplane("XY").box(
    4 * R_out, 4 * R_out, 2 * R_out, centered=(True, True, False)
)
outer_h = outer.intersect(box_o)

# Inner sphere, trimmed the same way
inner = cq.Workplane("XY").sphere(R_in)
box_i = cq.Workplane("XY").box(
    4 * R_in, 4 * R_in, 2 * R_in, centered=(True, True, False)
)
inner_h = inner.intersect(box_i)

# Outer hemisphere minus inner hemisphere gives a 10 mm wall
result = outer_h.cut(inner_h)
