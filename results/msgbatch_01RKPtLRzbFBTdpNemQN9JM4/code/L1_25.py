import cadquery as cq

# Main cylinder: diameter 40, height 40, base at z=0
body = cq.Workplane("XY").circle(20).extrude(40)

# Through hole diameter 10
through = cq.Workplane("XY").circle(5).extrude(40)

# Counterbore diameter 20, depth 10 from the top face
cbore = cq.Workplane("XY").workplane(offset=30).circle(10).extrude(10)

result = body.cut(through).cut(cbore)
