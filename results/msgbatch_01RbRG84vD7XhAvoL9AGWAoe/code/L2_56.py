import cadquery as cq

R_out = 20.0
wall = 2.0
R_in = R_out - wall
L = 100.0

# Outer solid: two orthogonal cylinders fused (along X and Y), centered at origin
cyl_x = cq.Workplane("YZ").circle(R_out).extrude(L / 2, both=True)
cyl_y = cq.Workplane("XZ").circle(R_out).extrude(L / 2, both=True)
outer = cyl_x.union(cyl_y)

# Inner cavity: cross-shaped union of bores, slightly longer to open all four ends
ext = L / 2 + 1.0
bore_x = cq.Workplane("YZ").circle(R_in).extrude(ext, both=True)
bore_y = cq.Workplane("XZ").circle(R_in).extrude(ext, both=True)
cavity = bore_x.union(bore_y)

# Shell result: uniform 2mm wall, fully connected internal cross cavity
result = outer.cut(cavity)
