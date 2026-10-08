import cadquery as cq

# Main body: circle D60 at origin merged with an 80 x 20 rectangle along +X
circle = cq.Workplane("XY").circle(30).extrude(15)
rod = cq.Workplane("XY").center(40, 0).rect(80, 20).extrude(15)
body = circle.union(rod)

# Through cut: D30 hole at X = 5 on the top face
body = body.faces(">Z").workplane(centerOption="ProjectedOrigin", origin=(0, 0, 0)) \
    .center(5, 0).circle(15).cutThruAll()

# Through cut: D10 hole near the end of the connecting rod
body = body.faces(">Z").workplane(centerOption="ProjectedOrigin", origin=(0, 0, 0)) \
    .center(70, 0).circle(5).cutThruAll()

result = body
