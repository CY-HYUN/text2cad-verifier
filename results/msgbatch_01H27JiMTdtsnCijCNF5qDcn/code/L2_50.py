import cadquery as cq
import math

# Stepped shaft revolved about X axis
pts = [(0,0),(0,10),(30,10),(30,15),(80,15),(80,10),(110,10),(110,0)]
body = (cq.Workplane("XY").polyline(pts).close()
        .revolve(360,(0,0,0),(1,0,0)))

# Groove: 20 long (X) x 6 wide (Y), cut 3.5 mm down from the tangent plane z=15
groove = (cq.Workplane("XY").workplane(offset=15-3.5)
          .center(55,0).rect(20,6).extrude(5))
body = body.cut(groove)

# End holes dia 5, depth 10
left = cq.Workplane("YZ").circle(2.5).extrude(10)
right = cq.Workplane("YZ").workplane(offset=100).circle(2.5).extrude(10)
body = body.cut(left).cut(right)

result = body
