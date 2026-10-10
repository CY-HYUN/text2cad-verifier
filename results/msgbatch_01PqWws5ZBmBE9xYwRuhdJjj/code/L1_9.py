import cadquery as cq

# Create a cylinder: circle (diameter 30mm) on XY plane, extruded 100mm upward
cylinder = cq.Workplane("XY").circle(15).extrude(100)

# Create a sphere with diameter 40mm (radius 20mm)
# Position its center at (0, 0, 115) - which is 5mm above the cylinder's top surface at z=100
sphere = cq.Solid.makeSphere(20, pnt=cq.Vector(0, 0, 115))

# Perform Boolean union to merge the cylinder and sphere
result = cylinder.union(sphere)
