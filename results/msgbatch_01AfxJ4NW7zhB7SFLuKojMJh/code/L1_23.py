import cadquery as cq

big = cq.Workplane("XY").center(0, 0).circle(25).extrude(50)
small = cq.Workplane("XY").center(40, 0).circle(15).extrude(50)

result = cq.Workplane("XY").newObject([
    cq.Compound.makeCompound([big.val(), small.val()])
])
