import cadquery as cq
import math

# Multi-section loft along X (sections on YZ-parallel planes at X=0, 50, 100, 150)
body = (
    cq.Workplane("YZ")
    .circle(7.5)                       # Plane1, X=0, dia 15
    .workplane(offset=50)
    .ellipse(12.5, 10)                 # Plane2, X=50, 25 x 20
    .workplane(offset=50)
    .ellipse(11, 9)                    # Plane3, X=100, 22 x 18
    .workplane(offset=50)
    .circle(10)                        # Plane4, X=150, dia 20
    .loft(ruled=False, combine=True)
)

# Shell: remove both end faces, wall thickness 1.5 mm (inward)
result = body.faces("<X or >X").shell(-1.5)
