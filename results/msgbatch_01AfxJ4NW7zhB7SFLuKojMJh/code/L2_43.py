import cadquery as cq

h = 20.0
frame = (cq.Workplane("XY")
         .rect(60, 60).extrude(h)
         .faces(">Z").workplane()
         .rect(40, 40).cutThruAll())

cyl = cq.Workplane("XY").circle(20).extrude(h)

result = cq.Workplane("XY").newObject([
    cq.Compound.makeCompound([frame.val(), cyl.val()])
])
