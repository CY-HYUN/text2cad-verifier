import cadquery as cq
import math

size = 40.0
d = 10.0

cube = cq.Workplane("XY").box(size, size, size)

# Through holes along each axis, centered at the cube center
hole_z = cq.Workplane("XY").circle(d / 2).extrude(size * 2, both=True)
hole_x = cq.Workplane("YZ").circle(d / 2).extrude(size * 2, both=True)
hole_y = cq.Workplane("XZ").circle(d / 2).extrude(size * 2, both=True)

result = cube.cut(hole_z).cut(hole_x).cut(hole_y)
