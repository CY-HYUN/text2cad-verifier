import cadquery as cq
import math

# Three 50x50x5 plates meeting at the origin corner
pxy = cq.Workplane("XY").box(50, 50, 5, centered=False)
pxz = cq.Workplane("XY").box(50, 5, 50, centered=False)
pyz = cq.Workplane("XY").box(5, 50, 50, centered=False)
body = pxy.union(pxz).union(pyz)

# 15 mm holes at the center of each plate
def cyl(center, direction):
    return cq.Workplane("XY").add(
        cq.Solid.makeCylinder(7.5, 5, cq.Vector(*center), cq.Vector(*direction))
    )

body = body.cut(cyl((25, 25, 0), (0, 0, 1)))   # XY plate
body = body.cut(cyl((25, 0, 25), (0, 1, 0)))   # XZ plate
body = body.cut(cyl((0, 25, 25), (1, 0, 0)))   # YZ plate

tri = [(5, 5), (25, 5), (5, 25)]

# Rib along X-edge (between XY and XZ plates), centered at x=25
rib_x = cq.Workplane("YZ", origin=(22.5, 0, 0)).polyline(tri).close().extrude(5)
# Rib along Y-edge (between XY and YZ plates), centered at y=25
rib_y = cq.Workplane("XZ", origin=(0, 27.5, 0)).polyline(tri).close().extrude(5)
# Rib along Z-edge (between XZ and YZ plates), centered at z=25
rib_z = cq.Workplane("XY", origin=(0, 0, 22.5)).polyline(tri).close().extrude(5)

result = body.union(rib_x).union(rib_y).union(rib_z)
