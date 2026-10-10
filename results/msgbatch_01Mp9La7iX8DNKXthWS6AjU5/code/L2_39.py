import cadquery as cq
import math

# Wedge: trapezoid in the XZ (front) plane, extruded 40 mm in Y
pts = [(0, 0), (60, 0), (60, 10), (0, 40)]
wedge = cq.Workplane("XZ").polyline(pts).close().extrude(-40)  # XZ normal is -Y, so negative gives +Y

# Beveled face reference
s5 = math.sqrt(5)
xdir = (2 / s5, 0, -1 / s5)   # along slope
nrm = (1 / s5, 0, 2 / s5)     # outward normal of bevel
center = (30, 20, 25)

plane = cq.Plane(origin=center, xDir=xdir, normal=nrm)
slot = cq.Workplane(plane).rect(30, 15).extrude(-10)
body = wedge.cut(slot)

# Hole at center of slot bottom, vertical through
bx = center[0] - 10 * nrm[0]
by = center[1]
hole = (cq.Workplane("XY").workplane(offset=-1).center(bx, by)
        .circle(4).extrude(60))
result = body.cut(hole)
