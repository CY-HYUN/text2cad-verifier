import cadquery as cq
import math

body = cq.Workplane("XY").ellipse(40.0, 25.0).extrude(25.0)

# through hole on top face
body = body.faces(">Z").workplane(centerOption="CenterOfBoundBox").center(10.0, 0.0).circle(8.0).cutThruAll()

# chamfer outer ellipse edge of top face
# select top-face edges, pick the outer one (the ellipse, not the circle)
top_edges = body.faces(">Z").edges()
outer = top_edges.edges(cq.selectors.BoxSelector((-41, -26, 24), (41, 26, 26)))
# choose the edge with largest bounding box
edges = body.faces(">Z").edges().vals()
outer_edge = max(edges, key=lambda e: e.BoundingBox().xlen)
result = body.newObject([outer_edge]).chamfer(0.8)
