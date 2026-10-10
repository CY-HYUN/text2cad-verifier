import cadquery as cq
import math

R = 20.0
L = 100.0
amp = 30.0
rc = 19.0  # radius of groove-bottom arc centre (20 - 4 + 3)

body = cq.Workplane("XY").circle(R).extrude(L)

def section(phi):
    c, s = math.cos(phi), math.sin(phi)
    P = cq.Vector(rc * c, rc * s, L / 2 + amp * s)
    T = cq.Vector(-rc * s, rc * c, amp * c).normalized()
    r = cq.Vector(c, s, 0)
    r = (r - T * r.dot(T)).normalized()
    pl = cq.Plane(origin=(P.x, P.y, P.z), xDir=(r.x, r.y, r.z), normal=(T.x, T.y, T.z))
    wp = (cq.Workplane(pl)
          .moveTo(2, -3).lineTo(2, 3).lineTo(0, 3)
          .threePointArc((-3, 0), (0, -3)).close())
    return wp.ctx.pendingWires[0] if wp.ctx.pendingWires else wp.val()

n = 72
wires = []
for i in range(n + 1):
    phi = 2 * math.pi * i / n
    wires.append(section(phi))

groove = cq.Solid.makeLoft(wires, False)
result = body.cut(cq.Workplane("XY").add(groove))
