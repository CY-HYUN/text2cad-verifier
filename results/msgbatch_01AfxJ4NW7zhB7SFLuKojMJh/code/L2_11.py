import cadquery as cq

block = cq.Workplane("XY").box(60, 40, 40, centered=(True, True, False))

# vertical holes from top down to z=10
holes = (cq.Workplane("XY").workplane(offset=10)
         .pushPoints([(-15, 0), (15, 0)]).circle(5).extrude(30))

# horizontal channel at z=10 connecting the holes
channel = (cq.Workplane("YZ").workplane(offset=-15)
           .center(0, 10).circle(5).extrude(30))

result = block.cut(holes).cut(channel)
