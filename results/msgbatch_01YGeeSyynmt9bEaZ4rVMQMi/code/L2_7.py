import cadquery as cq

# Main body: circle + rectangular arm, merged
circle = cq.Workplane("XY").circle(30).extrude(15)
arm = cq.Workplane("XY").center(40, 0).rect(80, 20).extrude(15)
body = circle.union(arm)

# 30 mm hole at X = 5
body = body.faces(">Z").workplane(origin=(0, 0, 15)).center(5, 0).circle(15).cutThruAll()

# 10 mm hole at the end of the rod (centered in the end region)
body = body.faces(">Z").workplane(origin=(0, 0, 15)).center(70, 0).circle(5).cutThruAll()

result = body
