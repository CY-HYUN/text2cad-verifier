import cadquery as cq
import math

# Hub: 30 mm dia, 20 mm tall, axis along Z
hub = cq.Workplane("XY").circle(15).extrude(20)

def naca_t(x, t=0.12):
    return 5 * t * (0.2969 * math.sqrt(x) - 0.1260 * x - 0.3516 * x**2
                    + 0.2843 * x**3 - 0.1036 * x**4)

def airfoil_wire(xpos, chord, angle_deg, le=(-8.5, 1.5)):
    a = math.radians(angle_deg)
    n = 14
    xs = [(1 - math.cos(math.pi * i / n)) / 2 for i in range(n + 1)]
    def mp(u, v):
        y = le[0] + chord * (u * math.cos(a) - v * math.sin(a))
        z = le[1] + chord * (u * math.sin(a) + v * math.cos(a))
        return cq.Vector(xpos, y, z)
    upper = [mp(x, naca_t(x)) for x in xs]
    lower = [mp(x, -naca_t(x)) for x in xs][::-1]
    e1 = cq.Edge.makeSpline(upper)
    e2 = cq.Edge.makeSpline(lower)
    return cq.Wire.assembleEdges([e1, e2])

# Root plane at x=15, tip plane at x=75 (leading edges aligned at the same point)
root = airfoil_wire(15, 25, 45)
tip = airfoil_wire(75, 15, 15)

blade = cq.Solid.makeLoft([root, tip], True)

# Small root stub buried in the hub so the blade fuses properly
stub_wire = airfoil_wire(10, 25, 45)
stub_face = cq.Face.makeFromWires(stub_wire)
stub = cq.Solid.extrudeLinear(stub_face, cq.Vector(5, 0, 0))

body = hub.union(cq.Workplane("XY").add(stub)).union(cq.Workplane("XY").add(blade))

# Fillet the blade/hub junction edges
def junction(e):
    c = e.Center()
    bb = e.BoundingBox()
    r = math.hypot(c.x, c.y)
    return (abs(r - 15) < 0.6 and 0.2 < c.z < 19.8 and bb.ylen > 0.5
            and bb.xmin > 5 and bb.xmax < 16.5)

try:
    edges = [e for e in body.edges().vals() if junction(e)]
    solid = body.val()
    result = cq.Workplane("XY").add(solid.fillet(2.0, edges))
except Exception:
    result = body
