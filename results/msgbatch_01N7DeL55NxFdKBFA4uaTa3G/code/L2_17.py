import cadquery as cq
import math

H = 50.0
R_out_o, R_out_i = 50.0, 45.0   # outer tube
R_in_o, R_in_i = 25.0, 20.0     # inner tube
rib_w = 5.0

# Annular rings
outer = cq.Workplane("XY").circle(R_out_o).circle(R_out_i).extrude(H)
inner = cq.Workplane("XY").circle(R_in_o).circle(R_in_i).extrude(H)

# Stiffeners: overlap slightly into both tubes (not into bores)
r0, r1 = R_in_o - 2.0, R_out_i + 2.0
rib_len = r1 - r0
rc = (r0 + r1) / 2.0

result = outer.union(inner)
for k in range(4):
    a = k * 90.0
    x = rc * math.cos(math.radians(a))
    y = rc * math.sin(math.radians(a))
    rib = (
        cq.Workplane("XY")
        .center(x, y)
        .transformed(rotate=(0, 0, a))
        .rect(rib_len, rib_w)
        .extrude(H)
    )
    result = result.union(rib)

result = result.clean()
