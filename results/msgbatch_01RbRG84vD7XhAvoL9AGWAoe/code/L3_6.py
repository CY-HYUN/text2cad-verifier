import cadquery as cq
import math

R = 20.0
L = 100.0
A = 30.0
rb = 3.0          # ball / groove half-width
depth = 4.0
N = 120

# main shaft, axis along Z, centered at origin
shaft = cq.Workplane("XY").circle(R).extrude(L).translate((0, 0, -L / 2))

def groove_tube(rc):
    pts = []
    for i in range(N):
        phi = 2 * math.pi * i / N
        pts.append(cq.Vector(rc * math.cos(phi), rc * math.sin(phi), A * math.sin(phi)))
    path = cq.Wire.assembleEdges([cq.Edge.makeSpline(pts, periodic=True)])
    p0 = cq.Vector(rc, 0, 0)
    t0 = cq.Vector(0, rc, A).normalized()
    plane = cq.Plane(origin=p0, xDir=(1, 0, 0), normal=t0)
    return cq.Workplane(plane).circle(rb).sweep(cq.Workplane().add(path))

# ball-end cutter centre at bottom: R - depth + rb = 19
rc_bottom = R - depth + rb
result = shaft
for rc in [rc_bottom, rc_bottom + 0.5, R, R + 1.0, R + 2.0]:
    result = result.cut(groove_tube(rc))
