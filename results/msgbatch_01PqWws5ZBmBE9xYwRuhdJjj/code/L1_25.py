import cadquery as cq

# Create a cylinder with diameter 40mm and height 40mm
result = cq.Workplane("XY").circle(20).extrude(40)

# Add a through-hole (diameter 10mm) on the top surface
result = result.faces(">Z").workplane().circle(5).cutThruAll()

# Add a counterbore (diameter 20mm, depth 10mm) on the top surface
result = result.faces(">Z").workplane().circle(10).cutBlind(-10)
