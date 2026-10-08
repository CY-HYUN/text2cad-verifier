import cadquery as cq
import math

# Base
base = cq.Workplane("XY").box(100, 100, 15, centered=(True, True, False))

# Base hub
hub = cq.Workplane("XY").workplane(offset=15).circle(35).extrude(10)
result = base.union(hub)

# Vertical plate at rear edge (y from 30 to 50)
plate = cq.Workplane("XY").center(0, 40).rect(100, 20).extrude(120)
result = result.union(plate)

# Vertical bearing seat (axis along Y, at z=80, centered on plate y=40)
seat = cq.Workplane("XY").add(
    cq.Solid.makeCylinder(35, 30, cq.Vector(0, 25, 80), cq.Vector(0, 1, 0))
)
result = result.union(seat)

# Reinforcing rib on YZ center plane
rib = (
    cq.Workplane("YZ")
    .polyline([(30, 15), (-20, 15), (30, 65)])
    .close()
    .extrude(7.5, both=True)
)
result = result.union(rib)

# Base hub through-hole
hub_hole = cq.Workplane("XY").workplane(offset=-1).circle(25).extrude(40)
result = result.cut(hub_hole)

# Bearing seat bore
bore = cq.Workplane("XY").add(
    cq.Solid.makeCylinder(20, 40, cq.Vector(0, 20, 80), cq.Vector(0, 1, 0))
)
result = result.cut(bore)

# Mounting holes
mh = (
    cq.Workplane("XY").workplane(offset=-1)
    .pushPoints([(40, 40), (-40, 40), (40, -40), (-40, -40)])
    .circle(6).extrude(30)
)
result = result.cut(mh)

# M8 hole at top of bearing seat down to bore
m8 = cq.Workplane("XY").add(
    cq.Solid.makeCylinder(4, 25, cq.Vector(0, 40, 95), cq.Vector(0, 0, 1))
)
result = result.cut(m8)
