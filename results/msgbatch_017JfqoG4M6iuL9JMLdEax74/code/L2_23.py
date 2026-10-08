import cadquery as cq

def body(side, dia, ext=0.0):
    r = dia / 2.0
    base = cq.Workplane("XY").workplane(offset=-ext).rect(side, side).extrude(20 + ext)
    trans = (cq.Workplane("XY").workplane(offset=20)
             .rect(side, side)
             .workplane(offset=20)
             .circle(r)
             .loft(combine=True))
    top = cq.Workplane("XY").workplane(offset=40).circle(r).extrude(20 + ext)
    return base.union(trans).union(top)

outer = body(50.0, 30.0)
inner = body(46.0, 26.0, ext=1.0)

result = outer.cut(inner)
