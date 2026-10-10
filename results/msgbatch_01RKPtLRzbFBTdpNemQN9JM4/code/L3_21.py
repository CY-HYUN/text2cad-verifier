import cadquery as cq
import math

# Profile in XY plane: x = axial, y = radius; revolve about X axis
def inner_div(x):
    return 5 + math.sqrt(2.8125 * (x - 20))

def outer_ell(x):
    return 30 * math.sqrt(1 - ((x - 40) / 92.0) ** 2)

# Inlet arc (R50, tangent at throat, center (20,55))
y0 = 55 - math.sqrt(2500 - 400)
ym = 55 - math.sqrt(2500 - 100)

# Outer elliptical spline points
ell_pts = [(x, outer_ell(x)) for x in [5 + i * 90 / 20.0 for i in range(21)]]
# Inner parabolic points (from exit back to throat)
par_pts = [(x, inner_div(x)) for x in [100 - i * 80 / 24.0 for i in range(25)]]

w = (cq.Workplane("XY")
     .moveTo(0, y0)
     .lineTo(0, 30)
     .lineTo(5, 30)
     .lineTo(*ell_pts[0])
     .spline(ell_pts[1:], includeCurrent=True)
     .lineTo(95, 30)
     .lineTo(100, 30)
     .lineTo(100, 20)
     .spline(par_pts[1:], includeCurrent=True)
     .threePointArc((10, ym), (0, y0))
     .close())

result = w.revolve(360, (0, 0, 0), (1, 0, 0))
