import cadquery as cq

blank = cq.Workplane("XY").box(80, 60, 30, centered=(True, True, False))
notch = (cq.Workplane("XY")
         .box(50, 30, 20, centered=False)
         .translate((-10, 0, 10)))
body = blank.cut(notch)

targets = [(-10, 15, 10), (15, 0, 10), (-10, 0, 20)]

def is_target(e):
    c = e.Center()
    return any(abs(c.x - t[0]) < 1e-3 and abs(c.y - t[1]) < 1e-3 and abs(c.z - t[2]) < 1e-3 for t in targets)

edges = [e for e in body.edges().vals() if is_target(e)]
result = body.newObject(edges).fillet(4)
