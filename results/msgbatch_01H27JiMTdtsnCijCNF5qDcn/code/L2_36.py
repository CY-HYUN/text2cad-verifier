import cadquery as cq
import math

ring = (cq.Workplane("XY")
        .circle(60).circle(40)
        .extrude(20))

pcd_r = 50
pts = [(pcd_r*math.cos(math.radians(60*i)), pcd_r*math.sin(math.radians(60*i))) for i in range(6)]

# through holes
thru = (cq.Workplane("XY").pushPoints(pts).circle(3).extrude(20))
# counterbore (diameter 10, depth 10) from top
cb = (cq.Workplane("XY").workplane(offset=10).pushPoints(pts).circle(5).extrude(10))

result = ring.cut(thru).cut(cb)
