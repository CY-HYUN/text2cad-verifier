import cadquery as cq
import math

# Base
base = cq.Workplane("XY").box(100, 100, 15, centered=(True, True, False))

# Hub on top of base
hub = cq.Workplane("XY").workplane(offset=15).circle(35).extrude(10)
body = base.union(hub)

# Vertical plate at rear edge (y 30..50), z 0..120
plate = cq.Workplane("XY").box(100, 20, 120, centered=(True, False, False)).translate((0, 30, 0))
body = body.union(plate)

# Bearing seat along Y, axis at z=80, symmetric about plate center plane y=40 (y 25..55)
seat = (cq.Workplane("XZ").workplane(offset=-55)  # XZ normal is -Y; offset -55 -> y=55
        .center(0, 80).circle(35).extrude(30))     # extrudes toward -Y: y 55 -> 25
body = body.union(seat)

# Reinforcing rib: right triangle 50x50 in YZ plane, 15 mm each side of x=0
rib = (cq.Workplane("YZ")
       .polyline([(30, 15), (-20, 15), (30, 65)]).close()
       .extrude(15, both=True))
body = body.union(rib)

# Hub through-hole (50) through hub and base
body = body.cut(cq.Workplane("XY").circle(25).extrude(30))

# Bearing bore (40) through seat
bore = (cq.Workplane("XZ").workplane(offset=-60)
        .center(0, 80).circle(20).extrude(40))
body = body.cut(bore)

# Four mounting holes (12) at 80x80 spacing through base
holes = (cq.Workplane("XY")
         .pushPoints([(40, 40), (-40, 40), (40, -40), (-40, -40)])
         .circle(6).extrude(15))
body = body.cut(holes)

# M8 radial hole from top of bearing seat down to bore
m8 = cq.Workplane("XY").workplane(offset=80).center(0, 40).circle(4).extrude(40)
body = body.cut(m8)

result = body
