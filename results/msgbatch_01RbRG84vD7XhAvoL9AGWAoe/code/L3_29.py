import cadquery as cq
import math

T_END = 10 * math.pi
DECAY = math.pi / 2
W = 8.0      # radial width
TH = 1.2     # axial thickness
N = 1200

def frame(t):
    turns = t / (2 * math.pi)
    R = 40 - 1.5 * turns
    f = min(1.0, t / DECAY, (T_END - t) / DECAY)
    f = max(0.0, f)
    z = 8 * turns + 2.5 * f * math.sin(6 * t)
    return R, z

params = [T_END * i / N for i in range(N + 1)]

def curve_pts(dr, dz):
    pts = []
    for t in params:
        R, z = frame(t)
        r = R + dr
        pts.append(cq.Vector(r * math.cos(t), r * math.sin(t), z + dz))
    return pts

ib = curve_pts(-W / 2, -TH / 2)
ob = curve_pts(W / 2, -TH / 2)
it = curve_pts(-W / 2, TH / 2)
ot = curve_pts(W / 2, TH / 2)

def spl(pts):
    try:
        return cq.Edge.makeSpline(pts, parameters=params)
    except Exception:
        return cq.Edge.makeSpline(pts)

e_ib, e_ob, e_it, e_ot = spl(ib), spl(ob), spl(it), spl(ot)

result = None
try:
    faces = [
        cq.Face.makeRuledSurface(e_ib, e_ob),
        cq.Face.makeRuledSurface(e_it, e_ot),
        cq.Face.makeRuledSurface(e_ib, e_it),
        cq.Face.makeRuledSurface(e_ob, e_ot),
    ]
    for k in (0, -1):
        w = cq.Wire.makePolygon([ib[k], ob[k], ot[k], it[k]], close=True)
        faces.append(cq.Face.makeFromWires(w))
    shell = cq.Shell.makeShell(faces)
    solid = cq.Solid.makeSolid(shell)
    if solid.Volume() < 0:
        solid = cq.Solid(solid.wrapped.Reversed())
    if solid.isValid() and abs(solid.Volume()) > 1.0:
        result = cq.Workplane("XY").add(solid)
except Exception:
    result = None

if result is None:
    # fallback: sweep a rectangular section along the centre path with fixed Z binormal
    cpts = curve_pts(0, 0)
    path = cq.Wire.assembleEdges([spl(cpts)])
    R0, z0 = frame(0)
    t0 = (cpts[1] - cpts[0]).normalized()
    plane = cq.Plane(origin=(R0, 0, z0), xDir=(1, 0, 0), normal=t0.toTuple())
    result = (cq.Workplane(plane).rect(W, TH)
              .sweep(cq.Workplane().add(path), normal=(0, 0, 1)))
