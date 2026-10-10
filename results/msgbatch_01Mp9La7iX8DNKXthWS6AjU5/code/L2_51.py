import cadquery as cq

# T-shaped profile: top bar 60 x 20, stem 20 wide x 40 tall
pts = [
    (-10, 0), (10, 0), (10, 40), (30, 40), (30, 60),
    (-30, 60), (-30, 40), (-10, 40)
]
body = cq.Workplane("XY").polyline(pts).close().extrude(20)

# Fillet all edges with 8 mm radius
body = body.edges().fillet(8)

# Through holes, 5 mm diameter, at the centre of the three flat end faces
hole_x = cq.Solid.makeCylinder(2.5, 80, cq.Vector(-40, 50, 10), cq.Vector(1, 0, 0))
hole_y = cq.Solid.makeCylinder(2.5, 80, cq.Vector(0, -10, 10), cq.Vector(0, 1, 0))

result = body.cut(cq.Workplane("XY").add(hole_x)).cut(cq.Workplane("XY").add(hole_y))
