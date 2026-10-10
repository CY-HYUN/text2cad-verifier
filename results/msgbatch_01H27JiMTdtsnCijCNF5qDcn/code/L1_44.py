import cadquery as cq
import math

# Cube 40x40x40, base on XY plane, extruded upward
cube = cq.Workplane("XY").rect(40.0, 40.0).extrude(40.0)

# Through hole, diameter 20, from top face
through = (
    cq.Workplane("XY")
    .workplane(offset=40.0)
    .circle(10.0)
    .extrude(-40.0)
)

# Counterbore, diameter 30, depth 10 from top face
cbore = (
    cq.Workplane("XY")
    .workplane(offset=40.0)
    .circle(15.0)
    .extrude(-10.0)
)

result = cube.cut(through).cut(cbore)
