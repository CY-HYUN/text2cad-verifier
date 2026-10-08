import cadquery as cq
import math

# ---------------- parameters ----------------
N_TURNS = 5
R0, R1 = 40.0, 32.5          # bottom / top radius
PITCH = 8.0                   # rise per turn
AMP = 2.5                     # wave amplitude
WAVES_PER_TURN = 6
W, TH = 8.0, 1.2              # strip width / thickness
DECAY = 0.25                  # decay zone (turns) at each end

def smooth(x):
    x = max(0.0, min(1.0, x))
    return 3 * x * x - 2 * x ** 3

def envelope(u):
    # u in turns [0, N_TURNS]
    return smooth(u / DECAY) * smooth((N_TURNS - u) / DECAY)

# ---------------- sample guide curve ----------------
n = N_TURNS * WAVES_PER_TURN * 16
us = [N_TURNS * i / n for i in range(n + 1)]

# rise with decaying slope (integrated numerically) -> flat ends
rise = [0.0]
for i in range(1, n + 1):
    du = us[i] - us[i - 1]
    rise.append(rise[-1] + PITCH * 0.5 * (envelope(us[i]) + envelope(us[i - 1])) * du)

pts = []
for i, u in enumerate(us):
    th = 2 * math.pi * u
    r = R0 + (R1 - R0) * u / N_TURNS
    z = rise[i] + AMP * envelope(u) * math.sin(WAVES_PER_TURN * th)
    pts.append(cq.Vector(r * math.cos(th), r * math.sin(th), z))

edge = cq.Edge.makeSpline(pts)
path = cq.Wire.assembleEdges([edge])

# ---------------- cross-section at path start ----------------
p0 = pts[0]
t0 = edge.tangentAt(0).normalized()
rad = cq.Vector(1, 0, 0)
xdir = (rad - t0 * rad.dot(t0)).normalized()   # long side horizontal / radial
plane = cq.Plane(origin=p0, xDir=xdir, normal=t0)
section = cq.Workplane(plane).rect(W, TH).wires().val()

# ---------------- sweep with fixed vertical binormal ----------------
try:
    solid = cq.Solid.sweep(section, [], path, makeSolid=True,
                           isFrenet=False, mode=cq.Vector(0, 0, 1))
    result = cq.Workplane("XY").add(solid)
except Exception:
    result = (cq.Workplane(plane).rect(W, TH)
              .sweep(cq.Workplane().add(path), isFrenet=True))
