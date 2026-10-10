import cadquery as cq

box = cq.Workplane("XY").rect(60, 40).extrude(40)

# vertical blind holes from top
holes = (cq.Workplane("XY").workplane(offset=40)
         .pushPoints([(-15, 0), (15, 0)]).circle(5).extrude(-30))
box = box.cut(holes)

# horizontal channel from side face x=-30, along +X
channel = (cq.Workplane("YZ").workplane(offset=-30)
           .center(0, 15).circle(5).extrude(45))
result = box.cut(channel)
