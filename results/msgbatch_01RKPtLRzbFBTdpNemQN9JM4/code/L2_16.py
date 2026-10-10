import cadquery as cq
import math

R = 25.0
sphere = cq.Workplane("XY").sphere(R)

# nozzles along X and Y: from sphere surface (25) to 45, start inside the sphere at 20
def cyl_x(x0, x1):
    return (cq.Workplane("YZ").workplane(offset=x0).circle(15).extrude(x1 - x0))

def cyl_y(y0, y1):
    return (cq.Workplane("XZ").workplane(offset=-y1).circle(15).extrude(y1 - y0))

body = sphere
body = body.union(cyl_x(20, 45))
body = body.union(cyl_x(-45, -20))
body = body.union(cyl_y(20, 45))
body = body.union(cyl_y(-45, -20))

# top flat: 20mm diameter circle on sphere -> plane at z = sqrt(R^2 - 10^2)
zf = math.sqrt(R**2 - 10**2)
cutter = cq.Workplane("XY").workplane(offset=zf).rect(200, 200).extrude(50)
body = body.cut(cutter)

# through holes
hole_x = cq.Workplane("YZ").workplane(offset=-60).circle(10).extrude(120)
hole_y = cq.Workplane("XZ").workplane(offset=-60).circle(10).extrude(120)
body = body.cut(hole_x).cut(hole_y)

result = body
