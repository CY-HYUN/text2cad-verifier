import cadquery as cq
import math

# Create the main cylindrical body
main_body = cq.Workplane("XY").circle(20).extrude(40)

# Create the countersunk hole structure
# Start with a sketch on the top face
hole = (cq.Workplane("XY")
        .circle(10)  # Lower through-hole diameter
        .extrude(-40, combine=False))  # Through the entire height

# Create the upper countersunk portion (large hole)
countersink = (cq.Workplane("XY")
               .circle(10)  # Upper large hole diameter
               .extrude(-10, combine=False))  # 10mm deep

# Combine: start with main body, subtract both hole features
result = main_body.cut(hole).cut(countersink)
