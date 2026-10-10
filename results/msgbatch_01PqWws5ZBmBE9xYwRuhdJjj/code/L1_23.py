import cadquery as cq

# Create a new workplane with origin at (0,0,0)
wp = cq.Workplane("XY")

# Draw the larger circle with diameter 50.0 mm (radius 25.0 mm)
# Center at (0, 0, 0)
large_circle = wp.circle(25.0)

# Draw the smaller circle with diameter 30.0 mm (radius 15.0 mm)
# Center at (40.0, 0, 0) to be externally tangent
# Distance between centers: 25.0 + 15.0 = 40.0 mm
small_circle = wp.circle(15.0).moved(cq.Vector(40.0, 0.0, 0.0))

# Create faces from both circles
face_large = large_circle.val()
face_small = small_circle.val()

# Extrude both circles along +Z direction by 50.0 mm
cylinder_large = wp.circle(25.0).extrude(50.0)
cylinder_small = wp.circle(15.0).moved(cq.Vector(40.0, 0.0, 0.0)).extrude(50.0)

# Merge the two cylinders using union
result = cylinder_large.union(cylinder_small)
