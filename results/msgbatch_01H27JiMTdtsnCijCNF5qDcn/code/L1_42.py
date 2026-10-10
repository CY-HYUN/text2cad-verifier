import cadquery as cq
import math

# Cylinder: diameter 30, height 50
cyl = cq.Workplane("XY").circle(15.0).extrude(50.0)

# Inclined plane through (-15, 0, 50), tilted 30° about the Y axis (descending along +X)
t = math.tan(math.radians(30.0))
def z_at(x):
    return 50.0 - (x + 15.0) * t

# Cutter: region above the plane, drawn in XZ and extruded symmetrically along Y
pts = [(-20.0, z_at(-20.0)), (20.0, z_at(20.0)), (20.0, 70.0), (-20.0, 70.0)]
cutter = cq.Workplane("XZ").polyline(pts).close().extrude(25.0, both=True)

result = cyl.cut(cutter)
