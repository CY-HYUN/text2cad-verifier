import cadquery as cq
import math

t = 5.0
z_top = 75.0
r_flange = 85.0
flange_t = 5.0
r_hole = 5.0

def zi(r):
    return r * r / 80.0

def outer(r):
    s = 1.0 / math.sqrt(1 + (r / 40.0) ** 2)
    return (r + t * s * r / 40.0, zi(r) - t * s)

def bisect(f, a, b):
    for _ in range(80):
        m = (a + b) / 2
        if f(a) * f(m) <= 0:
            b = m
        else:
            a = m
    return (a + b) / 2

r_top = math.sqrt(80 * z_top)
z_fb = z_top - flange_t
# parameter where outer surface reaches flange underside
p_end = bisect(lambda r: outer(r)[1] - z_fb, 1.0, 100.0)
# parameter where outer radius equals hole radius
p_start = bisect(lambda r: outer(r)[0] - r_hole, 0.0, 10.0)

n = 30
inner_pts = [(r_hole + (r_top - r_hole) * i / n, 0) for i in range(n + 1)]
inner_pts = [(x, zi(x)) for x, _ in inner_pts]
outer_pts = [outer(p_end + (p_start - p_end) * i / n) for i in range(n + 1)]

prof = (
    cq.Workplane("XZ")
    .moveTo(*inner_pts[0])
    .spline(inner_pts[1:], includeCurrent=True)
    .lineTo(r_flange, z_top)
    .lineTo(r_flange, z_fb)
    .lineTo(*outer_pts[0])
    .spline(outer_pts[1:], includeCurrent=True)
    .close()
)
body = prof.revolve(360, (0, 0, 0), (0, 1, 0))

r_bc = (outer(p_end)[0] + r_flange) / 2.0
pts = [(r_bc * math.cos(math.radians(90 + 90 * k)),
        r_bc * math.sin(math.radians(90 + 90 * k))) for k in range(4)]
holes = (
    cq.Workplane("XY").workplane(offset=z_fb - 1)
    .pushPoints(pts).circle(2.5).extrude(flange_t + 2)
)
result = body.cut(holes)
