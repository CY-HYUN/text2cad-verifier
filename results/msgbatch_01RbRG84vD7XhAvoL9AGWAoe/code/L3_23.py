import cadquery as cq
import math

L, W, H = 200.0, 100.0, 80.0

# Base block (centered at origin, z from -40 to 40)
body = cq.Workplane("XY").box(L, W, H)

# Countersunk mounting holes at the four corners
bolt_pts = [(sx * 88, sy * 38) for sx in (-1, 1) for sy in (-1, 1)]
body = body.faces(">Z").workplane().pushPoints(bolt_pts).cskHole(9.0, 18.0, 90)

solid = body.val()

# Internal channel network
z_ch = -15.0
row_y = [-25.0, 25.0]
out_x = [-72.0, -36.0, 0.0, 36.0, 72.0]
inlet_x = [-60.0, 0.0, 60.0]

cuts = []
# Two horizontal main galleries along X
for y in row_y:
    cuts.append(cq.Solid.makeCylinder(7.0, 160.0, cq.Vector(-80, y, z_ch), cq.Vector(1, 0, 0)))
# Cross-connecting distribution channel at y=0
cuts.append(cq.Solid.makeCylinder(6.0, 140.0, cq.Vector(-70, 0, z_ch), cq.Vector(1, 0, 0)))

# Inlets from front face (y = -50), d20, extending to rear gallery
for x in inlet_x:
    cuts.append(cq.Solid.makeCylinder(10.0, 78.0, cq.Vector(x, -W / 2 - 1, z_ch), cq.Vector(0, 1, 0)))

# Outlets from top face, d10, down into galleries
for y in row_y:
    for x in out_x:
        cuts.append(cq.Solid.makeCylinder(5.0, H / 2 - z_ch + 1, cq.Vector(x, y, H / 2 + 1), cq.Vector(0, 0, -1)))

for c in cuts:
    solid = solid.cut(c)

result = cq.Workplane("XY").add(solid)

# Weight-reduction grooves: 2 on bottom
bottom_pl = cq.Plane(origin=(0, 0, -H / 2), xDir=(1, 0, 0), normal=(0, 0, 1))
for x in (-30.0, 30.0):
    g = cq.Workplane(bottom_pl).center(x, 0).slot2D(30, 16, angle=90).extrude(12)
    result = result.cut(g)

# 2 on back side face (y = +50)
back_pl = cq.Plane(origin=(0, W / 2, 0), xDir=(1, 0, 0), normal=(0, -1, 0))
for x in (-50.0, 50.0):
    g = cq.Workplane(back_pl).center(x, 12).slot2D(50, 20, angle=0).extrude(14)
    result = result.cut(g)
