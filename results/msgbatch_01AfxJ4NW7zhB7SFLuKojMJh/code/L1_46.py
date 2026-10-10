import cadquery as cq
import math

# Right triangle base: legs 30 (X) and 40 (Y), extruded 60 along Z
result = (
    cq.Workplane("XY")
    .polyline([(0, 0), (30, 0), (0, 40)])
    .close()
    .extrude(60)
)
