import cadquery as cq
import math

# ---------------- parameters ----------------
turns = 5.0
r0, r1 = 40.0, 32.5          # bottom / top radius
pitch = 8.0                  # uniform rise per turn
waves_per_turn = 6
amp = 2.5                    # sine amplitude
ramp = 0.25                  # decay zone length (turns) at each end
width, thick = 8.0, 1.2      # rectangular section

def smooth(x):
    x = max(0.0, min(1.0, x))
    return 3 * x * x - 2 * x ** 3

def env(u):
    if u < ramp:
        return smooth(u / ramp)
    if u > turns - ramp:
        return smooth((turns - u) / ramp)
    return 1.0

# ---------------- path points ----------------
n = 900
fine = 20  # sub-steps for integrating the rise
pts = []
zlin = 0.0
u_prev = 0.0
for i in range(n + 1):
    u = turns * i / n
    # integrate rise rate pitch*env(u) from u_prev to u
    if i > 0:
        du = (u - u_prev) / fine
        for k in range(fine):
            a = u_prev + k * du
            zlin += pitch * 0.5 * (env(a) + env(a + du)) * du
    u_prev = u
    t = u / turns
    r = r0 + (r1 - r0) * t
    th = 2 * math.pi * u
    z = zlin + amp * env(u) * math.sin(2 * math.pi * waves_per_turn * u)
    pts.append(cq.Vector(r * math.cos(th), r * math.sin(th), z))

path_edge = cq.Edge.makeSpline(pts)
path = cq.Wire.assembleEdges([path_edge])

# ---------------- profile at path start ----------------
p0 = pts[0]
hw, ht = width / 2.0, thick / 2.0
corners = [
    cq.Vector(p0.x - hw, p0.y, p0.z - ht),
    cq.Vector(p0.x + hw, p0.y, p0.z - ht),
    cq.Vector(p0.x + hw, p0.y, p0.z + ht),
    cq.Vector(p0.x - hw, p0.y, p0.z + ht),
    cq.Vector(p0.x - hw, p0.y, p0.z - ht),
]
profile = cq.Wire.makePolygon(corners)

# ---------------- sweep with fixed binormal (keeps section horizontal) ----------------
solid = cq.Solid.sweep(profile, [], path, makeSolid=True, isFrenet=False,
                       mode=cq.Vector(0, 0, 1))

result = cq.Workplane("XY").add(solid)
