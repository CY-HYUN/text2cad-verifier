import cadquery as cq

# Create the bottom cylinder
# Circle with diameter 80mm on XY plane, extruded 20mm upward
bottom_cylinder = cq.Workplane("XY").circle(40).extrude(20)

# Create the top cylinder on the top surface of the bottom cylinder
# Circle with diameter 40mm (radius 20mm) on the top surface, extruded 30mm upward
top_cylinder = (
    cq.Workplane("XY")
    .workplane(offset=20)  # Move to the top surface of bottom cylinder
    .circle(20)  # Diameter 40mm means radius 20mm
    .extrude(30)  # Extrude 30mm upward
)

# Combine both cylinders using union (merge/join)
result = bottom_cylinder.union(top_cylinder)
