import cadquery as cq

# Frustum: 80 mm square at the bottom, 50 mm square at the top, 45 mm tall
bottom = cq.Workplane("XY").rect(80, 80)
top = bottom.workplane(offset=45).rect(50, 50)
body = top.loft(combine=True)

# Square blind cavity, 30 mm wide and 15 mm deep, centred in the top face
body = (
    body.faces(">Z").workplane()
    .rect(30, 30)
    .cutBlind(-15)
)

# 1 mm chamfer on the four edges of the cavity opening:
# edges lying on the top plane (z = 45) that are inside |x|, |y| <= 15
def _cavity_top_edge(e):
    c = e.Center()
    return abs(c.z - 45) < 1e-6 and abs(c.x) <= 15.01 and abs(c.y) <= 15.01

top_edges = body.edges().vals()
sel = [e for e in top_edges if _cavity_top_edge(e)]
body = body.newObject(sel).chamfer(1)

result = body
