import cadquery as cq

# Create the main cylinder along X-axis
# Start with a circle in the YZ plane (at X=0) with diameter 20.0 mm
wp1 = cq.Workplane("YZ").circle(10.0).extrude(80.0, combine=True)

# Create the second cylinder along Z-axis
# Start at X=40.0 mm with a circle of diameter 20.0 mm in YZ plane
# and extrude 40.0 mm along Z direction
wp2 = cq.Workplane("YZ").moveTo(40.0, 0, 0).circle(10.0).extrude(40.0, combine=True)

# Combine both cylinders using union operation
result = wp1.union(wp2)
