import cadquery as cq
import math

OD, ID, T = 120.0, 80.0, 20.0
PCD = 100.0
cb_d, cb_depth, thru_d = 10.0, 10.0, 6.0

ring = cq.Workplane("XY").circle(OD/2).circle(ID/2).extrude(T)

pts = [(PCD/2*math.cos(math.radians(60*i)), PCD/2*math.sin(math.radians(60*i))) for i in range(6)]

result = (ring.faces(">Z").workplane()
          .pushPoints(pts)
          .cboreHole(thru_d, cb_d, cb_depth))
