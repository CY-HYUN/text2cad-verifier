import cadquery as cq

def body(sq, d, ext=0.0):
    a = cq.Workplane("XY").workplane(offset=-ext).rect(sq, sq).extrude(20 + ext)
    b = (cq.Workplane("XY").workplane(offset=20).rect(sq, sq)
         .workplane(offset=20).circle(d / 2).loft(ruled=True))
    c = cq.Workplane("XY").workplane(offset=40).circle(d / 2).extrude(20 + ext)
    return a.union(b).union(c)

outer = body(50, 30)
inner = body(46, 26, ext=1)
result = outer.cut(inner)
