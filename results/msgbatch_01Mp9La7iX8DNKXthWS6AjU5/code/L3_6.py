import cadquery as cq
import math

R = 20.0
H = 100.0
amp = 30.0
width = 6.0

# base cylinder, symmetric about the sketch plane (built along Z, rotated at the end)
cyl = cq.Workplane("XY").circle(R).extrude(H / 2.0, both=True)

# 3D sine path wrapped on the cylinder: z = amp*sin(theta), one full period
N = 72
pts = []
for i in range(N + 1):
    t = 2 * math.pi * i / N
    pts.append((R * math.cos(t), R * math.sin(t), amp * math.sin(t)))

tan0 = cq.Vector(0, R, amp)  # tangent at theta=0 (dz/dt = amp*cos(0))
path = cq.Workplane("XY").spline(pts, tangents=[tuple(tan0.toTuple()), tuple(tan0.toTuple())])

# rectangular profile perpendicular to the path at its start
# radial span 16..22 (4 mm deep below surface, extending outside), width 6
plane = cq.Plane(origin=(19, 0, 0), xDir=(1, 0, 0), normal=tan0.normalized().toTuple())
groove = cq.Workplane(plane).rect(6.0, width).sweep(path, isFrenet=False, transition="round")

cam = cyl.cut(groove)

# put the cylinder axis along the Front plane normal (Y)
result = cam.rotate((0, 0, 0), (1, 0, 0), -90)
