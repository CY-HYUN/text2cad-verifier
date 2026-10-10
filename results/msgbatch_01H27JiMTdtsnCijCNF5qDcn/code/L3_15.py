import cadquery as cq
import math

# Outer quarter ellipse from apex (0,50) to (100,0)
n = 40
outer = [(100*math.sin(math.radians(90*i/n)), 50*math.cos(math.radians(90*i/n))) for i in range(n+1)]
# Inner quarter ellipse (offset inward 8 mm) from (92,0) to (0,42)
inner = [(92*math.sin(math.radians(90*(n-i)/n)), 42*math.cos(math.radians(90*(n-i)/n))) for i in range(n+1)]

prof = (cq.Workplane("XZ")
        .moveTo(*outer[0])
        .spline(outer[1:], includeCurrent=True)
        .lineTo(100, -25)
        .lineTo(92, -25)
        .lineTo(92, 0)
        .spline(inner[1:], includeCurrent=True)
        .close())

body = prof.revolve(360, (0, 0, 0), (0, 1, 0))

nozzle = (cq.Workplane("XY").workplane(offset=50)
          .circle(20).circle(15).extrude(30))

result = body.union(nozzle)
