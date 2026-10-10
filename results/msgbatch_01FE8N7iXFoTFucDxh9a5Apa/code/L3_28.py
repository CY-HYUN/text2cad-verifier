import cadquery as cq
import math

# --- Base flange ---
base = cq.Workplane("XY").box(100, 100, 15, centered=(True, True, False))

# Raised bearing hub on top of base
hub = cq.Workplane("XY").workplane(offset=15).circle(35).extrude(10)
body = base.union(hub)

# --- Vertical support plate (along +Y edge) ---
plate_w = 70
plate = (cq.Workplane("XY")
         .center(0, 40)
         .rect(plate_w, 20)
         .extrude(120))
body = body.union(plate)

# Bearing boss (axis along Y), centre 80 mm above base top surface
bore_z = 15 + 80
boss = (cq.Workplane("XZ", origin=(0, 60, 0))
        .center(0, bore_z)
        .circle(35)
        .extrude(40))  # XZ normal is -Y: from y=60 to y=20
body = body.union(boss)

# --- Triangular rib (15 mm thick, in YZ plane) ---
rib = (cq.Workplane("YZ", origin=(-7.5, 0, 0))
       .polyline([(30, 15), (30, 62), (-12, 15)])
       .close()
       .extrude(15))
body = body.union(rib)

# --- Central through-hole in base/hub ---
body = body.cut(cq.Workplane("XY").workplane(offset=-1).circle(25).extrude(40))

# --- Horizontal bearing bore ---
body = body.cut(
    cq.Workplane("XZ", origin=(0, 70, 0)).center(0, bore_z).circle(20).extrude(60)
)

# --- Mounting holes at base corners ---
holes = (cq.Workplane("XY").workplane(offset=-1)
         .pushPoints([(41, 41), (-41, 41), (41, -41), (-41, -41)])
         .circle(6).extrude(20))
body = body.cut(holes)

# --- M8 grease hole (tap drill 6.8) from top of boss into bore ---
grease = (cq.Workplane("XY").workplane(offset=bore_z)
          .center(0, 40).circle(3.4).extrude(50))
body = body.cut(grease)

result = body
