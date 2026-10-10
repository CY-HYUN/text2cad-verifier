import cadquery as cq
import math

# Create a 60mm cube
cube = cq.Workplane("XY").box(60, 60, 60)

# Create square holes along X axis (40mm x 40mm, extending full length)
hole_x = cq.Workplane("YZ").rect(40, 40).extrude(60)
cube = cube.cut(hole_x)

# Create square holes along Y axis (40mm x 40mm, extending full length)
hole_y = cq.Workplane("XZ").rect(40, 40).extrude(60)
cube = cube.cut(hole_y)

# Create square holes along Z axis (40mm x 40mm, extending full length)
hole_z = cq.Workplane("XY").rect(40, 40).extrude(60)
cube = cube.cut(hole_z)

result = cube
