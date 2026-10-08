import cadquery as cq

# Top plate: 100x100x5, sitting on top of the legs
top = cq.Workplane("XY").box(100, 100, 5, centered=(True, True, False)).translate((0, 0, 55))

# Legs: four 10mm diameter circles, 10mm in from each corner, extruded 50mm down
pts = [(40, 40), (-40, 40), (40, -40), (-40, -40)]
legs = (
    cq.Workplane("XY", origin=(0, 0, 55))
    .pushPoints(pts)
    .circle(5)
    .extrude(-50)
)

# Base frame: square ring 100x100 outer, 80x80 inner, 5mm thick
base = (
    cq.Workplane("XY", origin=(0, 0, 5))
    .rect(100, 100)
    .rect(80, 80)
    .extrude(-5)
)

result = top.union(legs).union(base)
