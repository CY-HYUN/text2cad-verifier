import cadquery as cq
import math

D = 30.0
R = D / 2.0
L = 60.0
depth = 1.0
pitch = 2.0

# grooves around the circumference (circumferential pitch ~2 mm)
N = int(round(math.pi * D / pitch))   # 47
M = 2 * N                              # grid points around (half-pitch steps)

# axial half-pitch step chosen so it divides the length evenly (~45 deg helix)
nz = int(round(L / (pitch / 2.0)))     # 60
dz = L / nz

# Height map of crossed V-grooves: on a half-pitch grid, points with odd
# (i+j) are pyramid apexes (full radius), even ones are groove crossings.
wires = []
for j in range(nz + 1):
    z = j * dz
    pts = []
    for i in range(M):
        a = 2 * math.pi * i / M
        r = R if (i + j) % 2 == 1 else R - depth
        pts.append(cq.Vector(r * math.cos(a), r * math.sin(a), z))
    wires.append(cq.Wire.makePolygon(pts, close=True))

solid = cq.Solid.makeLoft(wires, True)

result = cq.Workplane("XY").add(solid)
