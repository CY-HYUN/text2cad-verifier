import cadquery as cq
import math

L, W, H = 200.0, 100.0, 80.0
ch_z = 35.0  # internal channel elevation

# Base block
body = cq.Workplane("XY").box(L, W, H).translate((0, 0, H / 2))

# Countersunk mounting holes at corners
body = (
    body.faces(">Z").workplane()
    .pushPoints([(88, 40), (-88, 40), (88, -40), (-88, -40)])
    .cskHole(9.0, 18.0, 90)
)

cuts = []

def cyl(r, h, p, d):
    return cq.Solid.makeCylinder(r, h, cq.Vector(*p), cq.Vector(*d))

# Main horizontal distribution channel along X (internal)
cuts.append(cyl(8.0, 180.0, (-90, 0, ch_z), (1, 0, 0)))

# 3 inlets on front face (y = -50), running to the main channel
for x in (-60.0, 0.0, 60.0):
    cuts.append(cyl(10.0, 50.0, (x, -W / 2, ch_z), (0, 1, 0)))

# 10 outlets on top face: two rows of 5, with cross feeders to main channel
out_x = [-80.0, -40.0, 0.0, 40.0, 80.0]
for x in out_x:
    for y in (-15.0, 15.0):
        cuts.append(cyl(5.0, H - ch_z, (x, y, ch_z), (0, 0, 1)))
    # cross feeder along Y connecting both rows to main channel
    cuts.append(cyl(5.0, 30.0, (x, -15.0, ch_z), (0, 1, 0)))

for c in cuts:
    body = body.cut(cq.Workplane("XY").add(c))

# Weight-reduction grooves: 2 on bottom, 1 on each end face
for x in (-50.0, 50.0):
    slot = (
        cq.Workplane("XY").center(x, 0)
        .slot2D(60.0, 20.0, 0).extrude(20.0)
    )
    body = body.cut(slot)

slot_r = (
    cq.Workplane("YZ", origin=(L / 2, 0, 15.0))
    .slot2D(50.0, 16.0, 0).extrude(-15.0)
)
slot_l = (
    cq.Workplane("YZ", origin=(-L / 2, 0, 15.0))
    .slot2D(50.0, 16.0, 0).extrude(15.0)
)
body = body.cut(slot_r).cut(slot_l)

result = body
