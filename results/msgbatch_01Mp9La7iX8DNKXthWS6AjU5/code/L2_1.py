import cadquery as cq
import math

# Base cube 50x50x50 centered at origin (extruded 25 both directions in Z)
base = cq.Workplane("XY").rect(50, 50).extrude(25, both=True)

L = 200  # long enough for a through cut
r = 30   # 60 mm diameter
off = 35 # circle centers offset so the arc cuts into the solid

# Front view (XZ plane) circles, cut along Y (perpendicular to the plane), left and right sides
for sx in (-1, 1):
    cyl = (cq.Workplane("XY")
           .add(cq.Solid.makeCylinder(r, L, cq.Vector(sx * off, -L / 2, 0), cq.Vector(0, 1, 0))))
    base = base.cut(cyl)

# Right view (YZ plane) circles, cut along X (perpendicular to the plane), front and back sides
for sy in (-1, 1):
    cyl = (cq.Workplane("XY")
           .add(cq.Solid.makeCylinder(r, L, cq.Vector(-L / 2, sy * off, 0), cq.Vector(1, 0, 0))))
    base = base.cut(cyl)

result = base
