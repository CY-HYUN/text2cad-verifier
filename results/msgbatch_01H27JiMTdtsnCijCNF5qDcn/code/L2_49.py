import cadquery as cq
import math

# Entity 1: circle (r=3) offset 20 from the Y axis, revolved about Y -> horizontal ring (lies in XZ plane)
ring1 = (
    cq.Workplane("XY")
    .center(20, 0)
    .circle(3)
    .revolve(360, (-20, 0, 0), (-20, 1, 0))
)

# Entity 2: circle (r=3) offset 10 from the X axis, revolved about X -> vertical ring (lies in YZ plane),
# then centered at z=20 so it links through Entity 1's hole without touching it
ring2 = (
    cq.Workplane("XY")
    .center(0, 10)
    .circle(3)
    .revolve(360, (0, -10, 0), (1, -10, 0))
    .translate((0, 0, 20))
)

s1 = ring1.val()
s2 = ring2.val()
result = cq.Workplane("XY").newObject([cq.Compound.makeCompound([s1, s2])])
