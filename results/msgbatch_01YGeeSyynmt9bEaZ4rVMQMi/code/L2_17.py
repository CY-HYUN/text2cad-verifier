import cadquery as cq

H = 50.0
R_out_o, R_out_i = 50.0, 45.0   # outer tube
R_in_o, R_in_i = 20.0, 15.0     # inner tube
rib_w = 5.0

outer = cq.Workplane("XY").circle(R_out_o).circle(R_out_i).extrude(H)
inner = cq.Workplane("XY").circle(R_in_o).circle(R_in_i).extrude(H)

# ribs overlap into both tubes so the union merges into one section
r0, r1 = R_in_o - 2.0, R_out_i + 2.0
L = r1 - r0
xc = (r0 + r1) / 2.0

result = outer.union(inner)
for ang in (0, 90, 180, 270):
    rib = (cq.Workplane("XY")
           .center(xc, 0)
           .rect(L, rib_w)
           .extrude(H)
           .rotate((0, 0, 0), (0, 0, 1), ang))
    result = result.union(rib)

result = result.clean()
