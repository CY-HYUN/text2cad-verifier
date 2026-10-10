import cadquery as cq

L = 100.0
r_in = 10.0
r_out = 15.0
flange_r = 25.0
flange_t = 5.0
baffle_r = 20.0
baffle_t = 5.0

# Main tube
body = cq.Workplane("XY").circle(r_out).extrude(L)

# End flanges
f1 = cq.Workplane("XY").circle(flange_r).extrude(flange_t)
f2 = cq.Workplane("XY").workplane(offset=L - flange_t).circle(flange_r).extrude(flange_t)

# Central baffle
b = (cq.Workplane("XY").workplane(offset=L / 2 - baffle_t / 2)
     .circle(baffle_r).extrude(baffle_t))

body = body.union(f1).union(f2).union(b)

# Through bore
bore = cq.Workplane("XY").workplane(offset=-1).circle(r_in).extrude(L + 2)
result = body.cut(bore)
