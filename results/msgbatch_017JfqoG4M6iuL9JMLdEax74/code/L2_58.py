import cadquery as cq

L, W, H = 80.0, 40.0, 40.0
d = 10.0
r = d / 2

body = cq.Workplane("XY").box(L, W, H)

# Horizontal segment from left face center, 40 mm deep (to x=0)
h_cyl = cq.Solid.makeCylinder(r, 40.0, cq.Vector(-L / 2, 0, 0), cq.Vector(1, 0, 0))
# Vertical segment from top face center, 20 mm deep (to z=0)
v_cyl = cq.Solid.makeCylinder(r, 20.0, cq.Vector(0, 0, H / 2), cq.Vector(0, 0, -1))
# Small sphere at the bend to make a clean junction
joint = cq.Solid.makeSphere(r, cq.Vector(0, 0, 0))

result = body.cut(cq.Workplane().add(h_cyl)).cut(cq.Workplane().add(v_cyl)).cut(cq.Workplane().add(joint))
