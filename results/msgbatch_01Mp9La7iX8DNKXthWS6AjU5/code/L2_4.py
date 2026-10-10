import cadquery as cq

plate = cq.Workplane("XY").box(100, 100, 15, centered=(True, True, False))
plate = plate.edges("|Z").fillet(10)

tube = (cq.Workplane("XY").workplane(offset=15)
        .circle(30).circle(20).extrude(40))

result = plate.union(tube)

# center through hole through the plate
bore = cq.Workplane("XY").circle(20).extrude(55)
result = result.cut(bore)

# four mounting holes
holes = (cq.Workplane("XY")
         .pushPoints([(40, 40), (-40, 40), (40, -40), (-40, -40)])
         .circle(5).extrude(55))
result = result.cut(holes)
