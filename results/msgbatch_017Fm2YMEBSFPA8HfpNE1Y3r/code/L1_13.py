import cadquery as cq

# Create the main cylinder along X-axis
# Start with a circle in the YZ plane (at X=0) with diameter 20.0 mm
main_cylinder = cq.Workplane("YZ").circle(10.0).extrude(80.0)

# Create the second cylinder along Z-axis
# Start at X=40.0 mm with a circle of diameter 20.0 mm in YZ plane
# and extrude 40.0 mm along Z direction
secondary_cylinder = cq.Workplane("YZ").circle(10.0).extrude(40.0).translate((40.0, 0, 0))

# Combine both cylinders using union operation
result = main_cylinder.union(secondary_cylinder)
