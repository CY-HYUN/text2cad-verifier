import cadquery as cq
import math

# --- Base flange ---
base = cq.Workplane("XY").box(100, 100, 15, centered=(True, True, False))

# Raised bearing hub on base
hub = cq.Workplane("XY").workplane(offset=15).circle(35).extrude(10)
body = base.union(hub)

# --- Vertical support plate (along +Y edge) ---
plate = cq.Workplane("XY").box(100, 20, 120, centered=(True, False, False)) \
    .translate((0, 30, 15))
body = body.union(plate)

# Bearing boss (axis along Y), centerline 80 mm above base top surface
zc = 15 + 80
boss = cq.Workplane("XZ", origin=(0, 60, 0)).center(0, zc).circle(35).extrude(40)  # y 60 -> 20
body = body.union(boss)

# --- Triangular reinforcing ribs (15 mm thick) at inner junction ---
for x0 in (-50, 35):
    rib = (cq.Workplane("YZ", origin=(x0, 0, 0))
           .polyline([(30, 15), (-25, 15), (30, 100)]).close()
           .extrude(15))
    body = body.union(rib)

# --- Holes ---
# Central through-hole in base and hub
body = body.cut(cq.Workplane("XY").circle(25).extrude(30))

# Horizontal shaft bore through boss and plate
bore = cq.Workplane("XZ", origin=(0, 70, 0)).center(0, zc).circle(20).extrude(60)
body = body.cut(bore)

# Four corner mounting holes
for sx in (-40, 40):
    for sy in (-40, 40):
        body = body.cut(
            cq.Workplane("XY", origin=(sx, sy, -1)).circle(6).extrude(17))

# M8 grease fitting hole (tap drill 6.8) from top down into bore
grease = cq.Workplane("XY", origin=(0, 40, zc)).circle(3.4).extrude(60)
body = body.cut(grease)

result = body
