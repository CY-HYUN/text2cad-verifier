import cadquery as cq
import math

# ---------------- Base flange ----------------
base_t = 15.0
base = cq.Workplane("XY").box(100, 100, base_t, centered=(True, True, False))

# Raised bearing hub on base
hub = (cq.Workplane("XY").workplane(offset=base_t)
       .circle(35).extrude(10))
body = base.union(hub)

# ---------------- Vertical support plate ----------------
# Plate along +Y edge, 20 thick (y = 30..50), rising 120 above base surface
plate_top = base_t + 120.0
plate = (cq.Workplane("XY")
         .box(100, 20, plate_top, centered=(True, False, False))
         .translate((0, 30, 0)))
body = body.union(plate)

# Bearing boss (horizontal, axis along Y), centerline 80 above base surface
bore_z = base_t + 80.0
boss = (cq.Workplane("XZ", origin=(0, 50, 0))
        .center(0, bore_z).circle(35).extrude(40))  # XZ normal is -Y -> y 50..10
body = body.union(boss)

# ---------------- Triangular ribs (15 thick) ----------------
for xc in (-42.5, 42.5):
    rib = (cq.Workplane("YZ", origin=(xc - 7.5, 0, 0))
           .polyline([(30, base_t), (-28, base_t), (30, bore_z)]).close()
           .extrude(15))
    body = body.union(rib)

# ---------------- Holes ----------------
# Central through hole in base / hub
body = body.cut(cq.Workplane("XY").circle(25).extrude(base_t + 10))

# Horizontal bearing bore
bore = (cq.Workplane("XZ", origin=(0, 60, 0))
        .center(0, bore_z).circle(20).extrude(70))
body = body.cut(bore)

# Four corner mounting holes (through)
holes = (cq.Workplane("XY").workplane(offset=-1)
         .pushPoints([(40, 40), (-40, 40), (40, -40), (-40, -40)])
         .circle(6).extrude(base_t + 2))
body = body.cut(holes)

# M8 grease fitting hole (tap drill 6.8) from top down into bore
grease = (cq.Workplane("XY").workplane(offset=plate_top + 1)
          .center(0, 40).circle(3.4).extrude(-(plate_top + 1 - bore_z)))
body = body.cut(grease)
# Small counterbore/thread relief at top
body = body.cut(cq.Workplane("XY").workplane(offset=plate_top)
                .center(0, 40).circle(4.0).extrude(-10))

result = body
