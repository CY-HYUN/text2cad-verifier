import cadquery as cq

# Cylindrical body: 40 mm diameter, 40 mm tall, base on Z=0
result = cq.Workplane("XY").circle(20).extrude(40)

# Lower through-hole, 10 mm diameter, full height
result = result.faces(">Z").workplane().hole(10)

# Upper counterbore from the top face: 20 mm diameter, 10 mm deep
cbore = cq.Workplane("XY").workplane(offset=30).circle(10).extrude(10)
result = result.cut(cbore)
