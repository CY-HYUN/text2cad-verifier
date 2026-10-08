import cadquery as cq
import math

# Right trapezoid in the XZ (front) plane: base 60, rear side 40, front side 10
wedge = (
    cq.Workplane("XZ")
    .polyline([(0, 0), (60, 0), (60, 10), (0, 40)])
    .close()
    .extrude(-40)  # extrude toward +Y, width 40
)

# Bevel geometry
ang = math.degrees(math.atan2(30, 60))       # slope angle
n = cq.Vector(1, 0, 2).normalized()          # outward normal of beveled face
center = cq.Vector(30, 20, 25)               # center of beveled face

# 30 (along slope) x 15 (along width) rectangle, cut 10 deep normal to the bevel
slot = (
    cq.Workplane("XY")
    .box(30, 15, 20)  # z from -10..10: lower half is the cut depth
    .rotate((0, 0, 0), (0, 1, 0), ang)
    .translate(center)
)
body = wedge.cut(slot)

# Center of the slot bottom
bc = center - n * 10

# 8 mm hole vertically through the entire solid
hole = (
    cq.Workplane("XY")
    .workplane(offset=-1)
    .center(bc.x, bc.y)
    .circle(4)
    .extrude(60)
)
result = body.cut(hole)
