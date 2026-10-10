import cadquery as cq

t = 4.0
# Ring A: horizontal, centered at origin
ringA = (cq.Workplane("XY")
         .circle(20).circle(15)
         .extrude(t / 2, both=True))

# Ring B: vertical (XZ plane), offset so it threads through A's hole without touching
ringB = (cq.Workplane("XZ")
         .center(15, 0)
         .circle(20).circle(15)
         .extrude(t / 2, both=True))

result = cq.Workplane("XY").newObject([
    cq.Compound.makeCompound([ringA.val(), ringB.val()])
])
