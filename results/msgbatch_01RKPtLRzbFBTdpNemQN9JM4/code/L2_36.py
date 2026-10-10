import cadquery as cq
import math

ring = cq.Workplane("XY").circle(60).circle(40).extrude(20)

pts = [(50*math.cos(math.radians(60*i)), 50*math.sin(math.radians(60*i))) for i in range(6)]

# through holes
through = cq.Workplane("XY").pushPoints(pts).circle(3).extrude(20)
# counterbores from top
cb = cq.Workplane("XY").workplane(offset=10).pushPoints(pts).circle(5).extrude(10)

result = ring.cut(through).cut(cb)
