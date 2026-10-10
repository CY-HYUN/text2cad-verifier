import cadquery as cq
import math

L, W, H = 200.0, 100.0, 80.0

# base block centered in XY, z from 0 to 80
body = cq.Workplane("XY").box(L, W, H, centered=(True, True, False))

# main horizontal channel along X at y=0, z=40
main = (cq.Workplane("YZ").workplane(offset=-L/2 + 10)
        .center(0, 40).circle(8).extrude(L - 20))
body = body.cut(main)

# 3 front inlets (dia 20) from front face y=-50 to y=0
for x in (-60, 0, 60):
    inlet = (cq.Workplane("XZ").workplane(offset=W/2 - 0)  # XZ normal is -Y; offset moves to y=-50
             .center(x, 40).circle(10).extrude(-50))
    # ensure direction: build explicitly by solid cylinder
    cyl = cq.Workplane("XY").add(
        cq.Solid.makeCylinder(10, 50, cq.Vector(x, -50, 40), cq.Vector(0, 1, 0)))
    body = body.cut(cyl)

# 10 top outlets (dia 10): two rows of 5, drilled down to the main channel
for y in (-8, 8):
    for x in (-60, -30, 0, 30, 60):
        cyl = cq.Solid.makeCylinder(5, 40, cq.Vector(x, y, 40), cq.Vector(0, 0, 1))
        body = body.cut(cq.Workplane("XY").add(cyl))

# 4 corner countersunk (counterbored) mounting holes
for sx in (-1, 1):
    for sy in (-1, 1):
        x, y = sx * 90, sy * 40
        thru = cq.Solid.makeCylinder(5, H, cq.Vector(x, y, 0), cq.Vector(0, 0, 1))
        cone = cq.Solid.makeCone(5, 10, 5, cq.Vector(x, y, H - 5), cq.Vector(0, 0, 1))
        body = body.cut(cq.Workplane("XY").add(thru)).cut(cq.Workplane("XY").add(cone))

# 4 oval weight-reduction grooves from the bottom
for sx in (-1, 1):
    for sy in (-1, 1):
        groove = (cq.Workplane("XY").center(sx * 55, sy * 30)
                  .slot2D(40, 16, 0).extrude(25))
        body = body.cut(groove)

result = body
