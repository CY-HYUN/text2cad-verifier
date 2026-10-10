import cadquery as cq
import math

# Wedge: 60 long (X), 40 wide (Y), rear height 40, front height 10
wedge = (cq.Workplane("XZ")
         .polyline([(0, 0), (60, 0), (60, 10), (0, 40)]).close()
         .extrude(-40))

# Plane on the beveled surface at its center
s5 = math.sqrt(5)
origin = (30, 20, 25)
xdir = (2 / s5, 0, -1 / s5)
normal = (1 / s5, 0, 2 / s5)
pl = cq.Plane(origin=origin, xDir=xdir, normal=normal)

# Blind slot 30 x 15 x 10 deep, perpendicular to the bevel
slot = cq.Workplane(pl).workplane(offset=1).rect(30, 15).extrude(-11)

# Through hole dia 8, perpendicular to bevel, through to the base
hole = cq.Workplane(pl).circle(4).extrude(-100)

result = wedge.cut(slot).cut(hole)
