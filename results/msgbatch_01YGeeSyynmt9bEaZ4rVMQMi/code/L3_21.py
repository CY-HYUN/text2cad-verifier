import cadquery as cq
import math

# Inner contour: parabola r = 5 + k*x^2 through (80, 25)
k = (25.0 - 5.0) / (80.0 ** 2)
inner_para = [(x, 5.0 + k * x * x) for x in range(10, 81, 10)]

# Outer contour: elliptical-like arc from (-20,20) to (80,30),
# keeping the throat wall thickest
outer_pts = []
for i in range(1, 11):
    t = i / 10.0
    x = 80.0 - 100.0 * t
    # ellipse-shaped blend: radius drops toward the inlet with a thick throat region
    th = math.pi / 2 * t
    r = 30.0 - 10.0 * (1 - math.cos(th)) - 4.0 * math.sin(math.pi * t)
    outer_pts.append((x, r))
outer_pts[-1] = (-20.0, 20.0)

profile = (
    cq.Workplane("XY")
    .moveTo(-20, 15)
    .threePointArc((-11, 7.5), (0, 5))
    .spline(inner_para, includeCurrent=True)
    .lineTo(80, 30)
    .spline(outer_pts, includeCurrent=True)
    .close()
)

body = profile.revolve(360, (0, 0, 0), (1, 0, 0))

# Flanges
flange_t = 6.0
inlet_flange = (
    cq.Workplane("YZ").workplane(offset=-20 - flange_t)
    .circle(35).circle(15).extrude(flange_t)
)
outlet_flange = (
    cq.Workplane("YZ").workplane(offset=80)
    .circle(42).circle(25).extrude(flange_t)
)

result = body.union(inlet_flange).union(outlet_flange)

# Bolt holes in flanges
inlet_holes = (
    cq.Workplane("YZ").workplane(offset=-20 - flange_t)
    .polarArray(28, 0, 360, 6).circle(2.5).extrude(flange_t)
)
outlet_holes = (
    cq.Workplane("YZ").workplane(offset=80)
    .polarArray(36, 0, 360, 8).circle(2.5).extrude(flange_t)
)
result = result.cut(inlet_holes).cut(outlet_holes)
