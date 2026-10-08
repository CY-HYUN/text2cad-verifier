import cadquery as cq
import math

R = 20.0
L = 100.0
A = 30.0
w = 6.0
depth = 4.0
rb = w / 2.0

body = cq.Workplane("XY").circle(R).extrude(L).translate((0, 0, -L / 2))
vol0 = body.val().Volume()

def path_pt(phi):
    return cq.Vector(R * math.cos(phi), R * math.sin(phi), A * math.sin(phi))

result = None

# Attempt a smooth sweep
try:
    N = 72
    pts = [path_pt(2 * math.pi * i / N) for i in range(N)]
    spline = cq.Edge.makeSpline(pts, periodic=True)
    path = cq.Wire.assembleEdges([spline])
    t = cq.Vector(0, R, A).normalized()
    plane = cq.Plane(origin=(R, 0, 0), xDir=(1, 0, 0), normal=t.toTuple())
    c = depth - rb  # bottom circle center is at radius R - c
    prof = (
        cq.Workplane(plane)
        .moveTo(-c, -rb)
        .lineTo(3.0, -rb)
        .lineTo(3.0, rb)
        .lineTo(-c, rb)
        .threePointArc((-c - rb, 0), (-c, -rb))
        .close()
    )
    groove = prof.sweep(cq.Workplane().add(path), isFrenet=False, transition="right")
    cand = body.cut(groove)
    removed = vol0 - cand.val().Volume()
    if cand.val().isValid() and 1500 < removed < 6000:
        result = cand
except Exception:
    result = None

# Fallback: discrete ball-nose cutter positions along the path
if result is None:
    N = 240
    tools = []
    for i in range(N):
        phi = 2 * math.pi * i / N
        rc = R - depth + rb
        cen = cq.Vector(rc * math.cos(phi), rc * math.sin(phi), A * math.sin(phi))
        radial = cq.Vector(math.cos(phi), math.sin(phi), 0)
        tools.append(cq.Solid.makeSphere(rb, pnt=cen, angleDegrees1=-90, angleDegrees2=90))
        tools.append(cq.Solid.makeCylinder(rb, depth + 2.0, pnt=cen, dir=radial))
    comp = cq.Compound.makeCompound(tools)
    result = body.cut(cq.Workplane().add(comp))
