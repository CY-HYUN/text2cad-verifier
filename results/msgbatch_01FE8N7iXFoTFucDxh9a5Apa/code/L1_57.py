import cadquery as cq

# Rectangular blank, bottom face centred on the origin
blank = cq.Workplane("XY").box(80, 60, 30, centered=(True, True, False))

# Notch removed from the upper +X/+Y corner (outer corner at (40, 30, 30))
notch = cq.Workplane("XY").box(50, 30, 20, centered=False).translate((-10, 0, 10))
body = blank.cut(notch)

def pick(targets, tol=1e-3):
    """Return a selector function that keeps edges whose centres match the targets."""
    def f(objs):
        out = []
        for e in objs:
            c = e.Center()
            for t in targets:
                if abs(c.x - t[0]) < tol and abs(c.y - t[1]) < tol and abs(c.z - t[2]) < tol:
                    out.append(e)
                    break
        return out
    return f

# Concave edges of the notch: two floor edges and the vertical inner edge
all_inner = [(-10, 15, 10), (15, 0, 10), (-10, 0, 20)]
floor_only = [(-10, 15, 10), (15, 0, 10)]

result = body
for targets in (all_inner, floor_only):
    try:
        edges = pick(targets)(body.edges().vals())
        if edges:
            shp = body.val().fillet(4, edges)
            if shp.isValid():
                result = cq.Workplane("XY").newObject([shp])
                break
    except Exception:
        pass
