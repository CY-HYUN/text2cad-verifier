import cadquery as cq

# Top plate: 100x100x5, sitting on top of the 50 mm legs
top = cq.Workplane("XY").workplane(offset=50).rect(100, 100).extrude(5)

# Legs: D10 circles centred 10 mm in from each corner, extruded 50 mm downward
pts = [(40, 40), (-40, 40), (40, -40), (-40, -40)]
legs = (
    cq.Workplane("XY").workplane(offset=50)
    .pushPoints(pts).circle(5)
    .extrude(-50)
)

# Base frame: square ring 100x100 outer, 80x80 inner, extruded 5 mm below the legs
frame = (
    cq.Workplane("XY")
    .rect(100, 100).rect(80, 80)
    .extrude(-5)
)

result = top.union(legs).union(frame)
