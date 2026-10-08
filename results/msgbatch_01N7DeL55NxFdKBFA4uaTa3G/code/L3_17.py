import cadquery as cq
import math

D = 50.0
R = D / 2.0
H = 100.0
amp = 15.0
mid = 50.0
half_w = 4.0
depth = 5.0
circ = math.pi * D
k = 2 * math.pi / circ  # one full sine period around the circumference

base = cq.Workplane("XY").circle(R).extrude(H)

r_in = R - depth
r_out = R + 1.0  # overshoot for a clean cut
N = 144

def zc(t):
    X = R * t  # unrolled arc length
    return amp * math.sin(k * X) + mid

def pt(r, t, z):
    return cq.Vector(r * math.cos(t), r * math.sin(t), z)

groove = None
try:
    ts = [2 * math.pi * i / N for i in range(N)]
    def curve(r, dz):
        return cq.Edge.makeSpline([pt(r, t, zc(t) + dz) for t in ts], periodic=True)
    to = curve(r_out, half_w)
    bo = curve(r_out, -half_w)
    ti = curve(r_in, half_w)
    bi = curve(r_in, -half_w)
    faces = [
        cq.Face.makeRuledSurface(to, bo),
        cq.Face.makeRuledSurface(bo, bi),
        cq.Face.makeRuledSurface(bi, ti),
        cq.Face.makeRuledSurface(ti, to),
    ]
    sh = cq.Shell.makeShell(faces)
    sol = cq.Solid.makeSolid(sh).fix()
    if not sol.isValid() or sol.Volume() <= 0:
        raise ValueError
    groove = sol
    result = base.cut(cq.Workplane().add(groove))
    if result.val().Volume() >= base.val().Volume() - 1.0:
        raise ValueError
except Exception:
    # fallback: segmented ruled lofts
    def section(t):
        z = zc(t)
        pts = [pt(r_in, t, z - half_w), pt(r_out, t, z - half_w),
               pt(r_out, t, z + half_w), pt(r_in, t, z + half_w)]
        return cq.Wire.makePolygon(pts, close=True)
    secs = [section(2 * math.pi * i / N) for i in range(N + 1)]
    segs = [cq.Solid.makeLoft([secs[i], secs[i + 1]], True) for i in range(N)]
    result = base
    for s in segs:
        result = result.cut(cq.Workplane().add(s))
