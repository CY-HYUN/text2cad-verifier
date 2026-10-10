import cadquery as cq
import math

size = 40.0
d = 10.0

cube = cq.Workplane("XY").box(size, size, size)

# Through holes along each axis (longer than the cube to guarantee a clean cut)
hole_z = cq.Workplane("XY").circle(d / 2).extrude(size * 1.5).translate((0, 0, -size * 0.75))
hole_x = cq.Workplane("YZ").circle(d / 2).extrude(size * 1.5).translate((-size * 0.75, 0, 0))
hole_y = cq.Workplane("XZ").circle(d / 2).extrude(size * 1.5).translate((0, size * 0.75, 0))

result = cube.cut(hole_z).cut(hole_x).cut(hole_y)
