import cadquery as cq

R = 17.5   # mean radius (OD 40, ID 30)
r = 2.5    # tube radius

# Ring A: horizontal torus around Z axis
ringA = (
    cq.Workplane("XZ")
    .center(R, 0)
    .circle(r)
    .revolve(360, (-R, 0, 0), (-R, 1, 0))
)

# Ring B: vertical torus (axis along Y), shifted so it passes through A's hole
ringB = (
    ringA.rotate((0, 0, 0), (1, 0, 0), 90)
    .translate((R, 0, 0))
)

result = cq.Workplane("XY").newObject(
    [cq.Compound.makeCompound([ringA.val(), ringB.val()])]
)
