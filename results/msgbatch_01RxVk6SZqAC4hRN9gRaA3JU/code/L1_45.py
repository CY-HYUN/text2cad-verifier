import cadquery as cq

R_out = 50.0
R_in = 40.0

# Outer sphere, cut down to the upper hemisphere (z >= 0)
outer = cq.Workplane("XY").sphere(R_out)
outer_half = outer.intersect(
    cq.Workplane("XY").box(200, 200, 100, centered=(True, True, False))
)

# Inner sphere, cut down to the upper hemisphere (z >= 0)
inner = cq.Workplane("XY").sphere(R_in)
inner_half = inner.intersect(
    cq.Workplane("XY").box(200, 200, 100, centered=(True, True, False))
)

# Subtract inner hemisphere to leave a 10 mm wall
result = outer_half.cut(inner_half)
