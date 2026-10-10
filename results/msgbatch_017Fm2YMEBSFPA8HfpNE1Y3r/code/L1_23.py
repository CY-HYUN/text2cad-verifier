import cadquery as cq

# Create a new workplane with origin at (0,0,0)
wp = cq.Workplane("XY")

# Draw the larger circle with diameter 50.0 mm (radius 25.0 mm)
# Center at (0, 0, 0) and extrude
cylinder_large = wp.circle(25.0).extrude(50.0)

# Create a new workplane for the smaller circle
wp2 = cq.Workplane("XY").transformed(offset=cq.Vector(40.0, 0.0, 0.0))

# Draw the smaller circle with diameter 30.0 mm (radius 15.0 mm)
# Center at (40.0, 0, 0) to be externally tangent and extrude
cylinder_small = wp2.circle(15.0).extrude(50.0)

# Merge the two cylinders using union
result = cylinder_large.union(cylinder_small)
