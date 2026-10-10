import cadquery as cq
import math

# Wedge profile in XZ, extruded 40 mm along +Y
wedge = (
    cq.Workplane("XZ")
    .polyline([(0, 0), (60, 0), (60, 40), (0, 10)])
    .close()
    .extrude(-40)
)

# Plane on the sloped face, centred on it
n = math.sqrt(5)
slope_plane = cq.Plane(
    origin=(30, 20, 25),
    xDir=(2 / n, 0, 1 / n),
    normal=(-1 / n, 0, 2 / n),
)

# Rectangular blind slot 30 x 15 x 10 deep
slot = cq.Workplane(slope_plane).rect(30, 15).extrude(-10)

# 8 mm through-hole perpendicular to the slope, through the slot centre
hole = cq.Workplane(slope_plane).circle(4).extrude(100, both=True)

result = wedge.cut(slot).cut(hole)
