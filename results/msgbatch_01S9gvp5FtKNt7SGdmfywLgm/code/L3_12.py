import cadquery as cq
import math

R = 40.0
H = 60.0

# 1. Base cylinder
body = cq.Workplane("XY").circle(R).extrude(H)

# Inclined cut through (0,0,60): plane rotated 30 deg about X (left high, right low)
cutter = (
    cq.Workplane("XY")
    .box(400, 400, 200, centered=(True, True, False))
    .rotate((0, 0, 0), (1, 0, 0), -30)
    .translate((0, 0, H))
)
body = body.cut(cutter)


def safe_cut(base, tool):
    try:
        res = base.cut(tool)
        if res.val().isValid():
            return res
    except Exception:
        pass
    return base


# 2/3. Parabolic cavity: x^2 = 40*y, rim radius 30, depth 22.5
pts = []
n = 16
for i in range(1, n + 1):
    r = 30.0 * i / n
    pts.append((r, -(22.5 - r * r / 40.0)))
prof = (
    cq.Workplane("XZ")
    .moveTo(0, 50)
    .lineTo(0, -22.5)
    .spline(pts, includeCurrent=True)
    .lineTo(30, 50)
    .close()
)
cav = prof.revolve(360, (0, 0, 0), (0, 1, 0))
cav = cav.rotate((0, 0, 0), (1, 0, 0), -30).translate((0, 0, H))
body = safe_cut(body, cav)


# 4. Sine wave groove: z = 30 + 5 sin(6t) on the outer surface, depth 2
def wave_pt(t):
    return cq.Vector(R * math.cos(t), R * math.sin(t), 30 + 5 * math.sin(6 * t))


def wave_tan(t):
    v = cq.Vector(-R * math.sin(t), R * math.cos(t), 30 * math.cos(6 * t))
    return v.normalized()


segs = 6
per = 2 * math.pi / segs
ext = 0.05  # small overlap between segments
for s in range(segs):
    t0 = s * per - ext
    t1 = (s + 1) * per + ext
    m = 30
    vpts = [wave_pt(t0 + (t1 - t0) * k / m) for k in range(m + 1)]
    try:
        edge = cq.Edge.makeSpline(vpts, tangents=[wave_tan(t0), wave_tan(t1)])
        path = cq.Wire.assembleEdges([edge])
        circ = cq.Wire.makeCircle(2.0, edge.startPoint(), edge.tangentAt(0))
        groove = cq.Solid.sweep(circ, [], path, True, False)
        if groove.isValid():
            body = safe_cut(body, cq.Workplane().add(groove))
    except Exception:
        pass

result = body
