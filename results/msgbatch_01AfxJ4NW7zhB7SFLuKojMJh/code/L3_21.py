import cadquery as cq
import math

# Profile in XY plane: x = axis, y = radius. Revolve about the X axis.
rt = 5.0           # throat radius
R_arc = 50.0
ri0 = (rt + R_arc) - math.sqrt(R_arc**2 - 20.0**2)   # inlet inner radius
mid_r = (rt + R_arc) - math.sqrt(R_arc**2 - 10.0**2)

# Outer ellipse: center x=50, semi-axis a=45 along x, b=10 in radius, base radius 20
def outer(x):
    return 20.0 + 10.0 * math.sqrt(max(0.0, 1 - ((x - 50.0) / 45.0) ** 2))

outer_pts = [(x, outer(x)) for x in [5 + 90 * i / 24 for i in range(1, 24)]]

# Divergent parabola: r = 5 + a (x-20)^2, passes through (100, 20)
a = 15.0 / 80.0**2
par_pts = [(x, rt + a * (x - 20) ** 2) for x in [100 - 80 * i / 16 for i in range(1, 17)]]

w = (cq.Workplane("XY")
     .moveTo(0, ri0)
     .lineTo(0, 30)
     .lineTo(5, 30)
     .lineTo(5, 20)
     .spline(outer_pts + [(95, 20)], includeCurrent=True)
     .lineTo(95, 30)
     .lineTo(100, 30)
     .lineTo(100, 20)
     .spline(par_pts, includeCurrent=True)
     .threePointArc((10, mid_r), (0, ri0))
     .close())

result = w.revolve(360, (0, 0, 0), (1, 0, 0))
