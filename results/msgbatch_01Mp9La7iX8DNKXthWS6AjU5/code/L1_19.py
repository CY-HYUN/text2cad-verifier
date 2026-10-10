import cadquery as cq

ring1 = (cq.Workplane("XY")
         .circle(40.0).circle(30.0)
         .extrude(20.0))

ring2 = (cq.Workplane("XY")
         .circle(40.0).circle(30.0)
         .extrude(20.0))

result = cq.Workplane("XY").newObject([
    cq.Compound.makeCompound([ring1.val(), ring2.val()])
])
