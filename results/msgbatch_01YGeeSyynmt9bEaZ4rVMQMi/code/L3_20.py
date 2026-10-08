import cadquery as cq
import math

# ---------------- Hub ----------------
hub_d = 30.0
hub_h = 20.0
hub_r = hub_d / 2.0
hub = cq.Workplane("XY").circle(hub_r).extrude(hub_h)

z_mid = hub_h / 2.0
le_offset = -12.5  # common leading edge position (aligned leading edges)


def naca_points(c, t=0.12, n=30):
    """Return upper (LE->TE) and lower (LE->TE) local (u, v) points."""
    up, lo = [], []
    for i in range(n + 1):
        b = math.pi * i / n
        x = 0.5 * (1 - math.cos(b))
        yt = 5 * t * (0.2969 * math.sqrt(x) - 0.1260 * x - 0.3516 * x**2
                      + 0.2843 * x**3 - 0.1036 * x**4)
        up.append((x * c, yt * c))
        lo.append((x * c, -yt * c))
    return up, lo


def airfoil_wire(r, c, ang_deg):
    a = math.radians(ang_deg)
    up, lo = naca_points(c)

    def to3d(p):
        u, v = p
        u = u + le_offset
        # rotate about the common leading-edge line, then add the offset again
        u0 = le_offset
        du = u - u0
        y = u0 + du * math.cos(a) - v * math.sin(a)
        z = z_mid + du * math.sin(a) + v * math.cos(a)
        return cq.Vector(r, y, z)

    up3 = [to3d(p) for p in up]
    lo3 = [to3d(p) for p in lo]
    lo3[0] = up3[0]
    lo3[-1] = up3[-1]
    e1 = cq.Edge.makeSpline(up3)
    e2 = cq.Edge.makeSpline(lo3)
    return cq.Wire.assembleEdges([e1, e2])


root_r, tip_r = 15.0, 75.0
root_w = airfoil_wire(root_r, 25.0, 45.0)
tip_w = airfoil_wire(tip_r, 15.0, 15.0)
inner_w = airfoil_wire(5.0, 25.0, 45.0)  # embed root into hub

blade = cq.Solid.makeLoft([root_w, tip_w], False)
embed = cq.Solid.makeLoft([inner_w, root_w], True)

result = hub.union(cq.Workplane("XY").add(embed)).union(cq.Workplane("XY").add(blade))

# ---------------- Fillet at blade/hub junction ----------------
try:
    def on_junction(e):
        for t in (0.0, 0.25, 0.5, 0.75, 1.0):
            p = e.positionAt(t)
            if abs(math.hypot(p.x, p.y) - hub_r) > 0.05:
                return False
            if p.z < 0.05 or p.z > hub_h - 0.05:
                return False
        return True

    edges = [e for e in result.val().Edges() if on_junction(e)]
    if edges:
        filleted = result.val().fillet(2.0, edges)
        if filleted.isValid():
            result = cq.Workplane("XY").add(filleted)
except Exception:
    pass
