import cadquery as cq
import math

D = 30.0
R = D / 2.0
L = 60.0
depth = 1.0
pitch = 2.0
helix_angle = 45.0

# number of grooves around circumference (pitch measured circumferentially)
N = int(round(math.pi * D / pitch))  # ~47

# twist angle over the length for a 45 deg helix
lead = math.pi * D / math.tan(math.radians(helix_angle))
twist = L / lead * 360.0

# V-tooth star profile
pts = []
for i in range(N):
    a0 = 2 * math.pi * i / N
    a1 = 2 * math.pi * (i + 0.5) / N
    pts.append((R * math.cos(a0), R * math.sin(a0)))
    pts.append(((R - depth) * math.cos(a1), (R - depth) * math.sin(a1)))

right = cq.Workplane("XY").polyline(pts).close().twistExtrude(L, twist)
left = cq.Workplane("XY").polyline(pts).close().twistExtrude(L, -twist)

result = right.intersect(left)
