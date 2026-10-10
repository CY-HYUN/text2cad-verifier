import cadquery as cq
import math

# Base flange 100x100x15, centered in XY, z 0..15
base = cq.Workplane("XY").box(100, 100, 15, centered=(True, True, False))

# Bearing hub OD70, height 10 on top of the base
hub = cq.Workplane("XY").workplane(offset=15).circle(35).extrude(10)

# Vertical support plate: 20 thick at the -Y edge, 70 wide, 120 high
plate = cq.Workplane("XY").box(70, 20, 120, centered=(True, False, False)).translate((0, -50, 0))

# Bearing boss OD70 along Y, axis at z=80, y from -50 to -20
boss = (cq.Workplane("XZ", origin=(0, -20, 0)).center(0, 80).circle(35).extrude(30))

body = base.union(hub).union(plate).union(boss)

# Triangular ribs (15 thick) at the inner junction, in the YZ plane
for xc in (-27.5, 27.5):
    rib = (cq.Workplane("YZ", origin=(xc - 7.5, 0, 0))
           .polyline([(-30, 15), (30, 15), (-30, 100)]).close().extrude(15))
    body = body.union(rib)

# Central through hole dia 50
body = body.cut(cq.Workplane("XY").circle(25).extrude(60))

# Horizontal bearing bore dia 40 through the boss/plate
bore = cq.Workplane("XZ", origin=(0, -15, 0)).center(0, 80).circle(20).extrude(40)
body = body.cut(bore)

# Four mounting holes dia 12 at the base corners
holes = (cq.Workplane("XY").pushPoints([(42.5, 42.5), (-42.5, 42.5), (42.5, -42.5), (-42.5, -42.5)])
         .circle(6).extrude(15))
body = body.cut(holes)

# M8 grease hole (6.8 tap drill) from top into the bore
grease = cq.Workplane("XY", origin=(0, -35, 80)).circle(3.4).extrude(40)
body = body.cut(grease)

result = body
