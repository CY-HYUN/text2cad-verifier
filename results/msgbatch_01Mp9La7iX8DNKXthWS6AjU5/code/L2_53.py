import cadquery as cq
import math

# Cube frame
cube = cq.Workplane("XY").box(60, 60, 60)

# Cut circular holes through all three axes (circles on all six faces)
hole_d = 40
cut_z = cq.Workplane("XY").circle(hole_d / 2).extrude(70, both=True)
cut_x = cq.Workplane("YZ").circle(hole_d / 2).extrude(70, both=True)
cut_y = cq.Workplane("XZ").circle(hole_d / 2).extrude(70, both=True)
frame = cube.cut(cut_z).cut(cut_x).cut(cut_y)

# Central sphere (revolved semicircle profile)
sphere = (
    cq.Workplane("XZ")
    .moveTo(0, -15)
    .threePointArc((15, 0), (0, 15))
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)

result = frame.union(sphere)

# Connecting columns along the body diagonals
col_d = 4.0
length = 45.0
for sx in (1, -1):
    for sy in (1, -1):
        for sz in (1, -1):
            d = cq.Vector(sx, sy, sz).normalized()
            cyl = cq.Solid.makeCylinder(
                col_d / 2, length, cq.Vector(0, 0, 0), d
            )
            result = result.union(cq.Workplane("XY").add(cyl))
