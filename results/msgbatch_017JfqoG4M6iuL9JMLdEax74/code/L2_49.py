import cadquery as cq

R = 17.5   # centerline radius (OD 40, ID 30)
r = 2.5    # tube radius

# Ring A: horizontal (in XY plane), axis along Z, centered at origin
ringA = (
    cq.Workplane("XZ")
    .center(R, 0)
    .circle(r)
    .revolve(360, (-R, 0, 0), (-R, 1, 0))
)

# Ring B: vertical (in XZ plane), axis along Y, centered at (R,0,0)
# passes through the hole of Ring A
ringB = (
    cq.Workplane("XY")
    .center(2 * R, 0)
    .circle(r)
    .revolve(360, (-R, 0, 0), (-R, 1, 0))
)

result = ringA.union(ringB)
