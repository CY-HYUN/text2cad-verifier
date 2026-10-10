import cadquery as cq
import math

R = 25
sphere = cq.Workplane("XY").sphere(R)

L = R + 20
# nozzles along X
nx = cq.Workplane("YZ").circle(15).extrude(L, both=True)
ny = cq.Workplane("XZ").circle(15).extrude(L, both=True)

body = sphere.union(nx).union(ny)

# flat on top
zf = math.sqrt(R**2 - 10**2)
cutter = cq.Workplane("XY").workplane(offset=zf).rect(200, 200).extrude(50)
body = body.cut(cutter)

# through holes
hx = cq.Workplane("YZ").circle(10).extrude(L + 5, both=True)
hy = cq.Workplane("XZ").circle(10).extrude(L + 5, both=True)
result = body.cut(hx).cut(hy)
