import cadquery as cq

L = 100.0
r_in = 10.0
r_out = 15.0
flange_r = 25.0
flange_t = 5.0
baffle_r = 20.0
baffle_t = 5.0

# Main tube body (solid, bore cut later)
body = cq.Workplane("XY").circle(r_out).extrude(L).translate((0, 0, -L / 2))

# End flanges
f1 = cq.Workplane("XY").circle(flange_r).extrude(flange_t).translate((0, 0, -L / 2))
f2 = cq.Workplane("XY").circle(flange_r).extrude(flange_t).translate((0, 0, L / 2 - flange_t))

# Central baffle
b = cq.Workplane("XY").circle(baffle_r).extrude(baffle_t).translate((0, 0, -baffle_t / 2))

solid = body.union(f1).union(f2).union(b)

# Through bore
bore = cq.Workplane("XY").circle(r_in).extrude(L + 2).translate((0, 0, -L / 2 - 1))
result = solid.cut(bore)
