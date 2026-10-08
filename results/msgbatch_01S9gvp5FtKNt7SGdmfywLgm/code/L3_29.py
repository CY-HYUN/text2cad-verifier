import cadquery as cq
import math

# ---------------- parameters ----------------
N_TURNS = 5
R0, R1 = 40.0, 32.5          # bottom / top radius
PITCH = 8.0                   # rise per turn
AMP = 2.5                     # wave amplitude
WAVES_PER_TURN = 6
W, TH = 8.0, 1.2              # strip width (radial) / thickness (axial)
DECAY = 0.25                  # decay zone (turns) at each end

def smooth(x):
    x = max(0.0, min(1.0, x))
    return 3 * x * x - 2 * x ** 3

def envelope(u):
    return smooth(u / DECAY) * smooth((N_TURNS - u) / DECAY)

n = N_TURNS * WAVES_PER_TURN * 12
us = [N_TURNS * i / n for i in range(n + 1)]

# corner offsets: (radial, vertical)
offs = [(-W / 2, -TH / 2), (W / 2, -TH / 2), (W / 2, TH / 2), (-W / 2, TH / 2)]
corner_pts = [[] for _ in offs]

for u in us:
    th = 2 * math.pi * u
    r = R0 + (R1 - R0) * u / N_TURNS
    z = PITCH * u + AMP * envelope(u) * math.sin(WAVES_PER_TURN * th)
    c, s = math.cos(th), math.sin(th)
    for k, (dr, dz) in enumerate(offs):
        rr = r + dr
        corner_pts[k].append(cq.Vector(rr * c, rr * s, z + dz))

curves = [cq.Edge.makeSpline(p) for p in corner_pts]

faces = []
for k in range(4):
    faces.append(cq.Face.makeRuledSurface(curves[k], curves[(k + 1) % 4]))

start_wire = cq.Wire.makePolygon([corner_pts[k][0] for k in range(4)], close=True)
end_wire = cq.Wire.makePolygon([corner_pts[k][-1] for k in range(4)], close=True)
faces.append(cq.Face.makeFromWires(start_wire))
faces.append(cq.Face.makeFromWires(end_wire))

shell = cq.Shell.makeShell(faces)
solid = cq.Solid.makeSolid(shell)
result = cq.Workplane("XY").add(solid)
