import cadquery as cq

# Main blank: 80 x 60 x 30, centered in XY, bottom at Z=0
blank = cq.Workplane("XY").box(80, 60, 30, centered=(True, True, False))

# Notch block: 50 x 30 x 20, corner at (40, 30, 30)
notch = cq.Workplane("XY").box(50, 30, 20, centered=False).translate((-10, 0, 10))

body = blank.cut(notch)

tol = 1e-3

def concave_edges(full=True):
    sel = []
    for e in body.edges().vals():
        bb = e.BoundingBox()
        # Edge along Y at x=-10, z=10
        if abs(bb.xmin + 10) < tol and abs(bb.xmax + 10) < tol and abs(bb.zmin - 10) < tol and abs(bb.zmax - 10) < tol:
            sel.append(e)
        # Edge along X at y=0, z=10
        elif abs(bb.ymin) < tol and abs(bb.ymax) < tol and abs(bb.zmin - 10) < tol and abs(bb.zmax - 10) < tol:
            sel.append(e)
        # Vertical edge at x=-10, y=0
        elif full and abs(bb.xmin + 10) < tol and abs(bb.xmax + 10) < tol and abs(bb.ymin) < tol and abs(bb.ymax) < tol:
            sel.append(e)
    return sel

try:
    result = body.newObject(concave_edges(True)).fillet(4)
    if not result.val().isValid():
        raise ValueError
except Exception:
    try:
        result = body.newObject(concave_edges(False)).fillet(4)
    except Exception:
        result = body
