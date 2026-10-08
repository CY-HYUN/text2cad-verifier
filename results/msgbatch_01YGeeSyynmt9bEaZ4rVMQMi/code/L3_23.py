import cadquery as cq
import math

L, W, H = 200.0, 100.0, 80.0
zc = H / 2.0

# Base block
body = cq.Workplane("XY").rect(L, W).extrude(H)

# Internal longitudinal oil passages (drilled from +X end)
main_pass = cq.Solid.makeCylinder(10.0, 185.0, cq.Vector(L/2, 0, zc), cq.Vector(-1, 0, 0))
branch1 = cq.Solid.makeCylinder(6.0, 185.0, cq.Vector(L/2, -20, zc), cq.Vector(-1, 0, 0))
branch2 = cq.Solid.makeCylinder(6.0, 185.0, cq.Vector(L/2, 20, zc), cq.Vector(-1, 0, 0))
body = body.cut(cq.Workplane().add(main_pass)).cut(cq.Workplane().add(branch1)).cut(cq.Workplane().add(branch2))

# Front oil inlets (from front face y=-50), deep enough to cross all passages
for x in (-60.0, 0.0, 60.0):
    c = cq.Solid.makeCylinder(10.0, 72.0, cq.Vector(x, -W/2, zc), cq.Vector(0, 1, 0))
    body = body.cut(cq.Workplane().add(c))

# Top distribution holes: two rows of five, down to the passages
for y in (-20.0, 20.0):
    for x in (-72.0, -36.0, 0.0, 36.0, 72.0):
        c = cq.Solid.makeCylinder(5.0, H - zc + 2.0, cq.Vector(x, y, zc - 2.0), cq.Vector(0, 0, 1))
        body = body.cut(cq.Workplane().add(c))

# Countersunk corner bolt holes
corners = [(85, 40), (-85, 40), (85, -40), (-85, -40)]
body = (body.faces(">Z").workplane(origin=(0, 0, H))
        .pushPoints(corners).cskHole(9.0, 18.0, 90.0))

# Lightening pockets on the bottom (two oval slots)
bottom_pockets = (cq.Workplane("XY")
                  .pushPoints([(-40, 0), (40, 0)])
                  .slot2D(50.0, 40.0)
                  .extrude(25.0))
body = body.cut(bottom_pockets)

# Lightening pockets on the back side face (two oval slots)
back_pockets = (cq.Workplane("XZ", origin=(0, W/2, 0))
                .pushPoints([(-40, zc), (40, zc)])
                .slot2D(50.0, 30.0)
                .extrude(15.0))  # XZ normal is -Y, so extrudes into the block
body = body.cut(back_pockets)

result = body
