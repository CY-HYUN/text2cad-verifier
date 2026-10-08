import cadquery as cq
import math

R = 25.0
sphere = cq.Workplane("XY").sphere(R)

# Four bosses along +/-X and +/-Y, each protruding 20 mm beyond the sphere surface
cyl_r = 15.0
cyl_len = 20.0
reach = R + cyl_len  # 45 mm from centre

cx = cq.Workplane("YZ").circle(cyl_r).extrude(reach, both=True)
cy = cq.Workplane("XZ").circle(cyl_r).extrude(reach, both=True)
body = sphere.union(cx).union(cy)

# Through holes along X and Y (diameter 20)
hx = cq.Workplane("YZ").circle(10).extrude(100, both=True)
hy = cq.Workplane("XZ").circle(10).extrude(100, both=True)
body = body.cut(hx).cut(hy)

# Flat circular platform on top, diameter 20
z_cut = math.sqrt(R**2 - 10**2)
top_cut = cq.Workplane("XY").workplane(offset=z_cut).rect(200, 200).extrude(50)
body = body.cut(top_cut)

result = body
