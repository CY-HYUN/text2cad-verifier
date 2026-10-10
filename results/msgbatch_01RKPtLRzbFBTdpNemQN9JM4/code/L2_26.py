import cadquery as cq

top = cq.Workplane("XY").workplane(offset=50).rect(100, 100).extrude(5)

base = (cq.Workplane("XY").rect(100, 100).extrude(5)
        .cut(cq.Workplane("XY").rect(80, 80).extrude(5)))

legs = (cq.Workplane("XY").workplane(offset=5)
        .pushPoints([(45, 45), (-45, 45), (45, -45), (-45, -45)])
        .circle(5).extrude(50))

result = top.union(base).union(legs)
