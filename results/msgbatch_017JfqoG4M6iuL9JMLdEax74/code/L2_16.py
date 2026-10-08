import cadquery as cq
import math

R = 25.0          # sphere radius
noz_r = 15.0      # nozzle radius
noz_len = 20.0    # nozzle protrusion beyond sphere radius
bore_r = 10.0     # passage radius
flat_r = 10.0     # flat top circle radius

body = cq.Workplane("XY").sphere(R)

L = R + noz_len
# Nozzles along X and Y (each spans both directions from center)
noz_x = cq.Workplane("YZ").circle(noz_r).extrude(L, both=True)
noz_y = cq.Workplane("XZ").circle(noz_r).extrude(L, both=True)
body = body.union(noz_x).union(noz_y)

# Internal passages
bore_x = cq.Workplane("YZ").circle(bore_r).extrude(L + 1, both=True)
bore_y = cq.Workplane("XZ").circle(bore_r).extrude(L + 1, both=True)
body = body.cut(bore_x).cut(bore_y)

# Flat on top of sphere: 20 mm diameter flat
z_flat = math.sqrt(R**2 - flat_r**2)
cutter = cq.Workplane("XY").workplane(offset=z_flat).rect(200, 200).extrude(50)
body = body.cut(cutter)

result = body
