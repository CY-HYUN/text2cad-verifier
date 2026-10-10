import cadquery as cq
import math

# Base
base = cq.Workplane("XY").box(100, 100, 15, centered=(True, True, False))

# Hub on top of base
hub = cq.Workplane("XY").workplane(offset=15).circle(35).extrude(10)

# Vertical plate at rear edge (y 30..50), z 0..120
plate = cq.Workplane("XY").box(100, 20, 120, centered=(True, False, False)).translate((0, 30, 0))

# Bearing seat along Y, centered on plate mid-plane (y=40), z=80
seat = cq.Workplane("XY").add(
    cq.Solid.makeCylinder(35, 30, cq.Vector(0, 25, 80), cq.Vector(0, 1, 0))
)

# Rib: right triangle 50x50 in YZ plane, 15 mm each side of center
rib = (
    cq.Workplane("YZ")
    .polyline([(30, 15), (-20, 15), (30, 65)])
    .close()
    .extrude(15, both=True)
)

body = base.union(hub).union(plate).union(seat).union(rib)

# Bearing bore (dia 40) along Y
bore = cq.Workplane("XY").add(
    cq.Solid.makeCylinder(20, 80, cq.Vector(0, 5, 80), cq.Vector(0, 1, 0))
)
body = body.cut(bore)

# Hub/base through hole dia 50
hole50 = cq.Workplane("XY").add(
    cq.Solid.makeCylinder(25, 40, cq.Vector(0, 0, -5), cq.Vector(0, 0, 1))
)
body = body.cut(hole50)

# Four mounting holes dia 12 through the base only
mount = (
    cq.Workplane("XY")
    .workplane(offset=-1)
    .pushPoints([(40, 40), (-40, 40), (40, -40), (-40, -40)])
    .circle(6)
    .extrude(16)
)
body = body.cut(mount)

# M8 radial hole from top of seat down to the bore
m8 = cq.Workplane("XY").add(
    cq.Solid.makeCylinder(4, 45, cq.Vector(0, 40, 80), cq.Vector(0, 0, 1))
)
body = body.cut(m8)

result = body
