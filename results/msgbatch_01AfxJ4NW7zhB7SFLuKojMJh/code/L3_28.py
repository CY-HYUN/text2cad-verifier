import cadquery as cq
import math

# Base flange: 100x100x15
base = cq.Workplane("XY").box(100, 100, 15, centered=(True, True, False))
# Bearing hub OD70, 10 high
hub = cq.Workplane("XY").workplane(offset=15).circle(35).extrude(10)
body = base.union(hub)

# Vertical plate: 20 thick (y -50..-30), 120 high
plate = cq.Workplane("XY").box(100, 20, 120, centered=(True, False, False)).translate((0, -50, 0))
body = body.union(plate)

# Boss on bore axis (along Y), centre height 80, OD70, protruding 10 beyond inner face
boss = (cq.Workplane("XZ").workplane(offset=20)  # XZ normal is -Y; offset 20 -> y=-20
        .center(0, 80).circle(35).extrude(30))   # extrudes toward -Y to y=-50
body = body.union(boss)

# Triangular rib, 15 thick, centred on x=0
rib = (cq.Workplane("YZ").polyline([(-30, 15), (40, 15), (-30, 75)]).close()
       .extrude(7.5, both=True))
rib_clear = cq.Workplane("XY").circle(25).extrude(200)
rib = rib.cut(rib_clear)
body = body.union(rib)

# Central 50 mm hole through base and hub
body = body.cut(cq.Workplane("XY").circle(25).extrude(26))

# Bearing bore 40 mm along Y
bore = (cq.Workplane("XZ").workplane(offset=10).center(0, 80).circle(20).extrude(60))
body = body.cut(bore)

# Four 12 mm mounting holes at base corners
holes = (cq.Workplane("XY").pushPoints([(40, 40), (-40, 40), (40, -40), (-40, -40)])
         .circle(6).extrude(15))
body = body.cut(holes)

# M8 grease hole (tap drill 6.8) from top down into bore
grease = (cq.Workplane("XY").workplane(offset=80).center(0, -40).circle(3.4).extrude(40))
body = body.cut(grease)

result = body
