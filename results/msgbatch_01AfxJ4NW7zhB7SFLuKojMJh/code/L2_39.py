import cadquery as cq
import math

# Wedge: profile in XZ, extruded along Y (40 mm)
wedge = (cq.Workplane("XZ")
         .polyline([(0, 0), (60, 0), (60, 10), (0, 40)]).close()
         .extrude(40))
wedge = wedge.translate((0, 20, 0))  # center on Y

s5 = math.sqrt(5)
xdir = (2 / s5, 0, -1 / s5)
nrm = (1 / s5, 0, 2 / s5)
center = (30, 0, 25)

# Rectangular blind slot, 30 x 15 x 10 deep, perpendicular to slope
plane = cq.Plane(origin=center, xDir=xdir, normal=nrm)
slot = cq.Workplane(plane).rect(30, 15).extrude(-10)
body = wedge.cut(slot)

# Through hole dia 8 from slot bottom, perpendicular to slope
bottom_origin = (center[0] - 10 * nrm[0], 0, center[2] - 10 * nrm[2])
plane2 = cq.Plane(origin=bottom_origin, xDir=xdir, normal=nrm)
hole = cq.Workplane(plane2).circle(4).extrude(-60)
result = body.cut(hole)
