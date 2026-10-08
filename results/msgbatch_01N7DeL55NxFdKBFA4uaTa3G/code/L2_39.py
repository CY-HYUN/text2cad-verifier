import cadquery as cq
import math

# Wedge: right trapezoid in XZ (front) plane, extruded 40 mm in Y (centered)
pts = [(0, 0), (60, 0), (60, 10), (0, 40)]
wedge = cq.Workplane("XZ").polyline(pts).close().extrude(20, both=True)

# Beveled face geometry
s5 = math.sqrt(5)
n = cq.Vector(1 / s5, 0, 2 / s5)          # outward normal of slanted face
xdir = cq.Vector(2 / s5, 0, -1 / s5)      # direction along the slope
center = cq.Vector(30, 0, 25)             # center of slanted face

# Slot: 30 (along slope) x 15 (across width), 10 mm deep perpendicular to face
plane = cq.Plane(origin=center, xDir=xdir, normal=n)
slot = cq.Workplane(plane).rect(30, 15).extrude(-10)
body = wedge.cut(slot)

# Hole: 8 mm diameter at center of slot bottom, cut vertically through
bottom_c = center - n * 10
hole = (
    cq.Workplane("XY")
    .workplane(offset=-1)
    .center(bottom_c.x, bottom_c.y)
    .circle(4)
    .extrude(60)
)
result = body.cut(hole)
