import cadquery as cq
import math

cube = cq.Workplane("XY").box(60, 60, 60)

# Hole along X axis, axis at Z=5 (y=0)
hole_x = (cq.Workplane("YZ").workplane(offset=-40)
          .center(0, 5).circle(10).extrude(80))

# Hole along Y axis, axis at Z=-5 (x=0)
hole_y = (cq.Workplane("XZ").workplane(offset=-40)
          .center(0, -5).circle(10).extrude(80))

result = cube.cut(hole_x).cut(hole_y)
