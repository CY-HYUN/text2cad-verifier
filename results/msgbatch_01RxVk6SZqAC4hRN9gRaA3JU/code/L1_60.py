import cadquery as cq

result = (
    cq.Workplane("XY")
    .circle(50.0)
    .extrude(12.0)
    .faces(">Z").workplane()
    .pushPoints([(35, 0), (0, 35), (-35, 0), (0, -35)])
    .hole(10.0)
)

# Chamfer the hole edges on the top face (exclude outer edge)
result = (
    result.faces(">Z")
    .edges(cq.selectors.RadiusNthSelector(0))
    .chamfer(0.8)
)
