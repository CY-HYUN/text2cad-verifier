import cadquery as cq
import math

base = cq.Workplane("XY").circle(30).extrude(80)

ring = (cq.Workplane("XY").workplane(offset=35)
        .circle(31).circle(27).extrude(10))
body = base.cut(ring)

# fillet the groove side edges at the outer surface (radius 30, z=35 and z=45)
def sel(e):
    return True

result = body.edges(cq.selectors.BoxSelector((-31, -31, 34.9), (31, 31, 35.1))).edges(
    cq.selectors.RadiusNthSelector(1)
)
# Select outer edges (radius 30) at z=35 and z=45
result = (body.edges(cq.selectors.BoxSelector((-31, -31, 34.9), (31, 31, 35.1)))
          .edges(cq.selectors.RadiusNthSelector(1)))
outer_edges = (body.edges(cq.selectors.BoxSelector((-31, -31, 34.9), (31, 31, 35.1)))
               .edges(cq.selectors.RadiusNthSelector(1)).vals()
               + body.edges(cq.selectors.BoxSelector((-31, -31, 44.9), (31, 31, 45.1)))
               .edges(cq.selectors.RadiusNthSelector(1)).vals())
solid = body.val().fillet(1.0, outer_edges)
result = cq.Workplane("XY").newObject([solid])
