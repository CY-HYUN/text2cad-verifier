import cadquery as cq

# Disk
disk = cq.Workplane("XY").circle(50.0).extrude(12.0)

# Four holes on a 35 mm radius bolt circle, aligned with X/Y axes
pts = [(35.0, 0), (0, 35.0), (-35.0, 0), (0, -35.0)]
disk = (
    disk.faces(">Z").workplane()
    .pushPoints(pts)
    .circle(5.0)
    .cutThruAll()
)

# Chamfer hole edges on the top face (exclude the outer edge)
result = (
    disk.faces(">Z").edges(cq.selectors.RadiusNthSelector(0))
    .chamfer(0.8)
)
