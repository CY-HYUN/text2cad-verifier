import cadquery as cq
import math

R = 25.0          # sphere radius
nozzle_r = 15.0   # nozzle radius
nozzle_len = 20.0 # protrusion beyond sphere surface
bore_r = 10.0     # passage radius
flat_r = 10.0     # top flat radius

body = cq.Workplane("XY").sphere(R)

L = R + nozzle_len  # nozzle end distance from center

# Nozzles along +X, -X, +Y, -Y
nx = cq.Workplane("YZ").circle(nozzle_r).extrude(L, both=True)
ny = cq.Workplane("XZ").circle(nozzle_r).extrude(L, both=True)
body = body.union(nx).union(ny)

# Through passages
bx = cq.Workplane("YZ").circle(bore_r).extrude(L + 1, both=True)
by = cq.Workplane("XZ").circle(bore_r).extrude(L + 1, both=True)
body = body.cut(bx).cut(by)

# Top flat of 20mm diameter
z_flat = math.sqrt(R**2 - flat_r**2)
cutter = cq.Workplane("XY").workplane(offset=z_flat).rect(200, 200).extrude(50)
body = body.cut(cutter)

result = body
