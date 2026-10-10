import cadquery as cq
import math

D = 40.0
R = D / 2.0
L = 100.0
A = 30.0      # sine amplitude (axial)
W = 6.0       # groove width
DEPTH = 4.0

# Base cylinder on the Front plane (axis along Y), symmetric extrusion
base = cq.Workplane("XZ").circle(R).extrude(L / 2.0, both=True)

# 3D sine path wrapped around the cylinder surface (one period per revolution)
N = 72
def pt(r, t, amp=A):
    return cq.Vector(r * math.cos(t), amp * math.sin(t), r * math.sin(t))

pts = [pt(R, 2 * math.pi * i / N) for i in range(N)]
path_edge = cq.Edge.makeSpline(pts, periodic=True)
path = cq.Wire.assembleEdges([path_edge])

# Rectangular profile at path start, perpendicular to tangent
tangent = cq.Vector(0, A, R).normalized()
plane = cq.Plane(origin=(R, 0, 0), xDir=(1, 0, 0), normal=tangent.toTuple())
radial = 2 * DEPTH + 2.0  # extends outside cylinder for clean cut
prof = cq.Workplane(plane).rect(radial, W)

cutter = None
try:
    aux_pts = [pt(R * 0.25, 2 * math.pi * i / N, A * 0.25) for i in range(N)]
    aux = cq.Wire.assembleEdges([cq.Edge.makeSpline(aux_pts, periodic=True)])
    c = prof.sweep(cq.Workplane().add(path), auxSpine=cq.Workplane().add(aux), transition="right")
    if c.val().isValid():
        cutter = c
except Exception:
    cutter = None

if cutter is None:
    try:
        c = prof.sweep(cq.Workplane().add(path), transition="right")
        if c.val().isValid():
            cutter = c
    except Exception:
        cutter = None

if cutter is None:
    c = cq.Workplane(plane).circle(W / 2.0).sweep(cq.Workplane().add(path))
    cutter = c

# Limit cutter to the groove depth: keep only material outside radius R-DEPTH
core = cq.Workplane("XZ").circle(R - DEPTH).extrude(L, both=True)
try:
    cutter_trim = cutter.cut(core)
    result = base.cut(cutter_trim)
except Exception:
    result = base.cut(cutter)
