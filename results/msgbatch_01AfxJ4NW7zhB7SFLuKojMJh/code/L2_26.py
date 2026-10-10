import cadquery as cq

# Base frame
frame = (cq.Workplane("XY")
         .rect(100, 100).rect(80, 80)
         .extrude(5))

# Legs
pts = [(45, 45), (-45, 45), (45, -45), (-45, -45)]
legs = (cq.Workplane("XY").workplane(offset=5)
        .pushPoints(pts).circle(5).extrude(50))

# Top plate
top = (cq.Workplane("XY").workplane(offset=55)
       .rect(100, 100).extrude(5))

result = frame.union(legs).union(top)
