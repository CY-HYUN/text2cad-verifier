import cadquery as cq
import math

# Base: 100 x 100 x 15, centered in XY, bottom at z=0
base = cq.Workplane("XY").box(100, 100, 15, centered=(True, True, False))

# Hub on top of base
hub = cq.Workplane("XY").workplane(offset=15).circle(35).extrude(10)

# Vertical plate at rear edge (max Y), from base top upward 120
plate = (cq.Workplane("XY").workplane(offset=15)
         .center(0, 40).rect(100, 20).extrude(120))

# Vertical bearing seat: axis along Y, at z=80, length 30 centered on plate (y=40)
seat = (cq.Workplane("XZ", origin=(0, 40 + 15, 0))
        .center(0, 80).circle(35).extrude(30))

# Reinforcing rib in YZ plane (x=0), right angle at plate/base junction
rib = (cq.Workplane("YZ")
       .polyline([(30, 15), (-20, 15), (30, 65)]).close()
       .extrude(7.5, both=True))

body = base.union(hub).union(plate).union(seat).union(rib)

# Hub through-hole d50
hub_hole = cq.Workplane("XY").workplane(offset=-1).circle(25).extrude(30)
body = body.cut(hub_hole)

# Bearing seat bore d40
bore = (cq.Workplane("XZ", origin=(0, 60, 0))
        .center(0, 80).circle(20).extrude(40))
body = body.cut(bore)

# Mounting holes d12 at 80x80 spacing, through base
holes = (cq.Workplane("XY").workplane(offset=-1)
         .pushPoints([(40, 40), (-40, 40), (40, -40), (-40, -40)])
         .circle(6).extrude(17))
body = body.cut(holes)

# M8 hole from top of bearing seat to inner bore
m8 = cq.Workplane("XY").workplane(offset=80).center(0, 40).circle(4).extrude(40)
body = body.cut(m8)

result = body
