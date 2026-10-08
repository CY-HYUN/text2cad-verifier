import cadquery as cq
import math

# Wedge profile in XZ plane: front height 10 at x=0, rear height 40 at x=60
pts = [(0, 0), (60, 0), (60, 40), (0, 10)]
base = (
    cq.Workplane("XZ")
    .polyline(pts).close()
    .extrude(-40)  # extrude along +Y
)

# Local plane on the beveled face, centered on it
nx, nz = -30.0, 60.0
xd = (60.0, 0.0, 30.0)
plane = cq.Plane(origin=(30, 20, 25), xDir=xd, normal=(nx, 0, nz))

# Rectangular blind slot 30 x 15 x 10 deep, perpendicular to bevel
slot = cq.Workplane(plane).rect(30, 15).extrude(-10)

# Through hole dia 8 at slot bottom center, perpendicular to bevel
hole = (
    cq.Workplane(plane)
    .workplane(offset=20)
    .circle(4)
    .extrude(-150)
)

result = base.cut(slot).cut(hole)
