import cadquery as cq
import math

result = (
    cq.Workplane("XY")
    .ellipse(40.0, 25.0)
    .extrude(25.0)
)

# through hole from top face
result = (
    result.faces(">Z").workplane(centerOption="CenterOfBoundBox")
    .center(10.0, 0.0)
    .circle(8.0)
    .cutThruAll()
)

# chamfer outer ellipse edge on top face (select the edge by size)
top_edges = result.faces(">Z").edges()
# outer ellipse edge: the one with the largest bounding box
outer = max(top_edges.vals(), key=lambda e: e.BoundingBox().xlen)
result = result.newObject([outer]).chamfer(0.8)
