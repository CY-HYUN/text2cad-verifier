import cadquery as cq
import math

R = 25.0
sphere = cq.Workplane("XY").sphere(R)

# Four bosses along +/-X and +/-Y; each starts where its rim meets the sphere
cyl_r = 15.0
cyl_len = 20.0
start = math.sqrt(R**2 - cyl_r**2)  # 20 mm

body = sphere
# +X / -X
cx = (cq.Workplane("YZ").workplane(offset=start).circle(cyl_r).extrude(cyl_len))
cxn = (cq.Workplane("YZ").workplane(offset=-start).circle(cyl_r).extrude(-cyl_len))
# +Y / -Y
cy = (cq.Workplane("XZ").workplane(offset=-start).circle(cyl_r).extrude(-cyl_len))
cyn = (cq.Workplane("XZ").workplane(offset=start).circle(cyl_r).extrude(cyl_len))
body = body.union(cx).union(cxn).union(cy).union(cyn)

# Through holes along X and Y (diameter 20)
L = 200
hx = cq.Workplane("YZ").circle(10).extrude(L / 2, both=True)
hy = cq.Workplane("XZ").circle(10).extrude(L / 2, both=True)
body = body.cut(hx).cut(hy)

# Flat circular platform on top, diameter 20
z_cut = math.sqrt(R**2 - 10**2)
top_cut = cq.Workplane("XY").workplane(offset=z_cut).rect(200, 200).extrude(50)
body = body.cut(top_cut)

result = body
