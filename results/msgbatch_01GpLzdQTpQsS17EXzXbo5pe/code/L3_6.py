import cadquery as cq
import math

R = 20.0
H = 100.0
amp = 30.0
width = 6.0
depth = 4.0

# base cylinder, symmetric about the sketch plane (built along Z, rotated at the end)
cyl = cq.Workplane("XY").circle(R).extrude(H / 2.0, both=True)

# 3D sine path wrapped on the cylinder: z = amp*sin(theta), one full period
N = 60
def P(i):
    t = 2 * math.pi * i / N
    return cq.Vector(R * math.cos(t), R * math.sin(t), amp * math.sin(t))

cam = cyl
for i in range(N):
    p0 = P(i)
    p1 = P(i + 1)
    d = p1 - p0
    L = d.Length
    dn = d.normalized()
    mid = (p0 + p1) * 0.5
    rad = cq.Vector(mid.x, mid.y, 0).normalized()
    # profile x-axis: radial direction made perpendicular to the segment
    x = (rad - dn * rad.dot(dn)).normalized()
    # shift profile center so the groove spans (R-depth) .. (R+extra) radially
    radial_extent = depth + 2.0
    center_r = (R - depth) + radial_extent / 2.0
    center = cq.Vector(mid.x, mid.y, mid.z) + rad * (center_r - R)
    plane = cq.Plane(origin=center.toTuple(), xDir=x.toTuple(), normal=dn.toTuple())
    seg = (cq.Workplane(plane)
           .rect(radial_extent, width)
           .extrude(L / 2.0 * 1.2, both=True))
    cam = cam.cut(seg)

# put the cylinder axis along the Front plane normal (Y)
result = cam.rotate((0, 0, 0), (1, 0, 0), -90)
