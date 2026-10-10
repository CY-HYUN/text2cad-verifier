import cadquery as cq

r = 2.0
R = 10.0

# Entity 1: horizontal ring (circle in XY plane, revolved about Y axis)
ring1 = (
    cq.Workplane("XY")
    .center(R, 0)
    .circle(r)
    .revolve(360, (-R, 0, 0), (-R, 1, 0))
)

# Entity 2: vertical ring (circle in YZ plane, revolved about X axis),
# shifted along X so it encircles ring 1's tube
ring2 = (
    cq.Workplane("YZ")
    .center(R, 0)
    .circle(r)
    .revolve(360, (-R, 0, 0), (-R, 1, 0))
    .translate((R, 0, 0))
)

result = ring1.add(ring2)
result = cq.Workplane("XY").newObject([cq.Compound.makeCompound([ring1.val(), ring2.val()])])
