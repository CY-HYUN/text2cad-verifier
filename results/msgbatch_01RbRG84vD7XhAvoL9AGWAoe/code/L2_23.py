import cadquery as cq

t = 2.0
S = 50.0
D = 30.0
h1, h2, h3 = 20.0, 20.0, 20.0

# Outer solid
outer_box = cq.Workplane("XY").rect(S, S).extrude(h1)
outer_loft = (cq.Workplane("XY").workplane(offset=h1)
              .rect(S, S)
              .workplane(offset=h2)
              .circle(D / 2)
              .loft(combine=True))
outer_cyl = (cq.Workplane("XY").workplane(offset=h1 + h2)
             .circle(D / 2).extrude(h3))
outer = outer_box.union(outer_loft).union(outer_cyl)

# Inner void
si = S - 2 * t
ri = D / 2 - t
inner_box = (cq.Workplane("XY").workplane(offset=-1)
             .rect(si, si).extrude(h1 + 1))
inner_loft = (cq.Workplane("XY").workplane(offset=h1)
              .rect(si, si)
              .workplane(offset=h2)
              .circle(ri)
              .loft(combine=True))
inner_cyl = (cq.Workplane("XY").workplane(offset=h1 + h2)
             .circle(ri).extrude(h3 + 1))

result = outer.cut(inner_box).cut(inner_loft).cut(inner_cyl)
