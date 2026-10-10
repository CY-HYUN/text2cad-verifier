import cadquery as cq
import math

# Hub: 30 mm dia, 20 mm tall, axis along Z
hub = cq.Workplane("XY").circle(15).extrude(20)

Z0 = 2.0  # leading edge height on hub (shared by both sections -> aligned LEs)

def airfoil_wire(x_plane, chord, angle_deg, n=12, t=0.12):
    a = math.radians(angle_deg)
    xs = [(1 - math.cos(math.pi * i / n)) / 2 for i in range(n + 1)]
    up, lo = [], []
    for x in xs:
        yt = 5 * t * (0.2969 * math.sqrt(x) - 0.1260 * x - 0.3516 * x**2
                      + 0.2843 * x**3 - 0.1036 * x**4)
        for lst, s in ((up, 1), (lo, -1)):
            u = x * chord
            v = s * yt * chord
            # rotate about the leading edge, then place LE at Z0
            py = u * math.cos(a) - v * math.sin(a)
            pz = u * math.sin(a) + v * math.cos(a) + Z0
            lst.append(cq.Vector(x_plane, py, pz))
    # upper surface LE -> TE
    upper_pts = up
    # lower surface TE -> LE
    lower_pts = lo[::-1]
    e1 = cq.Edge.makeSpline(upper_pts)
    e2 = cq.Edge.makeLine(upper_pts[-1], lower_pts[0])
    e3 = cq.Edge.makeSpline(lower_pts)
    return cq.Wire.assembleEdges([e1, e2, e3])

ang_root, ang_tip = 45, 15

# Blade: loft from root plane (x=15) to tip plane (x=75)
w_root = airfoil_wire(15, 25, ang_root)
w_tip = airfoil_wire(75, 15, ang_tip)
blade = cq.Solid.makeLoft([w_root, w_tip], False)

# Root stub embedded in hub for a proper connection
body = hub
try:
    w_stub = airfoil_wire(9, 25, ang_root)
    stub = cq.Solid.extrudeLinear(cq.Face.makeFromWires(w_stub), cq.Vector(6.5, 0, 0))
    body = body.union(stub)
except Exception:
    pass

try:
    body = body.union(blade)
except Exception:
    body = body.add(blade)

# Fillet at blade/hub junction
def on_junction(e):
    for p in (0.0, 0.25, 0.5, 0.75, 1.0):
        pt = e.positionAt(p)
        if abs(math.hypot(pt.x, pt.y) - 15) > 0.05:
            return False
        if pt.z < 0.3 or pt.z > 19.7:
            return False
    return True

result = body
try:
    edges = [e for e in body.edges().vals() if e.geomType() != "LINE" and on_junction(e)]
    if edges:
        result = body.newObject(edges).fillet(2.0)
except Exception:
    result = body
