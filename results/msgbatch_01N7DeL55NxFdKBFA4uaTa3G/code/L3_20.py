import cadquery as cq
import math

# ---------------- Hub ----------------
HUB_D = 30.0
HUB_H = 20.0
hub = cq.Workplane("XY").circle(HUB_D / 2.0).extrude(HUB_H)

# ---------------- Airfoil helper ----------------
R_ROOT = 15.0   # root plane (tangent to hub)
R_TIP = 75.0    # tip plane
Z_LE = 18.5     # common leading-edge position (aligned LEs)
Y_LE = 0.0


def naca_points(chord, t=0.12, n=24):
    """NACA 00xx style closed contour: upper TE -> LE -> lower TE (local u,v)."""
    xs = [0.5 * (1 - math.cos(math.pi * i / n)) for i in range(n + 1)]  # 0..1
    def yt(x):
        return 5 * t * (0.2969 * math.sqrt(x) - 0.1260 * x - 0.3516 * x**2
                        + 0.2843 * x**3 - 0.1015 * x**4)
    upper = [(x * chord, yt(x) * chord) for x in reversed(xs)]       # TE -> LE
    lower = [(x * chord, -yt(x) * chord) for x in xs[1:]]            # LE -> TE
    return upper + lower


def airfoil_wire(chord, angle_deg, x_plane):
    a = math.radians(angle_deg)
    pts = []
    for u, v in naca_points(chord):
        # rotate about the leading edge (u=0,v=0) in the YZ plane
        y = Y_LE + u * math.sin(a) + v * math.cos(a)
        z = Z_LE - u * math.cos(a) + v * math.sin(a)
        pts.append(cq.Vector(x_plane, y, z))
    spline = cq.Edge.makeSpline(pts)
    close = cq.Edge.makeLine(pts[-1], pts[0])  # blunt trailing edge closure
    return cq.Wire.assembleEdges([spline, close])


# Root and tip profiles
root_w = airfoil_wire(25.0, 45.0, R_ROOT)
tip_w = airfoil_wire(15.0, 15.0, R_TIP)

# Twisted blade by loft
blade = cq.Solid.makeLoft([root_w, tip_w], True)

# Short root extension into the hub to guarantee a solid union
root_in = airfoil_wire(25.0, 45.0, R_ROOT - 3.0)
root_ext = cq.Solid.makeLoft([root_in, root_w], True)

body = hub.union(cq.Workplane("XY").add(root_ext)).union(cq.Workplane("XY").add(blade))

# ---------------- Fillet at blade/hub junction ----------------
result = body
try:
    def is_junction(e):
        c = e.Center()
        r = math.hypot(c.x, c.y)
        bb = e.BoundingBox()
        flat_cap = (abs(bb.zmax - bb.zmin) < 1e-3 and
                    (abs(bb.zmin) < 1e-3 or abs(bb.zmin - HUB_H) < 1e-3))
        return (abs(r - HUB_D / 2.0) < 1.5) and not flat_cap and c.x > 5.0

    edges = [e for e in body.val().Edges() if is_junction(e)]
    if edges:
        filleted = body.val().fillet(2.0, edges)
        if filleted.isValid():
            result = cq.Workplane("XY").add(filleted)
except Exception:
    result = body
