import cadquery as cq

# Datum plane heights
z1, z2, z3, z4 = 0, 20, 50, 70  # plane1, plane2, plane3, top of cylinder

def build(sq, d, off=0):
    base = cq.Workplane("XY").workplane(offset=z1 - off).rect(sq, sq).extrude(z2 - z1 + off)
    trans = (cq.Workplane("XY").workplane(offset=z2).rect(sq, sq)
             .workplane(offset=z3 - z2).circle(d / 2).loft(combine=True))
    top = cq.Workplane("XY").workplane(offset=z3).circle(d / 2).extrude(z4 - z3 + off)
    return base.union(trans).union(top)

outer = build(50, 30)

try:
    result = outer.faces(">Z or <Z").shell(-2)
    if not result.val().isValid():
        raise ValueError
except Exception:
    inner = build(46, 26, off=1)
    result = outer.cut(inner)
