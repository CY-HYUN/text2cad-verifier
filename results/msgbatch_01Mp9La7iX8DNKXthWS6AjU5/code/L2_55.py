import cadquery as cq
import math

R = 50.0
d_start = 30.0
d_end = 15.0
n = 9  # number of sections along the arc path (in the XZ / front plane)

wires = []
for i in range(n):
    f = i / (n - 1)
    t = math.radians(90.0 * f)
    # point on arc path (front plane = XZ), centre at origin
    origin = (R * math.cos(t), 0, R * math.sin(t))
    # tangent of path -> section plane normal
    normal = (-math.sin(t), 0, math.cos(t))
    plane = cq.Plane(origin=origin, xDir=(0, 1, 0), normal=normal)
    d = d_start + (d_end - d_start) * f
    w = cq.Workplane(plane).circle(d / 2.0).val()
    wires.append(w)

solid = cq.Solid.makeLoft(wires, False)
result = cq.Workplane("XY").add(solid)
