import cadquery as cq

# Sphere of radius 25 mm centred at the origin
sphere = cq.Workplane("XY").sphere(25.0)

# 20 x 20 mm square column, extruded symmetrically along Z (60 mm total)
cutter = cq.Workplane("XY").rect(20.0, 20.0).extrude(30.0, both=True)

# Subtract the column to leave a square through-hole
result = sphere.cut(cutter)
