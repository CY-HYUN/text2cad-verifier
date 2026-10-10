import cadquery as cq
import math

sphere = cq.Workplane("XY").sphere(25)

# cylinders along +X, -X, +Y, -Y : from x=20 to x=45
cylX = cq.Workplane("YZ").workplane(offset=20).circle(15).extrude(25)
cylXn = cq.Workplane("YZ").workplane(offset=-45).circle(15).extrude(25)
cylY = cq.Workplane("XZ").workplane(offset=-45).circle(15).extrude(25)   # XZ normal is -Y
cylYn = cq.Workplane("XZ").workplane(offset=20).circle(15).extrude(25)

body = sphere.union(cylX).union(cylXn).union(cylY).union(cylYn)

# through holes along X and Y
holeX = cq.Workplane("YZ").workplane(offset=-50).circle(10).extrude(100)
holeY = cq.Workplane("XZ").workplane(offset=-50).circle(10).extrude(100)
body = body.cut(holeX).cut(holeY)

# flat circular platform of diameter 20 on top
zc = math.sqrt(25**2 - 10**2)
cutter = cq.Workplane("XY").workplane(offset=zc).rect(200, 200).extrude(50)
result = body.cut(cutter)
