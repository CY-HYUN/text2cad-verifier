import cadquery as cq
import math

# Right trapezoid in the front (XZ) plane, extruded 40 mm in Y
pts = [(0, 0), (60, 0), (60, 10), (0, 40)]
wedge = (cq.Workplane("XZ").polyline(pts).close().extrude(-40))  # XZ normal is -Y, so negative extrude goes +Y

# Sketch plane on the beveled face
s5 = math.sqrt(5)
origin = (30, 20, 25)
xdir = (2 / s5, 0, -1 / s5)
normal = (1 / s5, 0, 2 / s5)
plane = cq.Plane(origin=origin, xDir=xdir, normal=normal)

# 30x15 rectangle cut 10 mm into the solid, perpendicular to the bevel
slot = cq.Workplane(plane).rect(30, 15).extrude(-10)
body = wedge.cut(slot)

# 8 mm hole at the center of the slot bottom, cut vertically down through everything
cx = 30 - 10 / s5
cy = 20
hole = (cq.Workplane("XY").workplane(offset=-1).center(cx, cy).circle(4).extrude(50))
result = body.cut(hole)
