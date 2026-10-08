import cadquery as cq

# Sphere of radius 25 mm centred at the origin
sphere = cq.Workplane("XY").sphere(25.0)

# 20 x 20 mm square column, extruded symmetrically along Z (total length > 50 mm so it cuts fully through)
cutter = (
    cq.Workplane("XY")
    .rect(20.0, 20.0)
    .extrude(30.0, both=True)
)

# Subtract the column from the sphere to leave a square through-hole
result = sphere.cut(cutter)
