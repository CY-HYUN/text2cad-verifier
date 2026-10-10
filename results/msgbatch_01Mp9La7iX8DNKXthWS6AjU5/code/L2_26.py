import cadquery as cq

plate = cq.Workplane("XY").box(100, 100, 5, centered=(True, True, False))

legs = (cq.Workplane("XY")
        .pushPoints([(40, 40), (-40, 40), (40, -40), (-40, -40)])
        .circle(5).extrude(-50))

frame = (cq.Workplane("XY").workplane(offset=-50)
         .rect(100, 100).rect(80, 80).extrude(-5))

result = plate.union(legs).union(frame)
