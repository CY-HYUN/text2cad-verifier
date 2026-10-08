import cadquery as cq

# Base cylinder: diameter 40 mm, height 40 mm
result = cq.Workplane("XY").circle(20.0).extrude(40.0)

# Through hole: diameter 10 mm, cut through the entire part
result = result.faces(">Z").workplane().circle(5.0).cutThruAll()

# Counterbore: diameter 20 mm, 10 mm deep from the top
result = result.faces(">Z").workplane().circle(10.0).cutBlind(-10.0)
