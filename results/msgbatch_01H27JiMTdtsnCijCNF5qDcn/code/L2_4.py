import cadquery as cq

base = cq.Workplane("XY").rect(100, 100).extrude(15)
base = base.edges("|Z").fillet(10)

tube = cq.Workplane("XY").workplane(offset=15).circle(30).circle(20).extrude(40)
result = base.union(tube)

# center through hole through base
result = result.cut(cq.Workplane("XY").circle(20).extrude(55))

# four holes
holes = (cq.Workplane("XY").pushPoints([(40, 40), (-40, 40), (40, -40), (-40, -40)])
         .circle(5).extrude(15))
result = result.cut(holes)
