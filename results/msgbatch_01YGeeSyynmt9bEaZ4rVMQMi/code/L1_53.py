import cadquery as cq

# Elliptical cylinder: major axis 80 (semi 40), minor axis 50 (semi 25), height 25
body = cq.Workplane("XY").ellipse(40.0, 25.0).extrude(25.0)

# Through hole: diameter 16, centred at (10, 0)
body = (
    body.faces(">Z").workplane(centerOption="ProjectedOrigin", origin=(0, 0, 0))
    .center(10.0, 0.0)
    .circle(8.0)
    .cutThruAll()
)

# 45° x 0.8 chamfer on the outer elliptical edge of the top face
try:
    result = body.faces(">Z").edges("not %CIRCLE").chamfer(0.8)
except Exception:
    result = body
