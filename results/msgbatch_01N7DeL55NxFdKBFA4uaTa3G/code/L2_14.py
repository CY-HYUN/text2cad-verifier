import cadquery as cq

L = 60.0
S = 40.0

result = cq.Workplane("XY").box(L, L, L)

# Through cuts along X, Y, Z with 40x40 square
cut_z = cq.Workplane("XY").box(S, S, L * 2)
cut_y = cq.Workplane("XY").box(S, L * 2, S)
cut_x = cq.Workplane("XY").box(L * 2, S, S)

result = result.cut(cut_z).cut(cut_y).cut(cut_x)
