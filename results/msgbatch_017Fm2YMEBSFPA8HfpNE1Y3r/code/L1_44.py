import cadquery as cq

# Create the base cube
result = cq.Workplane("XY").box(40.0, 40.0, 40.0)

# Select the top face and add the through hole (diameter 20.0 mm)
result = result.faces(">Z").workplane().hole(20.0, 40.0)

# Create counterbore by selecting top face and cutting a pocket
result = result.faces(">Z").workplane().pocket(10.0, mode="add")
result = result.circles(15.0)  # radius 15.0 (diameter 30.0)

# Alternative approach: manually create the counterbore using a cylinder
result = cq.Workplane("XY").box(40.0, 40.0, 40.0)

# Add through hole
result = result.faces(">Z").workplane().hole(20.0, 40.0)

# Add counterbore by cutting a shallow cylinder from top
result = result.cut(
    cq.Workplane("XY")
    .workplane(offset=30.0)
    .circle(15.0)
    .extrude(-10.0)
)

