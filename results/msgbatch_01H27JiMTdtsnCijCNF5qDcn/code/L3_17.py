import cadquery as cq
import math

R = 25.0
H = 100.0
depth = 5.0
half_w = 4.0
amp = 15.0
zc = 50.0

base = cq.Workplane("XY").circle(R).extrude(H)

r_in = R - depth
r_out = R + 1.0

def section(theta):
    # sine in unrolled coordinates: s = R*theta, k = 2*pi/(2*pi*R) -> one period per turn
    z = zc + amp * math.sin(theta)
    c, s = math.cos(theta), math.sin(theta)
    pts = [
        cq.Vector(r_in * c, r_in * s, z - half_w),
        cq.Vector(r_out * c, r_out * s, z - half_w),
        cq.Vector(r_out * c, r_out * s, z + half_w),
        cq.Vector(r_in * c, r_in * s, z + half_w),
    ]
    return cq.Wire.makePolygon(pts, close=True)

result = base
n_quarters = 4
steps = 12
for q in range(n_quarters):
    wires = []
    for j in range(steps + 1):
        th = (q * steps + j) * (2 * math.pi) / (n_quarters * steps)
        wires.append(section(th))
    groove = cq.Solid.makeLoft(wires, False)
    result = result.cut(cq.Workplane("XY").add(groove))
